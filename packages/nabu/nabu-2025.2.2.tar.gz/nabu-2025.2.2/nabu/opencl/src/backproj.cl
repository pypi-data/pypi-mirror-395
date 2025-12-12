#ifndef SHARED_SIZE
    #define SHARED_SIZE 256
#endif


/*
  Linear interpolation on a 2D array, horizontally.
  This will return arr[y][x] where y is an int (exact access) and x is a float (linear interp horizontally)
*/
static inline float linear_interpolation(global float* arr, int Nx, float x, int y) {
    if (x < -0.5f || x > Nx - 0.5f) return 0.0f; // texture address mode BORDER (CLAMP_TO_EDGE continues with edge)
    int xm = (int) floor(x);
    int xp = (int) ceil(x);
    if ((xm == xp) || (xp >= Nx)) return arr[y*Nx+xm];
    else return (arr[y*Nx+xm] * (xp - x)) + (arr[y*Nx+xp] * (x - xm));
}



kernel void backproj(
    global float* d_slice,
    #ifdef USE_TEXTURES
    read_only image2d_t d_sino,
    #else
    global float* d_sino,
    #endif
    int num_projs,
    int num_bins,
    float axis_position,
    int n_x,
    int n_y,
    float offset_x,
    float offset_y,
    global float* d_cos,
    global float* d_msin,
    #ifdef DO_AXIS_CORRECTION
    global float* d_axis_corr,
    #endif
    float scale_factor,
    local float* shared2 // local mem
) {

    int x = get_global_id(0);
    int y = get_global_id(1);

    uint Gx = get_global_size(0);
    uint Gy = get_global_size(1);

    #ifdef USE_TEXTURES
    const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP | CLK_FILTER_LINEAR;
    #endif

    // (xr, yr)    (xrp, yr)
    // (xr, yrp)   (xrp, yrp)
    float xr = (x + offset_x) - axis_position, yr = (y + offset_y) - axis_position;
    float xrp = xr + Gx, yrp = yr + Gy;

    local float s_cos[SHARED_SIZE];
    local float s_msin[SHARED_SIZE];
    #ifdef DO_AXIS_CORRECTION
    local float s_axis[SHARED_SIZE];
    float axcorr;
    #endif

    int next_fetch = 0;
    int tid = get_local_id(1) * get_local_size(0) + get_local_id(0);

    float costheta, msintheta;
    float h1, h2, h3, h4;
    float sum1 = 0.0f, sum2 = 0.0f, sum3 = 0.0f, sum4 = 0.0f;

    for (int proj = 0; proj < num_projs; proj++) {
        if (proj == next_fetch) {
            // Fetch SHARED_SIZE values to shared memory
            barrier(CLK_LOCAL_MEM_FENCE);
            if (next_fetch + tid < num_projs) {
                s_cos[tid] = d_cos[next_fetch + tid];
                s_msin[tid] = d_msin[next_fetch + tid];
                #ifdef DO_AXIS_CORRECTION
                s_axis[tid] = d_axis_corr[next_fetch + tid];
                #endif
            }
            next_fetch += SHARED_SIZE;
            barrier(CLK_LOCAL_MEM_FENCE);
        }

        costheta = s_cos[proj - (next_fetch - SHARED_SIZE)];
        msintheta = s_msin[proj - (next_fetch - SHARED_SIZE)];
        #ifdef DO_AXIS_CORRECTION
        axcorr = s_axis[proj - (next_fetch - SHARED_SIZE)];
        #endif
        float c1 = fma(costheta, xr, axis_position); // cos(theta)*xr + axis_pos
        float c2 = fma(costheta, xrp, axis_position); // cos(theta)*(xr + Gx) + axis_pos
        float s1 = fma(msintheta, yr, 0.0f); // -sin(theta)*yr
        float s2 = fma(msintheta, yrp, 0.0f); // -sin(theta)*(yr + Gy)
        h1 = c1 + s1;
        h2 = c2 + s1;
        h3 = c1 + s2;
        h4 = c2 + s2;
        #ifdef DO_AXIS_CORRECTION
        h1 += axcorr;
        h2 += axcorr;
        h3 += axcorr;
        h4 += axcorr;
        #endif

        #ifdef USE_TEXTURES
        sum1 += read_imagef(d_sino, sampler, (float2) (h1 +0.5f,proj +0.5f)).x;
        sum2 += read_imagef(d_sino, sampler, (float2) (h2 +0.5f,proj +0.5f)).x;
        sum3 += read_imagef(d_sino, sampler, (float2) (h3 +0.5f,proj +0.5f)).x;
        sum4 += read_imagef(d_sino, sampler, (float2) (h4 +0.5f,proj +0.5f)).x;
        #else
        if (h1 >= 0 && h1 < num_bins) sum1 += linear_interpolation(d_sino, num_bins, h1, proj);
        if (h2 >= 0 && h2 < num_bins) sum2 += linear_interpolation(d_sino, num_bins, h2, proj);
        if (h3 >= 0 && h3 < num_bins) sum3 += linear_interpolation(d_sino, num_bins, h3, proj);
        if (h4 >= 0 && h4 < num_bins) sum4 += linear_interpolation(d_sino, num_bins, h4, proj);
        #endif
    }


    int write_topleft = 1, write_topright = 1, write_botleft = 1, write_botright = 1;

    // useful only if n_x < blocksize_x or n_y < blocksize_y
    if (x >= n_x) return;
    if (y >= n_y) return;

    // Pixels in top-left quadrant
    if (write_topleft) d_slice[y*(n_x) + x] = sum1 * scale_factor;

    // Pixels in top-right quadrant
    if ((Gx + x < n_x) && (write_topright)) {
        d_slice[y*(n_x) + Gx + x] = sum2 * scale_factor;
    }

    if (Gy + y < n_y) {
    // Pixels in bottom-left quadrant
        if (write_botleft)
            d_slice[(y+Gy)*(n_x) + x] = sum3 * scale_factor;
    // Pixels in bottom-right quadrant
        if ((Gx + x < n_x) && (write_botright))
            d_slice[(y+Gy)*(n_x) + Gx + x] = sum4 * scale_factor;
    }


}


