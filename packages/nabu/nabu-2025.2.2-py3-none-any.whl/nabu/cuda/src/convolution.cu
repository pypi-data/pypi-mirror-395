/*
 * Convolution (without textures)
 * Adapted from OpenCL code of the the silx project
 *
*/

#include "boundary.h"

typedef unsigned int uint;


/******************************************************************************/
/**************************** 1D Convolution **********************************/
/******************************************************************************/


// Convolution with 1D kernel along axis "X" (fast dimension)
// Works for batched 1D on 2D and batched 2D on 3D, along axis "X".
__global__ void convol_1D_X(
    float * input,
    float * output,
    float * filter,
    int L, // filter size
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(L);
    float sum = 0.0f;

    for (int jx = 0; jx <= hR+hL; jx++) {
        CONV_IDX_X; // Get index "x"
        sum += READ_IMAGE_1D_X * filter[L-1 - jx];
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}


// Convolution with 1D kernel along axis "Y"
// Works for batched 1D on 2D and batched 2D on 3D, along axis "Y".
__global__ void convol_1D_Y(
    float * input,
    float * output,
    float * filter,
    int L, // filter size
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(L);
    float sum = 0.0f;

    for (int jy = 0; jy <= hR+hL; jy++) {
        CONV_IDX_Y; // Get index "y"
        sum += READ_IMAGE_1D_Y * filter[L-1 - jy];
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}


// Convolution with 1D kernel along axis "Z"
// Works for batched 1D on 2D and batched 2D on 3D, along axis "Z".
__global__ void convol_1D_Z(
    float * input,
    float * output,
    float * filter,
    int L, // filter size
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(L);
    float sum = 0.0f;

    for (int jz = 0; jz <= hR+hL; jz++) {
        CONV_IDX_Z; // Get index "z"
        sum += READ_IMAGE_1D_Z * filter[L-1 - jz];
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}


/******************************************************************************/
/**************************** 2D Convolution **********************************/
/******************************************************************************/

// Convolution with 2D kernel
// Works for batched 2D on 3D.
__global__ void convol_2D_XY(
    float * input,
    float * output,
    float * filter,
    int Lx, // filter number of columns,
    int Ly, // filter number of rows,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(Lx);
    float sum = 0.0f;

    for (int jy = 0; jy <= hR+hL; jy++) {
        CONV_IDX_Y; // Get index "y"
        for (int jx = 0; jx <= hR+hL; jx++) {
            CONV_IDX_X; // Get index "x"
            sum += READ_IMAGE_2D_XY * filter[(Ly-1-jy)*Lx + (Lx-1 - jx)];
        }
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}


// Convolution with 2D kernel
// Works for batched 2D on 3D.
__global__ void convol_2D_XZ(
    float * input,
    float * output,
    float * filter,
    int Lx, // filter number of columns,
    int Lz, // filter number of rows,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(Lx);
    float sum = 0.0f;

    for (int jz = 0; jz <= hR+hL; jz++) {
        CONV_IDX_Z; // Get index "z"
        for (int jx = 0; jx <= hR+hL; jx++) {
            CONV_IDX_X; // Get index "x"
            sum += READ_IMAGE_2D_XZ * filter[(Lz-1-jz)*Lx + (Lx-1 - jx)];
        }
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}


// Convolution with 2D kernel
// Works for batched 2D on 3D.
__global__ void convol_2D_YZ(
    float * input,
    float * output,
    float * filter,
    int Ly, // filter number of columns,
    int Lz, // filter number of rows,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(Ly);
    float sum = 0.0f;

    for (int jz = 0; jz <= hR+hL; jz++) {
        CONV_IDX_Z; // Get index "z"
        for (int jy = 0; jy <= hR+hL; jy++) {
            CONV_IDX_Y; // Get index "y"
            sum += READ_IMAGE_2D_YZ * filter[(Lz-1-jz)*Ly + (Ly-1 - jy)];
        }
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}



/******************************************************************************/
/**************************** 3D Convolution **********************************/
/******************************************************************************/

// Convolution with 3D kernel
__global__ void convol_3D_XYZ(
    float * input,
    float * output,
    float * filter,
    int Lx, // filter number of columns,
    int Ly, // filter number of rows,
    int Lz, // filter number of rows,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    int c, hL, hR;
    GET_CENTER_HL(Lx);
    float sum = 0.0f;

    for (int jz = 0; jz <= hR+hL; jz++) {
        CONV_IDX_Z; // Get index "z"
        for (int jy = 0; jy <= hR+hL; jy++) {
            CONV_IDX_Y; // Get index "y"
            for (int jx = 0; jx <= hR+hL; jx++) {
                CONV_IDX_X; // Get index "x"
                sum += READ_IMAGE_3D_XYZ * filter[((Lz-1-jz)*Ly + (Ly-1-jy))*Lx + (Lx-1 - jx)];
            }
        }
    }
    output[(gidz*Ny + gidy)*Nx + gidx] = sum;
}

