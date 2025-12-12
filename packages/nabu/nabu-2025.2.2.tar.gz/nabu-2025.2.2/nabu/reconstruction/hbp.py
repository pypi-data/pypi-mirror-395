# Generalized Hierarchical Backprojection (GHBP)
# for fast tomographic reconstruction from ultra high resolution images at non-negligible fan angles.
#
# Authors/Contributions:
# - Jonas Graetz, Fraunhofer IIS / Universität Würzburg: Algorithm Design and original OpenCL/Python implementation.
# - Alessandro Mirone, ESRF: CUDA translation, ESRF / BM18 integration, testing <mirone@esrf.fr>
# - Pierre Paleo, ESRF: ESRF / BM18 integration, testing <pierre.paleo@esrf.fr>
#
# JG was funded by the German Federal Ministry of Education and Research (BMBF), grant 05E2019,
# funding the development of BM18 at ESRF in collaboration with the Fraunhofer Gesellschaft,
# the Julius-Maximilians-Universität Würzburg, and the University of Passau

import math
import numpy as np

from ..utils import get_cuda_srcfile
from ..cuda.processing import __has_cupy__

if __has_cupy__:
    from ..cuda.kernel import CudaKernel
    from .sinogram_cuda import CudaSinoMult
    from .fbp import CudaBackprojector

    __have_hbp__ = True
else:
    __have_hbp__ = False


def buildConebeamGeometry(
    anglesRad, rotAxisProjectionFromLeftPixelUnits, sourceSampleDistanceVoxelUnits, opticalAxisFromLeftPixelUnits=None
):
    """Generate fanbeam/conebeam projection matrices (as required by the backprojector) based on geometry parameters"""
    if opticalAxisFromLeftPixelUnits is None:
        if hasattr(rotAxisProjectionFromLeftPixelUnits, "__iter__"):
            opticalAxisFromLeftPixelUnits = rotAxisProjectionFromLeftPixelUnits[0]
        else:
            opticalAxisFromLeftPixelUnits = rotAxisProjectionFromLeftPixelUnits

    t = opticalAxisFromLeftPixelUnits
    d = sourceSampleDistanceVoxelUnits

    if hasattr(rotAxisProjectionFromLeftPixelUnits, "__iter__"):
        P_list = [
            np.array([[0, -t / d, 1, a], [1, 0, 0, 0], [0, -1 / d, 0, 1]], dtype=np.float64)  # pylint: disable=E1130
            for a in rotAxisProjectionFromLeftPixelUnits
        ]
    else:
        a = rotAxisProjectionFromLeftPixelUnits
        P_list = [
            np.array([[0, -t / d, 1, a], [1, 0, 0, 0], [0, -1 / d, 0, 1]], dtype=np.float64)  # pylint: disable=E1130
        ] * len(anglesRad)

    R = lambda w: np.array(
        [[1, 0, 0, 0], [0, np.cos(w), np.sin(w), 0], [0, -np.sin(w), np.cos(w), 0], [0, 0, 0, 1]], dtype=np.float64
    )
    return np.array([P @ R(-w) for P, w in zip(P_list, anglesRad)])


