typedef unsigned int uint;


__global__ void histogram(
    float * array,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz,  // input/output depth
    float arr_min, // array minimum value
    float arr_max, // array maximum value
    uint* hist,    // histogram
    int nbins      // histogram size (number of bins)
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= Nx) || (gidy >= Ny) || (gidz >= Nz)) return;

    float val = array[(gidz*Ny + gidy)*Nx + gidx];
    float bin_pos = nbins * ((val - arr_min) / (arr_max - arr_min));
    uint bin_left = min((uint) bin_pos, nbins-1);
    atomicAdd(hist + bin_left, 1);
}
