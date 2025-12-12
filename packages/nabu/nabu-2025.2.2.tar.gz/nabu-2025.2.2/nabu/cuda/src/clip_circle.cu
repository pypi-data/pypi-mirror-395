inline __device__ int is_in_circle(int x, int y, float center_x, float center_y, int radius2) {
    return (((x - center_x)*(x - center_x) + (y - center_y)*(y - center_y)) <= radius2);
}

__global__ void clip_circle(
    float* d_image,
    int Nx,
    int Ny,
    float center_x,
    float center_y,
    float clip_circle_value
)
{
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;

    if ((x >= Nx) || (y >= Ny)) return;

    int radius2 = min(Nx/2, Ny/2);
    radius2 *= radius2;

    if (!is_in_circle(x, y, center_x, center_y, radius2)) {
        d_image[y * Nx + x] = clip_circle_value;
    }
}