class HierarchicalBackprojector(CudaBackprojector):
    kernel_filename = "hierarchical_backproj.cu"

    def _init_geometry(self, sino_shape, slice_shape, angles, rot_center, halftomo, slice_roi):
        super()._init_geometry(sino_shape, slice_shape, angles, rot_center, halftomo, slice_roi)
        # pylint: disable=E1130 # -angles because different convention for the rotation direction
        self.angles = -self.angles

        # to do the reconstruction in reduction_steps steps
        self.reduction_steps = self.extra_options.get("hbp_reduction_steps", 2)
        reduction_factor = math.ceil((sino_shape[-2]) ** (1 / self.reduction_steps))

        # TODO customize
        axis_source_meters = 1.0e9
        voxel_size_microns = 1.0
        #

        axis_cor = self.extra_options.get("axis_correction", None)
        if axis_cor is None:
            axis_cor = 0
        bpgeometry = buildConebeamGeometry(
            self.angles, self.rot_center + axis_cor, 1.0e6 * axis_source_meters / voxel_size_microns
        )
        self.setup_hbp(bpgeometry, reductionFactor=reduction_factor, legs=self.extra_options.get("hbp_legs", 4))

    def setup_hbp(
        self,
        bpgeometry,
        reductionFactor=20,
        grid_wh_factors=(1, 1),
        fac=1,
        legs=4,
    ):

        # This implementation seems not to use textures
        self._use_textures = False

        # for the non texture implementation, this big number will discard texture limitations
        large_factor_for_non_texture_memory_access = 2**10
        # TODO: read limits from device info.
        self.GPU_MAX_GRIDSIZE = 2**15 * large_factor_for_non_texture_memory_access
        self.GPU_MAX_GRIDS = 2**11 * large_factor_for_non_texture_memory_access

        if self.sino_shape[0] != len(bpgeometry):
            raise ValueError("self.sino_shape[0] != len(bpgeometry)")
        if self.sino_shape[0] != len(self.angles):
            raise ValueError("self.sino_shape[0] != len(self.angles)")

        if self.sino_shape[1] > self.GPU_MAX_GRIDSIZE:
            raise ValueError(f"self.sino_shape[1] > {self.GPU_MAX_GRIDSIZE} not supported by GPU")
        if self.sino_shape[0] > self.GPU_MAX_GRIDSIZE:
            raise ValueError(f"self.sino_shape[0] > {self.GPU_MAX_GRIDSIZE} currently not supported")

        self.reductionFactor = reductionFactor
        self.legs = legs

        self.bpsetupsH = bpgeometry.astype(np.float32)
        # self.bpsetupsD = cuda.mem_alloc(self.bpsetupsH.nbytes)
        # cuda.memcpy_htod(self.bpsetupsD, self.bpsetupsH)
        self.bpsetupsD = self._processing.to_device("bpsetupsD", self.bpsetupsH)

        # if allocate_cuda_sinogram:
        #     self.sinogramD = cuda.mem_alloc(self.sino_shape[0] * self.sino_shape[1] * self.float_size)
        # else:
        #     self.sinogramD = None
        self.sinogramD = None

        self.whf = grid_wh_factors
        if self.sino_shape[1] * 2 * self.whf[0] * fac > self.GPU_MAX_GRIDSIZE:
            print(f"WARNING: gridsampling limited to {self.GPU_MAX_GRIDSIZE}")
            self.whf[0] = self.GPU_MAX_GRIDSIZE / (self.sino_shape[1] * 2 * fac)

        ###############################################
        ########## create intermediate grids ##########
        ###############################################

        self.reductionFactors = []
        self.grids = []  # shapes
        self.gridTransforms = []  # grid-to-world
        self.gridInvTransforms = []  # world-to-grid
        self.gridTransformsH = []  # host buffer
        self.gridTransformsD = []  # device buffer

        ### first level grid: will receive backprojections #
        ####################################################

        N = self.slice_shape[1] * fac

        angularRange = abs(np.ptp(self.angles)) / self.sino_shape[0] * reductionFactor

        ngrids = math.ceil(self.sino_shape[0] / reductionFactor)

        grid_width = int(
            np.rint(2 * N * self.whf[0])
        )  # double sampling to account/compensate for diamond shaped grid of ray-intersections
        grid_height = math.ceil(
            angularRange * N * self.whf[1]
        )  # small-angle approximation, generates as much "lines" as needed to account for all intersection levels

        m = (len(self.angles) // reductionFactor) * reductionFactor
        # TODO: improve angle calculation for more general cases
        tmpangles = np.angle(
            np.average(np.exp(1.0j * self.angles[:m].reshape(m // reductionFactor, reductionFactor)), axis=1)
        )

        tmpangles = np.concatenate((tmpangles, (np.angle(np.average(np.exp(1.0j * self.angles[m:]))),)))[:ngrids]
        gridAinvT = self._getAinvT(N, grid_height, grid_width)
        setupRs = self._getRotationMatrices(tmpangles)

        pad = int(math.ceil(ngrids / legs) * legs - ngrids)  # add nan-padding for inline-signaling of unused grids
        self.gridTransforms += [
            np.array(
                [(R @ gridAinvT) for R in setupRs] + [np.ones((3, 3), np.float32) * math.nan] * pad, dtype=np.float32
            )
        ]
        self.gridInvTransforms += [np.array([np.linalg.inv(t) for t in self.gridTransforms[-1]], dtype=np.float32)]
        self.grids += [(grid_height, grid_width, math.ceil(ngrids / legs))]
        self.reductionFactors += [reductionFactor]

        ### intermediate level grids: accumulation grids ###
        ####################################################

        # Actual iteration count typically within 1-5. Cf. break condition
        for i in range(100):
            # for a reasonable (with regard to memory requirement) grid-aspect ratio in the intermediate levels,
            # the covered angular range per grid should not exceed 28.6°, i.e.,
            # fewer than 7 (6.3) or 13 (12.6)  grids for a 180° / 360° scan is not reasonable
            if math.ceil(ngrids / reductionFactor) < 20:
                break
            angularRange *= reductionFactor
            ngrids = math.ceil(ngrids / reductionFactor)

            grid_height = math.ceil(
                angularRange * N * self.whf[1]
            )  # implicit small angle approximation, whose validity is
            # asserted by the preceding "break"
            gridAinvT = self._getAinvT(N, grid_height, grid_width)

            prevAngles = tmpangles
            m = (len(prevAngles) // reductionFactor) * reductionFactor
            # TODO: improve angle calculation for more general cases
            tmpangles = np.angle(
                np.average(np.exp(1.0j * prevAngles[:m].reshape(m // reductionFactor, reductionFactor)), axis=1)
            )
            tmpangles = np.concatenate((tmpangles, (np.angle(np.average(np.exp(1.0j * prevAngles[m:]))),)))[:ngrids]
            setupRsRed = self._getRotationMatrices(tmpangles)

            pad = int(math.ceil(ngrids / legs) * legs - ngrids)
            self.gridTransforms += [
                np.array(
                    [(R @ gridAinvT) for R in setupRsRed] + [np.ones((3, 3), np.float32) * math.nan] * pad,
                    dtype=np.float32,
                )
            ]
            self.gridInvTransforms += [np.array([np.linalg.inv(t) for t in self.gridTransforms[-1]], dtype=np.float32)]
            self.grids += [(grid_height, grid_width, math.ceil(ngrids / legs))]
            self.reductionFactors += [reductionFactor]

        ##### final accumulation grid #################
        ###############################################

        reductionFactor = ngrids
        ngrids = 1
        grid_size = self.slice_shape[1]
        grid_width = grid_size
        grid_height = grid_size

        # gridAinvT    = self._getAinvT(N, grid_height, grid_width)
        gridAinvT = self._getAinvT(N, grid_height, grid_width, 1 / fac)

        self.gridTransforms += [
            np.array([gridAinvT] * legs, dtype=np.float32)
        ]  # inflate transform list for convenience in reconstruction loop
        self.gridInvTransforms += [np.array([np.linalg.inv(t) for t in self.gridTransforms[-1]], dtype=np.float32)]
        self.grids += [(grid_height, grid_width, ngrids)]
        self.reductionFactors += [reductionFactor]

        #### accumulation grids #####
        self.gridTransformsD = []
        self.gridInvTransformsD = []
        self.gridsD = []

        max_grid_size = get_max_grid_size(self.grids)

        for i in range(len(self.grids)):
            gridTransformH = np.array(self.gridTransforms[i][:, :2, :3], dtype=np.float32, order="C").copy()
            gridInvTransformH = np.array(self.gridInvTransforms[i][:, :2, :3], dtype=np.float32, order="C").copy()
            self.gridTransformsD.append(self._processing.to_device("gridTransformsD%d " % i, gridTransformH.ravel()))
            self.gridInvTransformsD.append(
                self._processing.to_device("gridInvTransformsD%d" % i, gridInvTransformH.ravel())
            )

            if legs == 1 or i + 1 != (len(self.grids)):
                if i < 2:
                    self.gridsD.append(self._processing.allocate_array("gridsD%d" % i, max_grid_size))
                else:
                    self.gridsD.append(self.gridsD[i % 2])
            else:
                self.gridsD.append(self._processing.allocate_array("gridsD%d" % i, get_max_grid_size(self.grids[-1:])))

        self.imageBufferShape = (grid_size, grid_size)
        self.imageBufferD = self._processing.allocate_array(
            "imageBufferD", self.imageBufferShape[0] * self.imageBufferShape[1]
        )
        self.imageBufferH = np.zeros(self.imageBufferShape, dtype=np.float32)

    def _getAinvT(self, finalGridWidthAndHeight, currentGridHeight, currentGridWidth, scale=1):
        N = finalGridWidthAndHeight
        grid_height = currentGridHeight
        grid_width = currentGridWidth

        # shifts a texture coordinate from corner origin to center origin
        T = np.array(((1, 0, -0.5 * (grid_height - 1)), (0, 1, -0.5 * (grid_width - 1)), (0, 0, 1)), dtype=np.float32)
        # scales texture coordinates (of subsampled grid) into the unit/cooridnate system of a fully sampled grid
        Ainv = np.array(
            (((N - 1) / (grid_height - 1) * scale, 0, 0), (0, (N - 1) / (grid_width - 1) * scale, 0), (0, 0, 1)),
            dtype=np.float32,
        )
        return Ainv @ T

    def _getRotationMatrices(self, angles):
        return [
            np.array(((np.cos(a), np.sin(a), 0), (-np.sin(a), np.cos(a), 0), (0, 0, 1)), dtype=np.float32)
            for a in angles
        ]

    def _compile_kernels(self):
        # pylint: disable=E0606
        self.backprojector = CudaKernel(
            "backprojector",
            filename=get_cuda_srcfile(self.kernel_filename),
        )
        self.aggregator = CudaKernel("aggregator", filename=get_cuda_srcfile(self.kernel_filename))
        self.clip_outer_circle_kernel = CudaKernel("clip_outer_circle", filename=get_cuda_srcfile(self.kernel_filename))
        # Duplicate of fbp.py ...
        if self.halftomo and self.rot_center < self.dwidth:
            self.sino_mult = CudaSinoMult(self.sino_shape, self.rot_center)  # , ctx=self._processing.ctx)
        #

    def _set_sino(self, sino, do_checks=True):
        if do_checks and not (sino.flags.c_contiguous):
            raise ValueError("Expected C-Contiguous array")
        else:
            self._d_sino = self._processing.allocate_array("_d_sino", self.sino_shape)
            if id(self._d_sino) == id(sino):
                return
            self._d_sino[:] = sino[:]

    def backproj(self, sino, output=None, do_checks=True, reference=False):
        if self.halftomo and self.rot_center < self.dwidth:
            self.sino_mult.prepare_sino(sino)
        self._set_sino(sino)
        lws = (64, 4, 4)

        if reference:
            gws = getGridSize(self.grids[-1], lws)
            (grid_height, grid_width, ngrids) = self.grids[-1]

            self.backprojector(
                self.bpsetupsD,
                self.gridTransformsD[-1].gpudata,
                np.int32(self.sino_shape[0]),
                np.int32(grid_width),
                np.int32(grid_height),
                np.int32(ngrids),
                self.gridsD[-1],
                np.int32(self.sino_shape[1]),
                np.int32(self.sino_shape[0]),
                np.float32(self._backproj_scale_factor),
                self._d_sino,
                np.int32(0),  # offset
                block=lws,
                grid=gws,
            )

        else:
            for leg in list(range(self.legs)):
                gridOffset = leg * self.grids[0][2]
                projOffset = gridOffset * self.reductionFactors[0]
                gws = getGridSize(self.grids[0], lws)
                (grid_height, grid_width, ngrids) = self.grids[0]

                self.backprojector(
                    self.bpsetupsD,
                    self.gridTransformsD[0][6 * gridOffset :],
                    np.int32(self.reductionFactors[0]),
                    np.int32(grid_width),
                    np.int32(grid_height),
                    np.int32(ngrids),
                    self.gridsD[0],
                    np.int32(self.sino_shape[1]),
                    np.int32(self.sino_shape[0]),
                    np.float32(self._backproj_scale_factor),
                    self._d_sino,
                    np.int32(projOffset),
                    block=lws,
                    grid=gws,
                )

                for i in range(1, len(self.grids)):
                    if self.grids[i][2] >= 8:
                        lws = (16, 16, 4)
                    else:
                        lws = (32, 32, 1)

                    gws = getGridSize(self.grids[i], lws)

                    (new_grid_height, new_grid_width, new_ngrids) = self.grids[i]
                    (prev_grid_height, prev_grid_width, prev_ngrids) = self.grids[i - 1]

                    gridOffset = leg * self.grids[i][2]
                    prevGridOffset = leg * self.grids[i - 1][2]

                    self.aggregator(
                        np.int32((i + 1 == len(self.grids)) and (leg > 0)),
                        self.gridTransformsD[i][6 * gridOffset :],
                        self.gridInvTransformsD[i - 1][6 * prevGridOffset :],
                        np.int32(self.reductionFactors[i]),
                        np.int32(new_grid_width),
                        np.int32(new_grid_height),
                        np.int32(new_ngrids),
                        self.gridsD[i],
                        np.int32(prev_grid_width),
                        np.int32(prev_grid_height),
                        np.int32(prev_ngrids),
                        self.gridsD[i - 1],
                        block=lws,
                        grid=gws,
                    )

        if self.extra_options.get("clip_outer_circle", False):
            lws = (16, 16, 1)
            ny, nx = self.slice_shape
            gws = getGridSize((nx, ny, 1), lws)
            self.clip_outer_circle_kernel(self.gridsD[-1], np.int32(ny), np.int32(nx), block=lws, grid=gws)

        # FIXME pycuda fails to do a discontiguous memcpy for more than 2^31 bytes
        if self.gridsD[-1].nbytes > 2**31:
            r1d = self.gridsD[-1].get()
            r2d = np.ascontiguousarray(r1d.reshape(self.slice_shape))
            if output is not None:
                output[:] = r2d[:]
                return output
            else:
                return r2d
        # --------

        else:
            res = self.gridsD[-1].reshape(self.slice_shape)
            if isinstance(output, self.backend_processing_class.array_class):
                output[:] = res[:]
                return output
            else:
                return res.get(out=output)


def get_max_grid_size(grids):
    size_max = 0
    for dims in grids:
        size = 1
        for d in dims:
            size = size * d
        if size > size_max:
            size_max = size
    return size_max


def getGridSize(minimum, local):
    m, l = np.array(minimum), np.array(local)  # noqa: E741
    new = (m // l) * l
    new[new < m] += l[new < m]
    return tuple(map(int, new // l))
