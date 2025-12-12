#ifndef SRC_DTYPE
  #define SRC_DTYPE float
#endif
#ifndef DST_DTYPE
  #define DST_DTYPE float
#endif

#include <pyopencl-complex.h>

__kernel void transpose(__global SRC_DTYPE* src, __global DST_DTYPE* dst, int src_width, int src_height) {
    // coordinates for "dst"
    uint x = get_global_id(0);
    uint y = get_global_id(1);
    if ((x >= src_height) || (y >= src_width)) return;
    dst[y*src_height + x] = (DST_DTYPE) src[x*src_width + y];
}