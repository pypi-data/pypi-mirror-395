import numpy as np
from scipy import sparse


class DetectorDistortionBase:

    def __init__(self, detector_full_shape_vh=(0, 0)):
        """This is the basis class.
        A simple identity transformation which has the only merit to show
        how it works.Reimplement this function to have more parameters for other
        transformations
        """
        self._build_full_transformation(detector_full_shape_vh)

    def transform(self, source_data, do_full=False):
        """performs the transformation"""

        if do_full:
            result = self.transformation_matrix_full @ source_data.flat
            result.shape = source_data.shape
        else:
            result = self.transformation_matrix @ source_data.flat
            result.shape = self.target_shape

        return result

    def _build_full_transformation(self, detector_full_shape_vh):
        """A simple identity.
        Reimplement this function to have more parameters for other
        transformations
        """

        self.detector_full_shape_vh = detector_full_shape_vh

        sz, sx = detector_full_shape_vh

        # A simple identity matrix in sparse coordinates format

        self.total_detector_npixs = detector_full_shape_vh[0] * detector_full_shape_vh[1]
        I_tmp = np.arange(self.total_detector_npixs)
        J_tmp = np.arange(self.total_detector_npixs)
        V_tmp = np.ones([self.total_detector_npixs], "f")

        coo_tmp = sparse.coo_matrix((V_tmp, (I_tmp, J_tmp)), shape=(sz * sx, sz * sx))

        csr_tmp = coo_tmp.tocsr()

        ## The following arrays  are kept for future usage
        ## when, according to the "sub_region" parameter of the moment,
        ## they will be used to extract a "slice" of them
        ## which will map an appropriate data region corresponding to "sub_region_source"
        ## to the target "sub_region" of the moment
        self.full_csr_data = csr_tmp.data
        self.full_csr_indices = csr_tmp.indices
        self.full_csr_indptr = csr_tmp.indptr

        ## This will be used to save time if the same sub_region argument is requested several time in a row
        self._status = None

    def get_adapted_subregion(self, sub_region_xz):
        if sub_region_xz is not None:
            start_x, end_x, start_z, end_z = sub_region_xz
        else:
            start_x = 0
            end_x = None
            start_z = 0
            end_z = None

        (start_x, end_x, start_z, end_z) = self.set_sub_region_transformation((start_x, end_x, start_z, end_z))
        return (start_x, end_x, start_z, end_z)

    def set_sub_region_transformation(self, target_sub_region=None):
        """must return a source sub_region. It sets internally  an object (a practical implementation
        would be a sparse matrice) which can be reused in further applications of "transform" method
        for transforming the source sub_region data into the target sub_region
        """
        if target_sub_region is None:
            target_sub_region = (None, None, 0, None)

        if self._status is not None and self._status["target_sub_region"] == target_sub_region:
            return self._status["source_sub_region"]
        else:
            self._status = None
            return self._set_sub_region_transformation(target_sub_region)

    def set_full_transformation(self):
        self._set_sub_region_transformation(do_full=True)

    def get_actual_shapes_source_target(self):
        if self._status is None:
            return None, None
        else:
            return self._status["source_sub_region"], self._status["target_sub_region"]

    def _set_sub_region_transformation(self, target_sub_region=None, do_full=False):
        """to be reimplemented in the derived classes"""
        if target_sub_region is None or do_full:
            target_sub_region = (None, None, 0, None)

        (x_start, x_end, z_start, z_end) = target_sub_region

        if z_start is None:
            z_start = 0
        if z_end is None:
            z_end = self.detector_full_shape_vh[0]

        if (x_start, x_end) not in [(None, None), (0, None), (0, self.detector_full_shape_vh[1])]:
            message = f""" In the base class DetectorDistortionBase only vertical slicing is accepted.
            The sub_region contained (x_start, x_end)={(x_start, x_end)} which would slice the 
            full horizontal size which is {self.detector_full_shape_vh[1]}
            """
            raise ValueError(message)

        x_start, x_end = 0, self.detector_full_shape_vh[1]

        row_ptr_start = z_start * self.detector_full_shape_vh[1]
        row_ptr_end = z_end * self.detector_full_shape_vh[1]

        indices_start = self.full_csr_indptr[row_ptr_start]
        indices_end = self.full_csr_indptr[row_ptr_end]

        indices_offset = self.full_csr_indptr[row_ptr_start]

        source_offset = target_sub_region[2] * self.detector_full_shape_vh[1]

        data_tmp = self.full_csr_data[indices_start:indices_end]
        indices_tmp = self.full_csr_indices[indices_start:indices_end] - source_offset
        indptr_tmp = self.full_csr_indptr[row_ptr_start : row_ptr_end + 1] - indices_offset

        target_size = (z_end - z_start) * self.detector_full_shape_vh[1]
        source_size = (z_end - z_start) * self.detector_full_shape_vh[1]

        tmp_transformation_matrix = sparse.csr_matrix(
            (data_tmp, indices_tmp, indptr_tmp), shape=(target_size, source_size)
        )

        if do_full:
            self.transformation_matrix_full = tmp_transformation_matrix
            return None
        else:
            self.transformation_matrix = tmp_transformation_matrix

        self.target_shape = ((z_end - z_start), self.detector_full_shape_vh[1])

        ## For the identity matrix the source and the target have the same size.
        ## The two following lines are trivial.
        ## For this identity transformation only the slicing of the appropriate part
        ## of the identity sparse matrix is slightly laborious.
        ## Practical case will be more complicated and source_sub_region
        ## will be in general larger than the target_sub_region
        self._status = {
            "target_sub_region": ((x_start, x_end, z_start, z_end)),
            "source_sub_region": ((x_start, x_end, z_start, z_end)),
        }

        return self._status["source_sub_region"]


