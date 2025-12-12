/*
"""
    Algorithm by Jonas Graetz.
    Submitted for publication.

    Please cite :
       reference to be added...



    # Generalized Hierarchical Backprojection (GHBP)
    # for fast tomographic reconstruction from ultra high resolution images at non-negligible fan angles.
    #
    # Authors/Contributions:
    # - Jonas Graetz, Fraunhofer IIS / Universitat Wurzburg: Algorithm Design and original OpenCL/Python implementation.
    # - Alessandro Mirone, ESRF: CUDA translation, ESRF / BM18 integration, testing <mirone@esrf.fr>
    # - Pierre Paleo, ESRF: ESRF / BM18 integration, testing <pierre.paleo@esrf.fr>
    #
    # JG was funded by the German Federal Ministry of Education and Research (BMBF), grant 05E2019,
    # funding the development of BM18 at ESRF in collaboration with the Fraunhofer Gesellschaft,
    # the Julius-Maximilians-Universitat Wurzburg, and the University of Passau

"""
 */

__device__ float3 operator-(const float3& a, const float3& b)
{
  return make_float3(a.x - b.x, a.y - b.y, a.z - b.z);
}
__device__ float dot(const float3& a, const float3& b)
{
  return a.x * b.x + a.y * b.y + a.z * b.z;
}
__device__ float dot4(const float4& a, const float4& b)
{
  return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w;
}

inline __device__ int is_in_circle(float x, float y, float center_x, float center_y, int radius2)
{
  return (((x - center_x) * (x - center_x) + (y - center_y) * (y - center_y)) <=
          radius2);
}
__global__ void clip_outer_circle(float* slice, int ny, int nx)
{
  const int tiy = threadIdx.y;
  const int bidy = blockIdx.y;
  int iy = (bidy * blockDim.y + tiy);

  const int tix = threadIdx.x;
  const int bidx = blockIdx.x;
  int ix = (bidx * blockDim.x + tix);

  float center_x = (nx - 1) / 2.0f, center_y = (ny - 1) / 2.0f;
  int radius2 = min(nx / 2, ny / 2);
  radius2 *= radius2;

  if (ix < nx && iy < ny) {
    if (!is_in_circle(ix, iy, center_x, center_y, radius2)) {
      slice[iy * nx + ix] = 0.0f;
    }
  }
}

__device__ float bilinear(float* data, int width, int height, float x, float y)
{
  int ix0 = (int)floorf(x);
  int iy0 = (int)floorf(y);
  float fx = x - ix0;
  float fy = y - iy0;

  int ix1 = ix0 + 1;
  int iy1 = iy0 + 1;

  ix0 = min(width - 1, max(0, ix0));
  ix1 = min(width - 1, max(0, ix1));
  iy0 = min(height - 1, max(0, iy0));
  iy1 = min(height - 1, max(0, iy1));

  float v00 = data[iy0 * width + ix0];
  float v01 = data[iy0 * width + ix1];
  float v10 = data[iy1 * width + ix0];
  float v11 = data[iy1 * width + ix1];

  return (v00 * (1 - fx) + v01 * fx) * (1 - fy) +
         (v10 * (1 - fx) + v11 * fx) * fy;
}

__global__ void backprojector(float* bpsetups,
              float* gridTransforms,
              int reductionFactor,
              int grid_width,
              int grid_height,
              int ngrids,
              float* grids,
              int sino_width,
              int sino_nangles,
              float scale_factor,
              float* sinogram,
              int projectionOffset)
{
  const int tix = threadIdx.x;
  const int bidx = blockIdx.x;
  int ix = (bidx * blockDim.x + tix);

  const int tiy = threadIdx.y;
  const int bidy = blockIdx.y;
  int iy = (bidy * blockDim.y + tiy);

  const int tiz = threadIdx.z;
  const int bidz = blockIdx.z;
  int iz = (bidz * blockDim.z + tiz);

  const int grid_px = ix;
  const int grid_py = iy;
  const int grid_i = iz;

  size_t grid_pos =
    (grid_i * ((size_t)grid_height) + grid_px) * ((size_t)grid_width) + grid_py;

  // if( grid_pos==0)   grids[grid_pos] = grid_height;
  // if( grid_pos==1)   grids[grid_pos] = grid_width;
  // if( grid_pos==2)   grids[grid_pos] = ngrids;
  // if( grid_pos==3)   printf(" CU %d   sino_nangles %d sino_width %d\n",
  // grid_height*  grid_width*  ngrids , sino_nangles, sino_width ) ;

  if ((grid_px < grid_height) && (grid_py < grid_width) && (grid_i < ngrids)) {
    const float3 grid_t1 = make_float3(gridTransforms[grid_i * 6 + 0],
                                       gridTransforms[grid_i * 6 + 1],
                                       gridTransforms[grid_i * 6 + 2]);
    const float3 grid_t2 = make_float3(gridTransforms[grid_i * 6 + 3 + 0],
                                       gridTransforms[grid_i * 6 + 3 + 1],
                                       gridTransforms[grid_i * 6 + 3 + 2]);

    const float4 final_p =
      make_float4(0.f,
                  grid_t1.x * grid_px + grid_t1.y * grid_py + grid_t1.z,
                  grid_t2.x * grid_px + grid_t2.y * grid_py + grid_t2.z,
                  1.f);

    float val = 0.f;
    int setup_i = 0;
    for (int k = 0; k < reductionFactor; k++) {
      setup_i = grid_i * reductionFactor + k + projectionOffset;
      if (setup_i < sino_nangles) // although the sinogram itself could be
                                  // read beyond extent, this is not true
                                  // for the setups-array!
      {
        int bi = setup_i * 4 * 3;
        const float4 ph = make_float4(bpsetups[bi + 0],
                                      bpsetups[bi + 1],
                                      bpsetups[bi + 2],
                                      bpsetups[bi + 3]);
        bi += 8;
        const float4 pw = make_float4(bpsetups[bi + 0],
                                      bpsetups[bi + 1],
                                      bpsetups[bi + 2],
                                      bpsetups[bi + 3]);

        const float n = 1.f / dot4(final_p, pw);
        const float h = dot4(final_p, ph) * n;

        int ih0 = (int)floorf(h);
        int ih1 = ih0 + 1;
        float fh = h - ih0;

        size_t sino_pos = setup_i * ((size_t)sino_width) + ih0;

        if (ih0 >= 0 && ih0 < sino_width) {
          // if(sino_pos>= sino_width*sino_nangles) printf(" problema
          // 1\n");
          val += sinogram[sino_pos] * (1 - fh);
        }
        if (ih1 >= 0 && ih1 < sino_width) {
          // if(sino_pos+1>= sino_width*sino_nangles) printf(" problema
          // 2 h ih0, ih1, sino_width , sino_nangles, setup_i %e  %e %e
          // %d %d %d %d %d\n", ray.x, ray.y, ray.z, ih0, ih1,
          // sino_width , sino_nangles, setup_i);
          val += sinogram[sino_pos + 1] * fh;
        }
      }
    }
    size_t grid_pos =
      (grid_i * ((size_t)grid_height) + grid_px) * ((size_t)grid_width) +
      grid_py;
    grids[grid_pos] = scale_factor * val;
  }
}

