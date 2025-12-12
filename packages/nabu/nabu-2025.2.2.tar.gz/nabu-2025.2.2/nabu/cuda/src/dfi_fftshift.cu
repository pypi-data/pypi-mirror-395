#include <cufft.h>
#define BLOCK_SIZE 16

__global__ void dfi_cuda_swap_quadrants_complex(cufftComplex *input, cufftComplex *output, int dim_x) {

    int idx = blockIdx.x * BLOCK_SIZE + threadIdx.x;
    int idy = blockIdx.y * BLOCK_SIZE + threadIdx.y;

    const int dim_y = gridDim.y * blockDim.y; //a half of real length

    output[idy * dim_x + idx] = input[(dim_y + idy) * dim_x + idx + 1];
    output[(dim_y + idy) * dim_x + idx] = input[idy * dim_x + idx + 1];
}

__global__ void dfi_cuda_swap_quadrants_real(cufftReal *output) {

    int idx = blockIdx.x * BLOCK_SIZE + threadIdx.x;
    int idy = blockIdx.y * BLOCK_SIZE + threadIdx.y;

    const int dim_x = gridDim.x * blockDim.x;
    int dim_x2 = dim_x/2, dim_y2 = dim_x2;
    long sw_idx1, sw_idx2;

    sw_idx1 = idy * dim_x + idx;

    cufftReal temp = output[sw_idx1];
    if (idx < dim_x2) {
        sw_idx2 = (dim_y2 + idy) * dim_x + (dim_x2 + idx);
        output[sw_idx1] = output[sw_idx2];
        output[sw_idx2] = temp;
    }
    else {
        sw_idx2 = (dim_y2 + idy) * dim_x + (idx - dim_x2);
        output[sw_idx1] = output[sw_idx2];
        output[sw_idx2] = temp;
    }
}

__global__ void swap_full_quadrants_complex(cufftComplex *output) {

    int idx = blockIdx.x * BLOCK_SIZE + threadIdx.x;
    int idy = blockIdx.y * BLOCK_SIZE + threadIdx.y;

    const int dim_x = gridDim.x * blockDim.x;
    int dim_x2 = dim_x/2, dim_y2 = dim_x2;
    long sw_idx1, sw_idx2;

    sw_idx1 = idy * dim_x + idx;

    cufftComplex temp = output[sw_idx1];
    if (idx < dim_x2) {
        sw_idx2 = (dim_y2 + idy) * dim_x + (dim_x2 + idx);
        output[sw_idx1] = output[sw_idx2];
        output[sw_idx2] = temp;
    }
    else {
        sw_idx2 = (dim_y2 + idy) * dim_x + (idx - dim_x2);
        output[sw_idx1] = output[sw_idx2];
        output[sw_idx2] = temp;
    }
}

__global__ void dfi_cuda_crop_roi(cufftReal *input, int x, int y, int roi_x, int roi_y, int raster_size, float scale, cufftReal *output) {

    int idx = blockIdx.x * BLOCK_SIZE + threadIdx.x;
    int idy = blockIdx.y * BLOCK_SIZE + threadIdx.y;

    if (idx < roi_x && idy < roi_y) {
        output[idy * roi_x + idx] = input[(idy + y) * raster_size + (idx + x)] * scale;
    }
}
