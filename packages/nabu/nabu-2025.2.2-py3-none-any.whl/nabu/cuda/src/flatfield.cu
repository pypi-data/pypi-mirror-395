#ifndef N_FLATS
    #error "Please provide the N_FLATS variable"
#endif

#ifndef N_DARKS
    #error "Please provide the N_FLATS variable"
#endif



/**
 * In-place flat-field normalization with linear interpolation.
 * This kernel assumes that all the radios are loaded into memory
 * (although not necessarily the full radios images)
 * and in radios[x, y z], z in the radio index
 *
 * radios: 3D array
 * flats: 3D array
 * darks: 3D array
 * Nx: number of pixel horizontally in the radios
 * Nx: number of pixel vertically in the radios
 * Nx: number of radios
 * flats_indices: indices of flats to fetch for each radio
 * flats_weights: weights of flats for each radio
 * darks_indices: indices of darks, in sorted order
 **/
__global__ void flatfield_normalization(
    float* radios,
    float* flats,
    float* darks,
    int Nx,
    int Ny,
    int Nz,
    int* flats_indices,
    float* flats_weights
) {
    size_t x = blockDim.x * blockIdx.x + threadIdx.x;
    size_t y = blockDim.y * blockIdx.y + threadIdx.y;
    size_t z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= Nx) || (y >= Ny) || (z >= Nz)) return;
    size_t pos = (z*Ny+y)*Nx + x;

    float dark_val = 0.0f, flat_val = 1.0f;

    #if N_FLATS == 1
        flat_val = flats[y*Nx + x];
    #else
        int prev_idx = flats_indices[z*2 + 0];
        int next_idx = flats_indices[z*2 + 1];
        float w1 = flats_weights[z*2 + 0];
        float w2 = flats_weights[z*2 + 1];
        if (next_idx == -1) {
            flat_val = flats[(prev_idx*Ny+y)*Nx + x];
        }
        else {
            flat_val = w1 * flats[(prev_idx*Ny+y)*Nx + x] + w2 * flats[(next_idx*Ny+y)*Nx + x];
        }

    #endif
    #if (N_DARKS == 1)
        dark_val = darks[y*Nx + x];
    #else
        // TODO interpolate between darks
        // Same as above...
        #error "N_DARKS > 1 is not supported yet"
    #endif

    float val = (radios[pos] - dark_val) / (flat_val - dark_val);

    #ifdef NAN_VALUE
    if (flat_val == dark_val) val = NAN_VALUE;
    #endif

    radios[pos] = val;
}
