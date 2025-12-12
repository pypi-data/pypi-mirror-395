typedef unsigned int uint;


/**
 * Chebyshev background removal.
 * This kernel does a degree 2 polynomial estimation of each line of an array,
 * and then subtracts the estimation from each line.
 * This process is done in-place.
 */
__global__ void normalize_chebyshev(
    float * array,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
)
{
    uint gidx = blockDim.x * blockIdx.x + threadIdx.x;
    uint gidy = blockDim.y * blockIdx.y + threadIdx.y;
    uint gidz = blockDim.z * blockIdx.z + threadIdx.z;
    if ((gidx >= 1) || (gidy >= Ny) || (gidz >= Nz)) return;

    float ff0=0.0f, ff1=0.0f, ff2=0.0f;
    float sum0=0.0f, sum1=0.0f, sum2=0.0f;
    float f0, f1, f2, x;
    for (int j=0; j < Nx; j++) {
        uint pos = (gidz*Ny + gidy)*Nx + j;
        float arr_val = array[pos];
        x = 2.0f*(j + 0.5f - Nx/2.0f)/Nx;
        f0 = 1.0f;
        f1 = x;
        f2 = (3.0f*x*x-1.0f);
        ff0 = ff0 + f0 * arr_val;
        ff1 = ff1 + f1 * arr_val;
        ff2 = ff2 + f2 * arr_val;
        sum0 += f0 * f0;
        sum1 += f1 * f1;
        sum2 += f2 * f2;
    }
    for (int j=0; j< Nx; j++) {
        uint pos = (gidz*Ny + gidy)*Nx + j;
        x = 2.0f*(j+0.5f-Nx/2.0f)/Nx;
        f0 = 1.0f;
        f1 = x;
        f2 = (3.0f*x*x-1.0f);
        array[pos] -= ff0*f0/sum0 + ff1*f1/sum1 + ff2*f2/sum2;
    }
}


// launched with (Nx, 1, Nz) threads
__global__ void vertical_mean(
    float * array,
    float* output,
    int Nx, // input/output number of columns
    int Ny, // input/output number of rows
    int Nz  // input/output depth
) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    uint z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= Nx) || (y >= 1) || (z >= Nz)) return;

    float m = 0.0f;
    for (uint i = 0; i < Ny; i++) {
        float s = array[(z * Ny + i) * Nx + x];
        m += (s - m)/(i+1);
    }
    output[z * Nx + x] = (float) m;
}

