#include "boundary.h"
typedef unsigned int uint;

#ifndef MEDFILT_X
    #define MEDFILT_X 3
#endif
#ifndef MEDFILT_Y
    #define MEDFILT_Y 3
#endif


#ifndef DO_THRESHOLD
    #define DO_THRESHOLD 0
#endif


// General-purpose 2D (or batched 2D) median filter with a square footprint.
// Boundary handling is customized via the USED_CONV_MODE macro (see boundary.h)
// Most of the time is spent computing the median, so this kernel can be sped up by
//  - creating dedicated kernels for 3x3, 5x5 (see http://ndevilla.free.fr/median/median/src/optmed.c)
//  - Using a quickselect algorithm instead of sorting (see http://ndevilla.free.fr/median/median/src/quickselect.c)
__global__ void medfilt2d(
    float * input,
    float * output,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz,  // input/output depth
    float threshold // threshold for thresholded median filter
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(MEDFILT_X);

    // Get elements in a 3x3 neighborhood
    float elements[MEDFILT_X*MEDFILT_Y] = {0};
    for (int jy = 0; jy <= hR+hL; jy++) {
        CONV_IDX_Y; // Get index "y"
        for (int jx = 0; jx <= hR+hL; jx++) {
            CONV_IDX_X; // Get index "x"
            elements[jy*MEDFILT_Y+jx] = READ_IMAGE_2D_XY;
        }
    }
    // Sort the elements with insertion sort
    // TODO quickselect ?
    int i = 1, j;
    while (i < MEDFILT_X*MEDFILT_Y) {
        j = i;
        while (j > 0 && elements[j-1] > elements[j]) {
            float tmp = elements[j];
            elements[j] = elements[j-1];
            elements[j-1] = tmp;
            j--;
        }
        i++;
    }
    float median = elements[MEDFILT_X*MEDFILT_Y/2];

    #if DO_THRESHOLD == 1
    float out_val = 0.0f;
    uint idx = (gidz*Ny + gidy)*Nx + gidx;
    if (input[idx] >= median + threshold) out_val = median;
    else out_val = input[idx];
    output[idx] = out_val;

    #elif DO_THRESHOLD == 2
    float out_val = 0.0f;
    uint idx = (gidz*Ny + gidy)*Nx + gidx;
    if (fabsf(input[idx] - median) > threshold) out_val = median;
    else out_val = input[idx];
    output[idx] = out_val;

    #else
    output[(gidz*Ny + gidy)*Nx + gidx] = median;
    #endif
}

