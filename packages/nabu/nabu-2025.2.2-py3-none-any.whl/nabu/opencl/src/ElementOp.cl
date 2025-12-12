#include <pyopencl-complex.h>
typedef cfloat_t complex;

__kernel void cpy2d(
    __global float* dst,
    __global float* src,
    int dst_width,
    int src_width,
    int2 dst_offset,
    int2 src_offset,
    int2 transfer_shape)
{
    int gidx = get_global_id(0), gidy = get_global_id(1);
    if (gidx < transfer_shape.x && gidy < transfer_shape.y) {
        dst[(dst_offset.y + gidy)*dst_width + (dst_offset.x + gidx)] = src[(src_offset.y + gidy)*src_width + (src_offset.x + gidx)];
    }
}


// arr2D *= arr1D (line by line, i.e along fast dim)
__kernel void inplace_complex_mul_2Dby1D(__global complex* arr2D, __global complex* arr1D, int width, int height) {
    int x = get_global_id(0);
    int y = get_global_id(1);
    if ((x >= width) || (y >= height)) return;
    size_t i = y*width + x;
    arr2D[i] = cfloat_mul(arr2D[i], arr1D[x]);
}

// arr3D *= arr1D (along fast dim)
__kernel void inplace_complex_mul_3Dby1D(__global complex* arr3D, __global complex* arr1D, int width, int height, int depth) {
    int x = get_global_id(0);
    int y = get_global_id(1);
    int z = get_global_id(2);
    if ((x >= width) || (y >= height) || (z >= depth)) return;
    size_t i = (z*height + y)*width + x;
    arr3D[i] = cfloat_mul(arr3D[i], arr1D[x]);
}

