#include <cupy/complex.cuh>
typedef complex<float> complex64;

/**
    Damping kernel used in the Fourier-Wavelets sinogram destriping method.
*/
__global__ void kern_fourierwavelets(complex64* sinoF, int Nx, int Ny, float wsigma) {
    int gidx = threadIdx.x + blockIdx.x*blockDim.x;
    int gidy = threadIdx.y + blockIdx.y*blockDim.y;
    if (gidx >= Nx || gidy >= Ny) return;

    float m = gidy/wsigma;
    float factor = 1.0f - expf(-(m * m)/2);

    int tid = gidy*Nx + gidx;
    // do not forget the scale factor (here Ny)
    sinoF[tid] *= factor;
}
