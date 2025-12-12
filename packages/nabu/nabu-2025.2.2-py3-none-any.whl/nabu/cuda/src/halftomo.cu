/*
    Perform a "half tomography" sinogram conversion.
    A 360 degrees sinogram is converted to a 180 degrees sinogram with a
    field of view extended (at most) twice".
    *
    Parameters:
    * sinogram: the 360 degrees sinogram, shape (n_angles, n_x)
    * output: the 160 degrees sinogram, shape (n_angles/2, rotation_axis_position * 2)
    * weights: an array of weight, size n_x - rotation_axis_position
*/
__global__ void halftomo_kernel(
    float* sinogram,
    float* output,
    float* weights,
    int n_angles,
    int n_x,
    int rotation_axis_position
) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;

    int n_a2 = (n_angles + 1) / 2;
    int d = n_x - rotation_axis_position;
    int n_x2  = 2 * rotation_axis_position;
    int r = rotation_axis_position;

    if ((x >= n_x2) || (y >= n_a2)) return;

    // output[:, :r - d] = sino[:n_a2, :r - d]
    if (x < r - d) {
        output[y * n_x2 + x] = sinogram[y * n_x + x];
    }

    // output[:, r-d:r+d] = (1 - weights) * sino[:n_a2, r-d:]
    else if (x < r+d) {
        float w = weights[x - (r - d)];
        output[y * n_x2 + x] = (1.0f - w) * sinogram[y*n_x + x] \
                                   + w * sinogram[(n_a2 + y)*n_x + (n_x2 - 1 - x)];
    }

    // output[:, nx:] = sino[n_a2:, ::-1][:, 2 * d :] = sino[n_a2:, -2*d-1:-n_x-1:-1]
    else {
        output[y * n_x2 + x] = sinogram[(n_a2 + y)*n_x + (n_x2 - 1 - x)];
    }

}



/*
    Multiply in-place a 360 degrees sinogram with weights.
    This kernel is used to prepare a sinogram to be backprojected using half-tomography geometry.
    One of the sides (left or right) is multiplied with weights.
    For example, if "r" is the center of rotation near the right side:
      sinogram[:, -overlap_width:] *= weights
    where overlap_width = 2*(n_x - 1 - r)

    This can still be improved when the geometry has horizontal translations.
    In this case, we should have "start_x" and "end_x" as arrays of size n_angles,
    i.e one varying (start_x, end_x) per angle.

    Parameters
    -----------
      * sinogram: array of size (n_angles, n_x): 360 degrees sinogram
      * weights: array of size (n_angles,): weights to apply on one side of the sinogram
      * n_angles: int: number of angles
      * n_x: int: horizontal size (number of pixels) of the sinogram
      * start_x: int: start x-position for applying the weights
      * end_x: int: end x-position for applying the weights (included!)

*/
__global__ void halftomo_prepare_sinogram(
    float* sinogram,
    float* weights,
    int n_angles,
    int n_x,
    int start_x,
    int end_x
) {
    size_t x = blockDim.x * blockIdx.x + threadIdx.x;
    size_t i_angle = blockDim.y * blockIdx.y + threadIdx.y;
    if (x < start_x || x > end_x || i_angle >= n_angles) return;
    sinogram[i_angle * n_x + x] *= weights[x - start_x];
}

