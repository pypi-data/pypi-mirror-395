typedef unsigned int uint;

// linear interpolation along "axis 0", where values outside of bounds are extrapolated
__global__ void linear_interp_vertical(float* arr2D, float* out, int Nx, int Ny, float* x, float* x_new) {
    uint c = blockDim.x * blockIdx.x + threadIdx.x;
    uint i = blockDim.y * blockIdx.y + threadIdx.y;
    if ((c >= Nx) || (i >= Ny)) return;

    int extrapolate_side = x_new[0] > x[0] ? 1 : 0; // 0: left, 1: right
    float dx, dy;

    if (i == 0) extrapolate_side = 1;
    else if (i == Ny - 1) extrapolate_side = 0;
    int extrapolate_side_compl = 1 - extrapolate_side;

    dx = x[i+extrapolate_side] - x[i - extrapolate_side_compl];
    dy = arr2D[(i + extrapolate_side) * Nx + c] - arr2D[(i - extrapolate_side_compl) * Nx + c];
    out[i * Nx + c] =  (dy / dx) * (x_new[i] - x[i]) + arr2D[i * Nx + c];

}
