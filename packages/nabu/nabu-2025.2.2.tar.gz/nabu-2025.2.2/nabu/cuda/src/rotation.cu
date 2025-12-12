typedef unsigned int uint;

__global__ void rotate(
    cudaTextureObject_t tex_image,
    float*  output,
    int Nx,
    int Ny,
    float cos_angle,
    float sin_angle,
    float rotc_x,
    float rotc_y
) {
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    if (gidx >= Nx || gidy >= Ny) return;

    float x = (gidx - rotc_x)*cos_angle - (gidy - rotc_y)*sin_angle;
    float y = (gidx - rotc_x)*sin_angle + (gidy - rotc_y)*cos_angle;
    x += rotc_x;
    y += rotc_y;

    float out_val = tex2D<float>(tex_image, x + 0.5f, y + 0.5f);
    output[gidy * Nx + gidx] = out_val;

}
