#include <pyopencl-complex.h>


static inline void swap(global DTYPE* arr, size_t idx, size_t idx2) {
    DTYPE tmp = arr[idx];
    arr[idx] = arr[idx2];
    arr[idx2] = tmp;
}


/*
    This code should work but it not used yet.
    The first intent was to have an in-place fftshift for odd-sized arrays:
      fftshift_odd = fftshift_even followed by roll(-1) on second half of the array
      ifft_odd = fftshift_even followed by roll(1) on second half of the array

    Roll elements (as in numpy.roll(arr, 1)) of an array, in-place.
    Needs to be launched with a large horizontal work group.
*/
__kernel void roll_forward_x(
    __global DTYPE* array,
    int Nx,
    int Ny,
    int offset_x,
    __local DTYPE* shmem
) {

    int Nx_tot = Nx;
    if (offset_x > 0) {
        Nx_tot = Nx;
        Nx -= offset_x;
    }

    int x = get_global_id(0), y = get_global_id(1);
    if ((x >= Nx / 2) || (y >= Ny)) return;

    __global DTYPE* arr = array + y * Nx_tot + offset_x;

    int lid = get_local_id(0);
    int wg_size = get_local_size(0);

    int n_steps = (int) ceil((Nx - (Nx & 1)) * 1.0f / (2*wg_size));

    DTYPE previous, current, write_on_first;
    int offset = 0;

    for (int step = 0; step < n_steps; step++) {

        int idx = 2*lid + 1;
        if (offset + idx >= Nx) break;

        previous = arr[offset + idx - 1];
        current = arr[offset + idx];
        arr[offset + idx] = previous;

        if ((step == n_steps - 1) && (offset + idx + 1 >= Nx - 1)) {
            if (Nx & 1) write_on_first = arr[offset + idx + 1];
            else write_on_first = current;
        }

        barrier(CLK_LOCAL_MEM_FENCE);

        if ((step > 0) && (lid == 0)) arr[offset + idx - 1] = shmem[0];
        if ((lid == wg_size - 1) && (step < n_steps - 1)) shmem[0] = current;
        else if (offset + idx + 1 <= Nx - 1) arr[offset + idx + 1] = current;

        if ((step == n_steps - 1) && (offset + idx + 1 >= Nx - 1)) arr[0] = write_on_first;

        barrier(CLK_LOCAL_MEM_FENCE);

        offset += 2 * wg_size;
    }

}


__kernel void revert_array_x(
    __global DTYPE* array,
    int Nx,
    int Ny,
    int offset_x
) {
    int x = get_global_id(0), y = get_global_id(1);

    int Nx_tot = Nx;
    if (offset_x > 0) {
        Nx_tot = Nx;
        Nx -= offset_x;
    }

    if ((x >= Nx / 2) || (y >= Ny)) return;

    size_t idx = y * Nx_tot + offset_x + x;
    size_t idx2 = y * Nx_tot + offset_x + (Nx - 1 - x); // Nx ?
    swap(array, idx, idx2);
}