typedef unsigned int uint;
#define M_PI_F 3.141592653589793


__global__ void  joseph_projector(
    cudaTextureObject_t texSlice,
    float *d_Sino,
    int dimslice,
    int num_bins,
    float* angles_per_project,
    float axis_position,
    float* d_axis_corrections,
    int* d_beginPos,
    int* d_strideJoseph,
    int* d_strideLine,
    int num_projections,
    int dimrecx,
    int dimrecy,
    float offset_x,
    int josephnoclip,
    int normalize
) {
    uint tidx = threadIdx.x;
    uint bidx = blockIdx.x;
    uint tidy = threadIdx.y;
    uint bidy = blockIdx.y;

    float angle;
    float cos_angle, sin_angle ;

    __shared__  float corrections[16];
    __shared__  int beginPos[16*2];
    __shared__  int strideJoseph[16*2];
    __shared__  int strideLine[16*2];

    // thread will use corrections[tidy]
    // All are read by first warp
    int offset, OFFSET;
    switch(tidy) {
    case 0:
        corrections[tidx] = d_axis_corrections[bidy*16+tidx];
        break;
    case 1:
    case 2:
        offset = 16 * (tidy - 1);
        OFFSET = dimrecy * (tidy - 1);
        beginPos[offset + tidx] = d_beginPos[OFFSET+ bidy*16 + tidx];
        break;
    case 3:
    case 4:
        offset = 16 * (tidy - 3);
        OFFSET = dimrecy*(tidy - 3);
        strideJoseph[offset + tidx] = d_strideJoseph[OFFSET + bidy*16 + tidx];
        break;
    case 5:
    case 6:
        offset = 16*(tidy-5);
        OFFSET = dimrecy*(tidy-5);
        strideLine[offset + tidx] = d_strideLine[OFFSET + bidy*16 + tidx];
        break;
    }
    __syncthreads();

    angle = angles_per_project[bidy*16+tidy];
    cos_angle = cos(angle);
    sin_angle = sin(angle);

    if (fabs(cos_angle) > 0.70710678f) {
        if(cos_angle > 0) {
            cos_angle = cos(angle);
            sin_angle = sin(angle);
        }
        else {
            cos_angle = -cos(angle);
            sin_angle = -sin(angle);
        }
    }
    else {
        if (sin_angle > 0) {
            cos_angle = sin(angle);
            sin_angle = -cos(angle);
        }
        else {
            cos_angle = -sin(angle);
            sin_angle = cos(angle);
        }
    }
    float res=0.0f;
    float axis_corr = axis_position + corrections[tidy];
    float axis = axis_position;
    float xpix = (bidx*16 + tidx) - offset_x;
    float posx = axis * (1.0f - sin_angle/cos_angle) + (xpix - axis_corr)/cos_angle;

    float shiftJ = sin_angle/cos_angle;
    float x1 = fminf(-sin_angle/cos_angle, 0.f);
    float x2 = fmaxf(-sin_angle/cos_angle, 0.f);

    float Area;
    Area = 1.0f/cos_angle;
    int stlA, stlB, stlAJ, stlBJ;
    stlA = strideLine[16 + tidy];
    stlB = strideLine[tidy];
    stlAJ = strideJoseph[16 + tidy];
    stlBJ = strideJoseph[tidy];

    int beginA = beginPos[16 + tidy];
    int beginB = beginPos[tidy];
    float add;
    int l;

    if(josephnoclip) {
        for(int j=0; j<dimslice; j++) {
            x1 = beginA + posx*stlA + j*stlAJ + 1.5f;
            x2 = beginB + posx*stlB + j*stlBJ + 1.5f;
            add = tex2D<float>(texSlice, x1,x2);
            res += add;
            posx += shiftJ;
        }
    }
    else {
        for(int j=0; j<dimslice; j++) {
            x1 = beginA + posx*stlA + j*stlAJ + 1.5f;
            x2 = beginB + posx*stlB + j*stlBJ + 1.5f;
            l = (x1 >= 0.0f) * (x1 < (dimslice + 2)) * (x2 >= 0.0f) * (x2 < (dimslice + 2));
            add = tex2D<float>(texSlice, x1,x2);
            res += add * l;
            posx += shiftJ;
        }
    }

    if((bidy*16 + tidy) < num_projections && (bidx*16 + tidx) < num_bins) {
        res *= Area;
        if (normalize) res *= M_PI_F * 0.5f / num_projections;
        d_Sino[dimrecx*(bidy*16 + tidy) + (bidx*16 + tidx)] = res;
    }
}


