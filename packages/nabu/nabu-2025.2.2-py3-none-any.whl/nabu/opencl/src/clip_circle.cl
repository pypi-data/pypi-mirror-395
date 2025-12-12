static inline int is_in_circle(float x, float y, float center_x, float center_y, int radius2) {
    return (((x - center_x)*(x - center_x) + (y - center_y)*(y - center_y)) <= radius2);
}


kernel void clip_circle(
    global float* d_image,
    int Nx,
    int Ny,
    float center_x,
    float center_y,
    float clip_circle_value
) {

    int x = get_global_id(0);
    int y = get_global_id(1);

    if ((x >= Nx) || (y >= Ny)) return;

    int radius2 = min(Nx/2, Ny/2);
    radius2 *= radius2;

    if (!is_in_circle(x, y, center_x, center_y, radius2)) {
        d_image[y * Nx + x] = clip_circle_value;
    }
}