typedef unsigned int uint;


/**
This function padds in-place a 2D array with constant values.
It is designed to leave the data in the "FFT layout", i.e the data is *not*
in the center of the extended/padded data.

In one dimension:

<--------------- N0 ---------------->
|  original data  |  padded values  |
<----- N -------- ><---- Pl+Pr ----->

N0: width of data
Pl, Pr: left/right padding lengths

ASSUMPTIONS:
   - data is already extended before padding (its size is Nx_padded * Ny_padded)
   - the original data lies in the top-left quadrant.


**/
__global__ void padding_constant(
    float* data,
    int Nx,
    int Ny,
    int Nx_padded,
    int Ny_padded,
    int pad_left_len,
    int pad_right_len,
    int pad_top_len,
    int pad_bottom_len,
    float pad_left_val,
    float pad_right_val,
    float pad_top_val,
    float pad_bottom_val
) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx_padded) || (y >= Ny_padded)) return;
    int idx = y*Nx_padded  +  x;

    // data[s0:s0+Pd, :s1] = pad_bottom_val
    if ((Ny <= y) && (y < Ny+pad_bottom_len) && (x < Nx))
        data[idx] = pad_bottom_val;
    // data[s0+Pd:s0+Pd+Pu, :s1] = pad_top_val
    else if ((Ny + pad_bottom_len <= y) && (y < Ny+pad_bottom_len+pad_top_len) && (x < Nx))
        data[idx] = pad_top_val;
    // data[:, s1:s1+Pr] = pad_right_val
    else if ((Nx <= x) && (x < Nx+pad_right_len))
        data[idx] = pad_right_val;
    // data[:, s1+Pr:s1+Pr+Pl] = pad_left_val
    else if ((Nx+pad_right_len <= x) && (x < Nx+pad_right_len+pad_left_len))
        data[idx] = pad_left_val;
    // top-left quadrant
    else
        return;
}



__global__ void padding_edge(
    float* data,
    int Nx,
    int Ny,
    int Nx_padded,
    int Ny_padded,
    int pad_left_len,
    int pad_right_len,
    int pad_top_len,
    int pad_bottom_len
) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx_padded) || (y >= Ny_padded)) return;
    int idx = y*Nx_padded  +  x;

    //
    // This kernel can be optimized:
    //   - Optimize the logic to use less comparisons
    //   - Store the values data[0], data[s0-1, 0], data[0, s1-1], data[s0-1, s1-1]
    //     into shared memory to read only once from global mem.
    //

    // data[s0:s0+Pd, :s1] = data[s0, :s1]
    if ((Ny <= y) && (y < Ny+pad_bottom_len) && (x < Nx))
        data[idx] = data[(Ny-1)*Nx_padded+x];
    // data[s0+Pd:s0+Pd+Pu, :s1] = data[0, :s1]
    else if ((Ny + pad_bottom_len <= y) && (y < Ny+pad_bottom_len+pad_top_len) && (x < Nx))
        data[idx] = data[x];
    // data[:s0, s1:s1+Pr] = data[:s0, s1]
    else if ((y < Ny) && (Nx <= x) && (x < Nx+pad_right_len))
        data[idx] = data[y*Nx_padded + Nx-1];
    // data[:s0, s1+Pr:s1+Pr+Pl] = data[:s0, 0]
    else if ((y < Ny) && (Nx+pad_right_len <= x) && (x < Nx+pad_right_len+pad_left_len))
        data[idx] = data[y*Nx_padded];
    // data[s0:s0+Pb, s1:s1+Pr] = data[s0-1, s1-1]
    else if ((Ny <= y && y < Ny + pad_bottom_len) && (Nx <= x && x < Nx + pad_right_len))
        data[idx] = data[(Ny-1)*Nx_padded + Nx-1];
    // data[s0:s0+Pb, s1+Pr:s1+Pr+Pl] = data[s0-1, 0]
    else if ((Ny <= y && y < Ny + pad_bottom_len) && (Nx+pad_right_len <= x && x < Nx + pad_right_len+pad_left_len))
        data[idx] = data[(Ny-1)*Nx_padded];
    // data[s0+Pb:s0+Pb+Pu, s1:s1+Pr] = data[0, s1-1]
    else if ((Ny+pad_bottom_len <= y && y < Ny + pad_bottom_len+pad_top_len) && (Nx <= x && x < Nx + pad_right_len))
        data[idx] = data[Nx-1];
    // data[s0+Pb:s0+Pb+Pu, s1+Pr:s1+Pr+Pl] = data[0, 0]
    else if ((Ny+pad_bottom_len <= y && y < Ny + pad_bottom_len+pad_top_len) && (Nx+pad_right_len <= x && x < Nx + pad_right_len+pad_left_len))
        data[idx] = data[0];
    // top-left quadrant
    else
        return;
}



__global__ void coordinate_transform(
    float* array_in,
    float* array_out,
    int* cols_inds,
    int* rows_inds,
    int Nx,
    int Nx_padded,
    int Ny_padded
) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx_padded) || (y >= Ny_padded)) return;
    uint idx = y*Nx_padded  +  x;
    int x2 = cols_inds[x];
    int y2 = rows_inds[y];
    array_out[idx] = array_in[y2*Nx + x2];
}

