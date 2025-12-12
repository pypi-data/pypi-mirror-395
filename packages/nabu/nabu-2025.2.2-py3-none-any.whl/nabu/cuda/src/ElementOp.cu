#include <cupy/complex.cuh>

typedef complex<float> complex64;


// Generic operations
#define OP_ADD 0
#define OP_SUB 1
#define OP_MUL 2
#define OP_DIV 3
//

#ifndef GENERIC_OP
#define GENERIC_OP OP_ADD
#endif

// arr2D *= arr1D (line by line, i.e along fast dim)
__global__ void inplace_complex_mul_2Dby1D(complex64* arr2D, complex64* arr1D, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    // This does not seem to work
    // Use cuCmulf of cuComplex.h ?
    //~ arr2D[y*width + x] *= arr1D[x];
    size_t i = y*width + x;
    complex64 a = arr2D[i];
    complex64 b = arr1D[x];
    // arr2D[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    // arr2D[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
    arr2D[i] = a * b; // cuCmulf(a, b);
}

__global__ void inplace_generic_op_2Dby2D(float* arr2D, float* arr2D_other, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    uint i = y*width + x;

    #if GENERIC_OP == OP_ADD
    arr2D[i] += arr2D_other[i];
    #elif GENERIC_OP == OP_SUB
    arr2D[i] -= arr2D_other[i];
    #elif GENERIC_OP == OP_MUL
    arr2D[i] *= arr2D_other[i];
    #elif GENERIC_OP == OP_DIV
    arr2D[i] /= arr2D_other[i];
    #endif
}


// launched with (Nx, Ny, Nz) threads
// does array3D[x, y, z] = op(array3D[x, y, z], array1D[x]) (in the "numpy broadcasting" sense)
__global__ void inplace_generic_op_3Dby1D(
    float * array3D,
    float* array1D,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    uint z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= Nx) || (y >= Ny) || (z >= Nz)) return;
    size_t idx = ((z * Ny) + y)*Nx + x;

    #if GENERIC_OP == OP_ADD
    array3D[idx] += array1D[x];
    #elif GENERIC_OP == OP_SUB
    array3D[idx] -= array1D[x];
    #elif GENERIC_OP == OP_MUL
    array3D[idx] *= array1D[x];
    #elif GENERIC_OP == OP_DIV
    array3D[idx] /= array1D[x];
    #endif
}


// arr3D *= arr1D (along fast dim)
__global__ void inplace_complex_mul_3Dby1D(complex64* arr3D, complex64* arr1D, int width, int height, int depth) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    int z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= width) || (y >= height) || (z >= depth)) return;
    // This does not seem to work
    // Use cuCmulf of cuComplex.h ?
    //~ arr3D[(z*height + y)*width + x] *= arr1D[x];
    size_t i = (z*height + y)*width + x;
    complex64 a = arr3D[i];
    complex64 b = arr1D[x];
    // arr3D[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    // arr3D[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
    arr3D[i] = a * b; // cuCmulf(a, b);
}



// arr2D *= arr2D
__global__ void inplace_complex_mul_2Dby2D(complex64* arr2D_out, complex64* arr2D_other, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    size_t i = y*width + x;
    complex64 a = arr2D_out[i];
    complex64 b = arr2D_other[i];
    // arr2D_out[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    // arr2D_out[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
    arr2D_out[i] = a * b; // cuCmulf(a, b);
}


// arr2D *= arr2D
__global__ void inplace_complexreal_mul_2Dby2D(complex64* arr2D_out, float* arr2D_other, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    int i = y*width + x;
    complex64 a = arr2D_out[i];
    float b = arr2D_other[i];
    // arr2D_out[i]._M_re *= b;
    // arr2D_out[i]._M_im *= b;
    arr2D_out[i] *= b;
}


/*
  Kernel used for CTF phase retrieval

    img_f = img_f * filter_num
    img_f[0, 0] -= mean_scale_factor * filter_num[0,0]
    img_f = img_f * filter_denom

    where mean_scale_factor = Nx*Ny
*/
__global__ void CTF_kernel(
    complex64* image,
    float* filter_num,
    float* filter_denom,
    float mean_scale_factor,
    int Nx,
    int Ny
) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx) || (y >= Ny)) return;
    uint idx = y*Nx + x;

    image[idx] *= filter_num[idx];
    if (idx == 0) image[idx] -= mean_scale_factor;
    image[idx] *= filter_denom[idx];
}



#ifndef DO_CLIP_MIN
    #define DO_CLIP_MIN 0
#endif

#ifndef DO_CLIP_MAX
    #define DO_CLIP_MAX 0
#endif

// arr = -log(arr)
__global__ void nlog(float* array, int Nx, int Ny, int Nz, float clip_min, float clip_max) {
    size_t x = blockDim.x * blockIdx.x + threadIdx.x;
    size_t y = blockDim.y * blockIdx.y + threadIdx.y;
    size_t z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= Nx) || (y >= Ny) || (z >= Nz)) return;
    size_t pos = (z*Ny + y)*Nx + x;
    float val = array[pos];
    #if DO_CLIP_MIN
        val = fmaxf(val, clip_min);
    #endif
    #if DO_CLIP_MAX
        val = fminf(val, clip_max);
    #endif
    array[pos] = -logf(val);
}



// Reverse elements of a 2D array along "x", i.e:
// arr = arr[:, ::-1]
// launched with grid (Nx/2, Ny)
__global__ void reverse2D_x(float* array, int Nx, int Ny) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx/2) || (y >= Ny)) return;
    uint pos = y*Nx + x;
    uint pos2 = y*Nx + (Nx - 1 - x);
    float tmp = array[pos];
    array[pos] = array[pos2];
    array[pos2] = tmp;
}


/**

  Generic mul-add kernel with possibly-complicated indexing.

  dst[DST_IDX] = fac_dst*dst[DST_IDX] + fac_other*other[OTHER_IDX]
  where
    DST_IDX = dst_start_row:dst_end_row, dst_start_col:dst_end_col
    OTHER_IDX = other_start_row:other_end_row, other_start_col:other_end_col

  Usage:
    mul_add(dst, other, dst_nx, other_nx, a, b, (x1, x2), (y1, y2), (x3, x4), (y3, y4))
*/

__global__ void  mul_add(
    float* dst,
    float* other,
    int dst_width,
    int other_width,
    float fac_dst,
    float fac_other,
    int2 dst_x_range,
    int2 dst_y_range,
    int2 other_x_range,
    int2 other_y_range
    )
{
    size_t x = blockDim.x * blockIdx.x + threadIdx.x;
    size_t y = blockDim.y * blockIdx.y + threadIdx.y;

    int x_start_dst = dst_x_range.x;
    int x_stop_dst = dst_x_range.y;
    int y_start_dst = dst_y_range.x;
    int y_stop_dst = dst_y_range.y;

    int x_start_other = other_x_range.x;
    int x_stop_other = other_x_range.y;
    int y_start_other = other_y_range.x;
    int y_stop_other = other_y_range.y;

    int operation_width = x_stop_dst - x_start_dst; // assumed == x_stop_other - x_start_other
    int operation_height = y_stop_dst - y_start_dst; // assumed == y_stop_other - y_start_other

    if ((x >= operation_width) || (y >= operation_height)) return;

    size_t idx_in_dst = (y + y_start_dst)*dst_width + (x + x_start_dst);
    size_t idx_in_other = (y + y_start_other)*other_width + (x + x_start_other);

    dst[idx_in_dst] = fac_dst * dst[idx_in_dst] + fac_other * other[idx_in_other];
}

