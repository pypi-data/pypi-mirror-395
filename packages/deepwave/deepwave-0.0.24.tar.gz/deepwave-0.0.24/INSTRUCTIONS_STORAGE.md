# Instructions for Implementing Intermediate Data Storage

This document details the implementation of the "Intermediate Data Storage" feature across the Deepwave propagators (Scalar, Elastic, etc.).

**Goal**: Allow propagators to store intermediate wavefields (required for gradient calculation during backpropagation) to **Device Memory**, **Host Memory (CPU)**, or **Disk**, with optional **Simple Compression** (8-bit quantization).

---

## 1. Core Concepts & Configuration

### 1.1. Storage Modes (`storage_mode`)
The implementation relies on integer flags passed from Python to C/CUDA:
*   **`"device"` (0)**: Store data in the compute device's RAM (GPU VRAM if CUDA, System RAM if CPU). Fastest, but limited capacity.
*   **`"cpu"` (1)**: Store data in Host System RAM. If computing on GPU, this requires Device-to-Host (D2H) transfers every saved step.
*   **`"disk"` (2)**: Store data in binary files on disk. Requires D2H transfer (if GPU) followed by File I/O. Slower, but huge capacity.
*   **`"none"` (3)**: Do not store intermediate data. Gradients are not calculated automatically for model parameters.

### 1.2. Simple Compression
*   **Algorithm**: Linearly quantizes floating-point data (float or double) to 8-bit integers (`uint8`).
    *   Stores `min` and `max` values (original precision) + `uint8` array.
    *   **Overhead**: 2 values (min/max) per compressed block.
*   **Granularity**:
    *   **CPU Backend**: Compression is applied **per-shot**.
    *   **GPU Backend**: Compression is applied **per-batch** (multiple shots compressed in parallel kernels).
*   **Alignment**: Compressed size must be aligned to `dtype_size` (4 or 8 bytes) to ensure memory accesses remain aligned.

### 1.3. Buffers Strategy
We use up to three buffers (`w_store_1`, `w_store_2`, `w_store_3`) to handle the data flow. Their roles change based on the configuration.

| Mode | Compression | `w_store_1` (Device/Compute) | `w_store_2` (Device/Comp) | `w_store_3` (Host) |
| :--- | :--- | :--- | :--- | :--- |
| **Device** | No | **History** `[steps, shots, ...]` | Unused | Unused |
| **Device** | Yes | **Staging** `[shots, ...]` | **History** `[steps, shots, ...]` | Unused |
| **CPU** | No | **Staging** `[shots, ...]` | Unused | **History** `[steps, shots, ...]` |
| **CPU** | Yes | **Staging** `[shots, ...]` | **Staging** `[shots, ...]` | **History** `[steps, shots, ...]` |
| **Disk** | No | **Staging** `[shots, ...]` | Unused | **Staging** `[shots, ...]` |
| **Disk** | Yes | **Staging** `[shots, ...]` | **Staging** `[shots, ...]` | **Staging** `[shots, ...]` |

*   **History**: The full buffer storing all time steps.
*   **Staging**: A small buffer holding only the *current* time step (for I/O transfer or compression).
*   **Device/Compute**: The buffer the C/CUDA kernel directly writes to / reads from.

---

## 2. Common Infrastructure

The shared logic is already implemented. You will utilize these existing files:
*   **Compression**: `src/deepwave/simple_compress.h/c/cu`
*   **Storage Utils**: `src/deepwave/storage_utils.h/c/cu` (Handles the logic of "Copy to Host", "Write to Disk", "Compress", etc.)
*   **Python Utils**: `TemporaryStorage` class in `src/deepwave/common.py`.

---

## 3. Propagator Implementation Guide

Follow this guide to modify `scalar.py/.c/.cu`, `elastic.py/.c/.cu`, etc. Use `scalar_born` as the reference implementation.

### 3.1. Python Wrapper (`src/deepwave/PROP.py`)

#### A. Update `__init__`
Add storage configuration arguments.
```python
storage_mode: str = "device",
storage_path: str = ".",
storage_compression: bool = False,
```

#### B. Update `forward` (The Function Wrapper)
1.  **Resolve Mode**: Convert string to int (0=Device, 1=CPU, 2=Disk, 3=None). Handle the edge case: if `device='cpu'` and `storage_mode='cpu'`, treat it as `storage_mode='device'` (since Host RAM *is* Device RAM).
2.  **Calculate Sizes**:
    *   `shot_bytes_uncomp`: `prod(model_shape) * element_size`.
    *   `shot_bytes_comp`: If compression is on, calculate size: `num_elements + 2 * element_size`. **Crucial**: Round up to the nearest multiple of `element_size` (4 or 8) to prevent misalignment when storing shots consecutively.
3.  **Allocate Buffers**: Implement the "Buffers Strategy" table above.
    *   **Tip**: For `Disk` mode, use `ctx.w_storage = TemporaryStorage(...)` to manage files. Pass the filenames to C via `ctypes`.
    *   **Tip**: For `CPU/Disk` modes on GPU, `w_store_3` must be **pinned memory** (`pin_memory=True`) for async CUDA transfers.
4.  **Signature**: Update the call to the backend function to include the 3 store tensors, filenames, storage mode, and size parameters.