__global__ void aggregator(int do_sum,
           const float* newGridTransforms,
           const float* prevGridInverseTransforms,
           const int reductionFactor,
           int new_grid_width,
           int new_grid_height,
           int new_ngrids,
           float* newGrids,
           int prev_grid_width,
           int prev_grid_height,
           int prev_ngrids,
           float* prevGrids)
{
  const int tix = threadIdx.x;
  const int bidx = blockIdx.x;
  int ix = (bidx * blockDim.x + tix);

  const int tiy = threadIdx.y;
  const int bidy = blockIdx.y;
  int iy = (bidy * blockDim.y + tiy);

  const int tiz = threadIdx.z;
  const int bidz = blockIdx.z;
  int iz = (bidz * blockDim.z + tiz);

  const int new_grid_px = ix;
  const int new_grid_py = iy;
  const int new_grid_i = iz;

  if ((new_grid_px < new_grid_height) && (new_grid_py < new_grid_width) &&
      (new_grid_i < new_ngrids)) {
    const float3 new_grid_t1 =
      make_float3(newGridTransforms[new_grid_i * 6 + 0],
                  newGridTransforms[new_grid_i * 6 + 1],
                  newGridTransforms[new_grid_i * 6 + 2]);

    const float3 new_grid_t2 =
      make_float3(newGridTransforms[new_grid_i * 6 + 3 + 0],
                  newGridTransforms[new_grid_i * 6 + 3 + 1],
                  newGridTransforms[new_grid_i * 6 + 3 + 2]);

    const float3 final_p = make_float3(
      new_grid_t1.x * new_grid_px + new_grid_t1.y * new_grid_py + new_grid_t1.z,
      new_grid_t2.x * new_grid_px + new_grid_t2.y * new_grid_py + new_grid_t2.z,
      1.f);

    if (isnan(new_grid_t1.x)) {
      return; // inband-signaling for unused grids that shall be skipped
    }

    float val = 0.f;
    int prev_grid_i;
    float3 prev_grid_ti1, prev_grid_ti2;
    float3 prev_p_tex;
    for (int k = 0; k < reductionFactor; k++) {
      prev_grid_i = new_grid_i * reductionFactor + k;
      if (prev_grid_i < prev_ngrids) {
        prev_grid_ti1 =
          make_float3(prevGridInverseTransforms[prev_grid_i * 6 + 0],
                      prevGridInverseTransforms[prev_grid_i * 6 + 1],
                      prevGridInverseTransforms[prev_grid_i * 6 + 2]);

        prev_grid_ti2 =
          make_float3(prevGridInverseTransforms[prev_grid_i * 6 + 3 + 0],
                      prevGridInverseTransforms[prev_grid_i * 6 + 3 + 1],
                      prevGridInverseTransforms[prev_grid_i * 6 + 3 + 2]);

        if (isnan(prev_grid_ti1.x)) {
          break;
        }

        prev_p_tex = make_float3(dot(prev_grid_ti2, final_p),
                                 dot(prev_grid_ti1, final_p),
                                 (float)prev_grid_i);

        val += bilinear(prevGrids + prev_grid_i * ((size_t)prev_grid_height) *
                                      ((size_t)prev_grid_width),
                        prev_grid_width,
                        prev_grid_height,
                        prev_p_tex.x,
                        prev_p_tex.y);
      }
    }

    size_t new_grid_pos =
      (new_grid_i * ((size_t)new_grid_height) + new_grid_px) *
        ((size_t)new_grid_width) +
      new_grid_py;

    if (do_sum == 1) {
      newGrids[new_grid_pos] += val;
    } else {
      newGrids[new_grid_pos] = val;
    }
  }
}
