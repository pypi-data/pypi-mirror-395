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
kernel void halftomo_prepare_sinogram(
    global float* sinogram,
    global float* weights,
    int n_angles,
    int n_x,
    int start_x,
    int end_x
) {
    uint x = get_global_id(0);
    uint i_angle = get_global_id(1);
    if (x < start_x || x > end_x || i_angle >= n_angles) return;
    sinogram[i_angle * n_x + x] *= weights[x - start_x];
}
