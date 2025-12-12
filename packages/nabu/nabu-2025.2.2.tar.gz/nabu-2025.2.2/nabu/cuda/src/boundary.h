#ifndef BOUNDARY_H
#define BOUNDARY_H

// Get the center index of the filter,
// and the "half-Left" and "half-Right" lengths.
// In the case of an even-sized filter, the center is shifted to the left.
#define GET_CENTER_HL(hlen){\
        if (hlen & 1) {\
            c = hlen/2;\
            hL = c;\
            hR = c;\
        }\
        else {\
            c = hlen/2 - 1;\
            hL = c;\
            hR = c+1;\
        }\
}\

// Boundary handling modes
#define CONV_MODE_REFLECT 0 // cba|abcd|dcb
#define CONV_MODE_NEAREST 1 // aaa|abcd|ddd
#define CONV_MODE_WRAP 2 // bcd|abcd|abc
#define CONV_MODE_CONSTANT 3 // 000|abcd|000
#ifndef USED_CONV_MODE
    #define USED_CONV_MODE CONV_MODE_NEAREST
#endif

#define CONV_PERIODIC_IDX_X int idx_x = gidx - c + jx; if (idx_x < 0) idx_x += Nx; if (idx_x >= Nx) idx_x -= Nx;
#define CONV_PERIODIC_IDX_Y int idx_y = gidy - c + jy; if (idx_y < 0) idx_y += Ny; if (idx_y >= Ny) idx_y -= Ny;
#define CONV_PERIODIC_IDX_Z int idx_z = gidz - c + jz; if (idx_z < 0) idx_z += Nz; if (idx_z >= Nz) idx_z -= Nz;


// clamp not in cuda
__device__ int clamp(int x, int min_, int max_) {
    return min(max(x, min_), max_);
}



#define CONV_NEAREST_IDX_X int idx_x = clamp((int) (gidx - c + jx), 0, Nx-1);
#define CONV_NEAREST_IDX_Y int idx_y = clamp((int) (gidy - c + jy), 0, Ny-1);
#define CONV_NEAREST_IDX_Z int idx_z = clamp((int) (gidz - c + jz), 0, Nz-1);

#define CONV_REFLECT_IDX_X int idx_x = gidx - c + jx; if (idx_x < 0) idx_x = -idx_x-1; if (idx_x >= Nx) idx_x = Nx-(idx_x-(Nx-1));
#define CONV_REFLECT_IDX_Y int idx_y = gidy - c + jy; if (idx_y < 0) idx_y = -idx_y-1; if (idx_y >= Ny) idx_y = Ny-(idx_y-(Ny-1));
#define CONV_REFLECT_IDX_Z int idx_z = gidz - c + jz; if (idx_z < 0) idx_z = -idx_z-1; if (idx_z >= Nz) idx_z = Nz-(idx_z-(Nz-1));


#if USED_CONV_MODE == CONV_MODE_REFLECT
    #define CONV_IDX_X CONV_REFLECT_IDX_X
    #define CONV_IDX_Y CONV_REFLECT_IDX_Y
    #define CONV_IDX_Z CONV_REFLECT_IDX_Z
#elif USED_CONV_MODE == CONV_MODE_NEAREST
    #define CONV_IDX_X CONV_NEAREST_IDX_X
    #define CONV_IDX_Y CONV_NEAREST_IDX_Y
    #define CONV_IDX_Z CONV_NEAREST_IDX_Z
#elif USED_CONV_MODE == CONV_MODE_WRAP
    #define CONV_IDX_X CONV_PERIODIC_IDX_X
    #define CONV_IDX_Y CONV_PERIODIC_IDX_Y
    #define CONV_IDX_Z CONV_PERIODIC_IDX_Z
#elif USED_CONV_MODE == CONV_MODE_CONSTANT
    #error "constant not implemented yet"
#else
    #error "Unknown convolution mode"
#endif



// Image access patterns
#define READ_IMAGE_1D_X input[(gidz*Ny + gidy)*Nx + idx_x]
#define READ_IMAGE_1D_Y input[(gidz*Ny + idx_y)*Nx + gidx]
#define READ_IMAGE_1D_Z input[(idx_z*Ny + gidy)*Nx + gidx]

#define READ_IMAGE_2D_XY input[(gidz*Ny + idx_y)*Nx + idx_x]
#define READ_IMAGE_2D_XZ input[(idx_z*Ny + gidy)*Nx + idx_x]
#define READ_IMAGE_2D_YZ input[(idx_z*Ny + idx_y)*Nx + gidx]

#define READ_IMAGE_3D_XYZ input[(idx_z*Ny + idx_y)*Nx + idx_x]

#endif
