#include <cupy/complex.cuh>
typedef complex<float> complex64;


#ifndef SRC_DTYPE
  #define SRC_DTYPE float
#endif
#ifndef DST_DTYPE
  #define DST_DTYPE float
#endif

__global__ void transpose(SRC_DTYPE* src, DST_DTYPE* dst, int src_width, int src_height) {
    // coordinates for "dst"
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= src_height) || (y >= src_width)) return;
    dst[y*src_height + x] = (DST_DTYPE) src[x*src_width + y];
}