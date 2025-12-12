#ifndef SHARED_SIZE
    #define SHARED_SIZE 256
#endif

texture<float, 2, cudaReadModeElementType> tex_projections;

__global__ void backproj_polar(
    float* d_slice,
    int num_projs,
    int num_bins,
    float axis_position,
    int n_x,
    int n_y,
    int offset_x,
    int offset_y,
    float* d_cos,
    float* d_msin,
    float scale_factor
)
{
    int i_r = offset_x + blockDim.x * blockIdx.x + threadIdx.x;
    int i_theta = offset_y + blockDim.y * blockIdx.y + threadIdx.y;

    float r = i_r - axis_position;
    float x = r * d_cos[i_theta];
    float y = - r * d_msin[i_theta];

    /*volatile*/ __shared__ float s_cos[SHARED_SIZE];
    /*volatile*/ __shared__ float s_msin[SHARED_SIZE];

    int next_fetch = 0;
    int tid = threadIdx.y * blockDim.x + threadIdx.x;

    float costheta, msintheta;
    float h1;
    float sum1 = 0.0f;

    for (int proj = 0; proj < num_projs; proj++) {
        if (proj == next_fetch) {
            // Fetch SHARED_SIZE values to shared memory
            __syncthreads();
            if (next_fetch + tid < num_projs) {
                s_cos[tid] = d_cos[next_fetch + tid];
                s_msin[tid] = d_msin[next_fetch + tid];
            }
            next_fetch += SHARED_SIZE;
            __syncthreads();
        }

        costheta = s_cos[proj - (next_fetch - SHARED_SIZE)];
        msintheta = s_msin[proj - (next_fetch - SHARED_SIZE)];
        float c1 = fmaf(costheta, x, axis_position); // cos(theta)*xr + axis_pos
        float s1 = fmaf(msintheta, y, 0.0f); // -sin(theta)*yr
        h1 = c1 + s1;
        if (h1 >= 0 && h1 < num_bins) sum1 += tex2D(tex_projections, h1 + 0.5f, proj + 0.5f);
    }


    // useful only if n_x < blocksize_x or n_y < blocksize_y
    if (i_r >= n_x) return;
    if (i_theta >= n_y) return;

    d_slice[i_theta*(n_x) + i_r] = sum1 * scale_factor;

}