#### C. Update `backward`
1.  **Retrieve**: Unpack `w_store_1/2/3` from `ctx.saved_tensors`.
2.  **Re-open Files**: If `storage_mode == 'disk'`, convert the filenames from `ctx.w_filenames_arr` back to `ctypes` pointers (pointers might be invalid across process boundaries if using multiprocessing, though threads are usually fine, re-fetching ensures safety).

### 3.2. C Backend (`src/deepwave/PROP.c`)

The C backend (CPU execution) processes shots in a loop (`for (shot = 0; shot < n_shots; ...)`).

#### A. Setup
*   Include `storage_utils.h`.
*   Inside the **Shot Loop**, open file pointers if `STORAGE_DISK`. One file per shot.

#### B. Forward Loop (Time Stepping)
*   **Check Gradient Need**: Only store if `requires_grad` is true for the relevant parameter.
*   **Pointer Arithmetic**: Determine where the kernel should write.
    *   If `STORAGE_DEVICE` (Uncompressed): `w_store_1_t` = `w_store_1 + shot_offset + step_offset`. (Write directly to history).
    *   Else: `w_store_1_t` = `w_store_1 + shot_offset`. (Write to staging).
*   **Kernel Call**: Pass `w_store_1_t`.
*   **Save**: Call `storage_save_snapshot_cpu`.
    *   This function handles the logic: Compress `store_1` -> `store_2` (if needed), Write to Disk (if needed).
    *   **Note**: CPU backend assumes `storage_save` processes *one shot*.

#### C. Backward Loop
*   **Load**: Call `storage_load_snapshot_cpu` *before* the kernel computation.
    *   Reads from Disk -> Staging. Decompresses -> `w_store_1_t`.
    *   If `STORAGE_DEVICE`, `w_store_1_t` already points to the data (or `store_2` decompresses to `store_1`).
*   **Kernel Call**: Pass `w_store_1_t` (now populated) as a `const` input.

### 3.3. CUDA Backend (`src/deepwave/PROP.cu`)

The CUDA backend processes a **batch** of shots simultaneously. File I/O happens on the Host (CPU side of the .cu file).

#### A. Setup
*   File pointers are opened once (usually using the filename of the first shot as a base, or passed as an array). *Note: In the current implementation, disk storage on GPU writes one large interleaved file or separate files? The reference `scalar_born` passes `w_filenames_ptr[0]`. Verify if the requirement is one file per batch or per shot. The `storage_utils_gpu` writes to `fp`, implying one file stream per call.*

#### B. Forward Loop
*   **Pointer Arithmetic**:
    *   `w_store_1_t`:
        *   If `STORAGE_DEVICE` (Uncompressed): `w_store_1 + step_offset`. (Base of the batch history for this step).
        *   Else: `w_store_1`. (Base of staging).
    *   Do the same for `w_store_2_t` and `w_store_3_t`.
*   **Kernel Call**: Pass `w_store_1_t`. The kernel itself will index `[shot_idx * shot_size + i]`.
*   **Save**: Call `storage_save_snapshot_gpu`.
    *   This function launches CUDA kernels for compression.
    *   It initiates `cudaMemcpyAsync` to Host (`w_store_3`).
    *   It performs `fwrite` to Disk (synchronizing stream if needed).

#### C. Backward Loop
*   **Load**: Call `storage_load_snapshot_gpu`.
    *   `fread` -> Host Staging (`w_store_3`).
    *   `cudaMemcpy` -> Device.
    *   Decompression Kernel.
*   **Kernel Call**: Pass `w_store_1_t`.

### 3.4. Kernel Implementation (C & CUDA)

1.  **Arguments**: Add `w_store` (and `wsc_store` if applicable) pointers to the kernel signature.
2.  **Forward**:
    *   Identify the "source term" or "wavefield" that constitutes the gradient input (e.g., the second derivative of the wavefield, or the wavefield itself, depending on the formulation).
    *   If `store_step` is true, write this value to `w_store[index]`.
3.  **Backward**:
    *   Read `val = w_store[index]`.
    *   Accumulate gradient: `grad[index] += ... * val`.

---

## 4. Key Implementation Details & Gotchas

1.  **Data Types**: The simple compressor handles `float` and `double`. Pass `sizeof(DW_DTYPE) == sizeof(double)` to the utils.
2.  **Alignment**: When calculating `shot_bytes_comp`, ensure it's a multiple of 4 (float) or 8 (double). The `simple_compress` function writes 2 scalars (min/max) then bytes. If the next shot starts immediately after, it must be aligned for the float/double read of the next min/max.
3.  **Step Ratio**: Data is only stored every `step_ratio` steps. Ensure your loop counters and pointer arithmetic (`step_idx = t / step_ratio`) respect this.
4.  **Batched vs Unbatched**:
    *   **CPU**: `w_store_1` pointers passed to the kernel are offset by `shot`.
    *   **GPU**: `w_store_1` pointers passed to the kernel are the *base* of the batch. The kernel calculates `shot_offset`.
5.  **Pinned Memory**: For `STORAGE_CPU` or `STORAGE_DISK` on GPU, `w_store_3` **MUST** be allocated with `pin_memory=True` in PyTorch to allow asynchronous transfer.
6.  **File Management**: Use `TemporaryStorage` to ensure files are cleaned up even if the program crashes or raises an exception.
7.  **mode=='none'**: Only the returned gradients (which will be all zero) should be allocated. No intermediate variables should be allocated or stored, and no gradients calculated during backpropagation.

