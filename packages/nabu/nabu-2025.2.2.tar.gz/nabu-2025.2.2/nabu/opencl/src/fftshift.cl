#include <pyopencl-complex.h>

#ifndef DTYPE
  #define DTYPE float
#endif


static inline void swap(global DTYPE* arr, size_t idx, size_t idx2) {
    DTYPE tmp = arr[idx];
    arr[idx] = arr[idx2];
    arr[idx2] = tmp;
}


/*
  In-place one-dimensional fftshift, along horizontal dimension.
  The array can be 1D or 2D.

  direction > 0 means fftshift, direction < 0 means ifftshift.

  It works for even-sized arrays.
  Odd-sized arrays need an additional step (see roll.cl: roll_forward_x)

*/

__kernel void fftshift_x_inplace(
    __global DTYPE* arr,
    int Nx,
    int Ny,
    int direction
) {
    int x = get_global_id(0), y = get_global_id(1);

    int shift = Nx / 2;
    if (x >= shift) return;

    // (i)fftshift on odd-sized arrays cannot be done in-place in one step - need another kernel after this one
    if ((Nx & 1) && (direction > 0)) shift++;
    size_t idx = y * Nx + x;
    size_t idx_out = y * Nx + ((x + shift) % Nx);
    swap(arr, idx, idx_out);
}


#ifdef DTYPE_OUT

/*
    Out-of-place fftshift, possibly with type casting - useful for eg. fft(ifftshift(array))
*/
__kernel void fftshift_x(global DTYPE* arr, global DTYPE_OUT* dst, int Nx, int Ny, int direction) {

    int x = get_global_id(0), y = get_global_id(1);
    if (x >= Nx || y >= Ny) return;

    int shift = Nx / 2;
    if ((Nx & 1) && (direction < 0)) shift++;

    size_t idx = y * Nx + x;
    size_t idx_out = y * Nx + ((x + shift) % Nx);

    DTYPE_OUT out_item;
    #ifdef CAST_TO_COMPLEX
      out_item = cfloat_new(arr[idx], 0);
    #else
      #ifdef CAST_TO_REAL
        out_item = cfloat_real(arr[idx]);
      #else
        out_item = (DTYPE_OUT) arr[idx];
      #endif
    #endif
    dst[idx_out] = out_item;

}

#endif


