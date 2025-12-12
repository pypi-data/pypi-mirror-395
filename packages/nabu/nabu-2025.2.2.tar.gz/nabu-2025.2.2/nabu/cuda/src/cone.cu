/*
-----------------------------------------------------------------------
Copyright: 2010-2022, imec Vision Lab, University of Antwerp
           2014-2022, CWI, Amsterdam

Contact: astra@astra-toolbox.com
Website: http://www.astra-toolbox.com/

This file is part of the ASTRA Toolbox.


The ASTRA Toolbox is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ASTRA Toolbox is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the ASTRA Toolbox. If not, see <http://www.gnu.org/licenses/>.

-----------------------------------------------------------------------
*/


// static const unsigned int g_anglesPerWeightBlock = 16;
// static const unsigned int g_detBlockU = 32;
// static const unsigned int g_detBlockV = 32;


__global__ void devFDK_preweight(void* D_projData, unsigned int projPitch, unsigned int startAngle, unsigned int endAngle, float fSrcOrigin, float fDetOrigin, float fZShift, float fDetUSize, float fDetVSize, unsigned int iProjAngles, unsigned int iProjU, unsigned int iProjV)
{
    float* projData = (float*)D_projData;

    const uint angle = blockDim.y * blockIdx.y + threadIdx.y + startAngle;

    if (angle >= endAngle)
        return;

    // Astra FDK kernel used this indexing (with the appropriate grid)
    // const int detectorU = (blockIdx.x%((iProjU+g_detBlockU-1)/g_detBlockU)) * g_detBlockU + threadIdx.x;
    // const int startDetectorV = (blockIdx.x/((iProjU+g_detBlockU-1)/g_detBlockU)) * g_detBlockV;
    // Instead we choose a simpler scheme which does not assume pitch memory allocation

    const uint detectorU = blockDim.x * blockIdx.x + threadIdx.x;
    const int startDetectorV = 0;

    int endDetectorV = iProjV; // startDetectorV + g_detBlockV;
    // if (endDetectorV > iProjV)
        // endDetectorV = iProjV;
    if (detectorU >= iProjU) return;


    // We need the length of the central ray and the length of the ray(s) to
    // our detector pixel(s).

    const float fCentralRayLength = fSrcOrigin + fDetOrigin;

    const float fU = (detectorU - 0.5f*iProjU + 0.5f) * fDetUSize;

    const float fT = fCentralRayLength * fCentralRayLength + fU * fU;

    float fV = (startDetectorV - 0.5f*iProjV + 0.5f) * fDetVSize + fZShift;

    // Contributions to the weighting factors:
    // fCentralRayLength / fRayLength   : the main FDK preweighting factor
    // fSrcOrigin / (fDetUSize * fCentralRayLength)
    //                                  : to adjust the filter to the det width
    // pi / (2 * iProjAngles)           : scaling of the integral over angles

    const float fW2 = fCentralRayLength / (fDetUSize * fSrcOrigin);
    const float fW = fCentralRayLength * fW2 * (M_PI / 2.0f) / (float)iProjAngles;

    for (int detectorV = startDetectorV; detectorV < endDetectorV; ++detectorV)
    {
        const float fRayLength = sqrtf(fT + fV * fV);

        const float fWeight = fW / fRayLength;

        #ifndef RADIOS_LAYOUT
        projData[(detectorV*iProjAngles+angle)*projPitch+detectorU] *= fWeight;
        #else
        projData[(angle*iProjV+detectorV)*projPitch+detectorU] *= fWeight;
        #endif

        fV += fDetVSize;
    }
}