class DetectorDistortionMapsXZ(DetectorDistortionBase):
    def __init__(self, map_x, map_z):
        """
        This class implements the distortion correction from the knowledge of
        two arrays, map_x and map_z.
        Pixel (i,j) of the corrected image is obtained by interpolating the raw data at position
        ( map_z(i,j), map_x(i,j) ).

        Parameters
        ----------
            map_x : float 2D array
            map_z : float 2D array
        """

        self._build_full_transformation(map_x, map_z)

    def _build_full_transformation(self, map_x, map_z):
        detector_full_shape_vh = map_x.shape
        if detector_full_shape_vh != map_z.shape:
            message = f"""  map_x and map_z must have the same shape
            but the dimensions were {map_x.shape} and {map_z.shape}
            """
            raise ValueError(message)

        coordinates = np.array([map_z, map_x])

        # padding
        sz, sx = detector_full_shape_vh
        # total_detector_npixs = sz * sx
        xs = np.clip(np.array(coordinates[1].flat), [[0]], [[sx - 1]])
        zs = np.clip(np.array(coordinates[0].flat), [[0]], [[sz - 1]])

        ix0s = np.floor(xs)
        ix1s = np.ceil(xs)
        fx = xs - ix0s

        iz0s = np.floor(zs)
        iz1s = np.ceil(zs)
        fz = zs - iz0s

        I_tmp = np.empty([4 * sz * sx], np.int64)
        J_tmp = np.empty([4 * sz * sx], np.int64)
        V_tmp = np.ones([4 * sz * sx], "f")

        I_tmp[:] = np.arange(sz * sx * 4) // 4

        J_tmp[0::4] = iz0s * sx + ix0s
        J_tmp[1::4] = iz0s * sx + ix1s
        J_tmp[2::4] = iz1s * sx + ix0s
        J_tmp[3::4] = iz1s * sx + ix1s

        V_tmp[0::4] = (1 - fz) * (1 - fx)
        V_tmp[1::4] = (1 - fz) * fx
        V_tmp[2::4] = fz * (1 - fx)
        V_tmp[3::4] = fz * fx

        self.detector_full_shape_vh = detector_full_shape_vh

        coo_tmp = sparse.coo_matrix((V_tmp.astype("f"), (I_tmp, J_tmp)), shape=(sz * sx, sz * sx))

        csr_tmp = coo_tmp.tocsr()

        self.full_csr_data = csr_tmp.data
        self.full_csr_indices = csr_tmp.indices
        self.full_csr_indptr = csr_tmp.indptr

        ## This will be used to save time if the same sub_region argument is requested several time in a row
        self._status = None

    def _set_sub_region_transformation(
        self,
        target_sub_region=(
            (
                None,
                None,
                0,
                0,
            ),
        ),
        do_full=False,
    ):
        if target_sub_region is None or do_full:
            target_sub_region = (None, None, 0, None)

        (x_start, x_end, z_start, z_end) = target_sub_region

        if z_start is None:
            z_start = 0
        if z_end is None:
            z_end = self.detector_full_shape_vh[0]

        if (x_start, x_end) not in [(None, None), (0, None), (0, self.detector_full_shape_vh[1])]:
            message = f""" In the base class DetectorDistortionRotation only vertical slicing is accepted.
            The sub_region contained (x_start, x_end)={(x_start, x_end)} which would slice the 
            full horizontal size which is {self.detector_full_shape_vh[1]}
            """
            raise ValueError(message)

        x_start, x_end = 0, self.detector_full_shape_vh[1]

        row_ptr_start = z_start * self.detector_full_shape_vh[1]
        row_ptr_end = z_end * self.detector_full_shape_vh[1]

        indices_start = self.full_csr_indptr[row_ptr_start]
        indices_end = self.full_csr_indptr[row_ptr_end]

        data_tmp = self.full_csr_data[indices_start:indices_end]

        target_offset = self.full_csr_indptr[row_ptr_start]
        indptr_tmp = self.full_csr_indptr[row_ptr_start : row_ptr_end + 1] - target_offset

        indices_tmp = self.full_csr_indices[indices_start:indices_end]

        iz_source = (indices_tmp) // self.detector_full_shape_vh[1]

        z_start_source = iz_source.min()
        z_end_source = iz_source.max() + 1
        source_offset = z_start_source * self.detector_full_shape_vh[1]
        indices_tmp = indices_tmp - source_offset

        target_size = (z_end - z_start) * self.detector_full_shape_vh[1]
        source_size = (z_end_source - z_start_source) * self.detector_full_shape_vh[1]

        tmp_transformation_matrix = sparse.csr_matrix(
            (data_tmp, indices_tmp, indptr_tmp), shape=(target_size, source_size)
        )

        if do_full:
            self.transformation_matrix_full = tmp_transformation_matrix
            return None
        else:
            self.transformation_matrix = tmp_transformation_matrix

        self.target_shape = ((z_end - z_start), self.detector_full_shape_vh[1])

        ## For the identity matrix the source and the target have the same size.
        ## The two following lines are trivial.
        ## For this identity transformation only the slicing of the appropriate part
        ## of the identity sparse matrix is slightly laborious.
        ## Practical case will be more complicated and source_sub_region
        ## will be in general larger than the target_sub_region
        self._status = {
            "target_sub_region": ((x_start, x_end, z_start, z_end)),
            "source_sub_region": ((x_start, x_end, z_start_source, z_end_source)),
        }
        return self._status["source_sub_region"]
