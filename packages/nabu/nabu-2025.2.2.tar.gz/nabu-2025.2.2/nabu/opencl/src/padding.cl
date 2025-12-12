
__kernel void coordinate_transform(
    __global float* array_in,
    __global float* array_out,
    __global int* cols_inds,
    __global int* rows_inds,
    int Nx,
    int Nx_padded,
    int Ny_padded
) {

    uint x = get_global_id(0);
    uint y = get_global_id(1);
    if ((x >= Nx_padded) || (y >= Ny_padded)) return;
    uint idx = y*Nx_padded  +  x;
    int x2 = cols_inds[x];
    int y2 = rows_inds[y];
    array_out[idx] = array_in[y2*Nx + x2];
}

