# ruff: noqa
import math
import numpy as np
from ...resources.logger import LoggerOrPrint
from ...utils import DictToObj


class SpanStrategy:
    def __init__(
        self,
        z_pix_per_proj,
        x_pix_per_proj,
        detector_shape_vh,
        phase_margin_pix,
        projection_angles_deg,
        require_redundancy=False,
        pixel_size_mm=0.1,
        z_offset_mm=0.0,
        logger=None,
        angular_tolerance_steps=0.0,
    ):
        """
        This class does all the accounting for the reconstructible slices, giving for each one the list of the useful angles,
        of the vertical and horizontal shifts,and more ...

        Parameters
        ----------
        z_pix_per_proj : array of floats
            an array of floats with one entry per projection, in pixel units. The values are the vertical displacements of the detector.
            An decreasing z means that the rotation axis is following the positive direction of the detector  vertical axis, which is pointing toward the ground.
            In the experimental setup, the vertical detector axis is pointing toward the ground. Moreover the values are offsetted so that the
            first value is zero. The offset value, in millimiters is z_offset_mm and it is the vertical position of the sample stage relatively
            to the center of the detector. A negative z_offset_mm means that the sample stage is below the detector for the first projection, and this is almost
            always the case, because the sample is above the sample stage.
            A  z_pix=0 value indicates that  the translation-rotation stage "ground" is exactly at the beam height ( supposed to be near the central line of the detector)
            plus z_offset_mm.
            A positive z_pix means that the  translation   stage has been lowered, compared to the first projection, in order to scan higher parts of the sample.
            ( the sample is above the translation-rotation stage).
        x_pix_per_proj : array of floats
            one entry per projection. The horizontal displacement of the detector respect to  the rotation axis.
            A positive x means that the sample shadow on the detector is moving toward the left of the detector.
             (the detector is going right)
        detector_shape_vh : a tuple of two ints
            the vertical and horizontal dimensions
        phase_margin_pix : int
            the  maximum margin needed for the different kernels (phase, unsharp..) otherwhere in the pipeline
        projection_angles_deg :  array of floats
            per each projection the rotation angle of the sample in degree.
        require_redundancy: bool, optional, defaults to False
            It can be set  to True, when there are dead zones in the detector.
            In this case the minimal required angular span is increased from 360 to  2*360
            in order to enforce  the necessary redundancy, which allows the
            correction of the dead zones. The lines which do not satisfy this requirement are not doable.
        z_offset_mm: float
            the vertical position of the sample stage relatively to the center of the detector. A negative z_offset_mm means that the
            sample stage is below the detector for the first projection, and this is almost
            always the case, because the sample is above the sample stage.
        pixel_size_mm:  float, the pixel size in millimiters
           this value is used to give results in units of " millimeters above the sample stage"
           Althougth internally all is calculated in pixel units, it is useful to incorporate
           such information in the SpanStrategy object which will then be able to set up
           reconstruction information according to several request formats: be they in
           sequential number of reconstructible slices, or millimeters above the stage.
        angular_tolerance_steps: float, defaults to zero
             the angular tolerance, an angular width expressed in units of an angular step, which is tolerated in
             the criteria for deciding if a slice is reconstructable or not
        logger : a logger, optional
        """
        self.logger = LoggerOrPrint(logger)
        self.require_redundancy = require_redundancy
        self.z_pix_per_proj = z_pix_per_proj
        self.x_pix_per_proj = x_pix_per_proj
        self.detector_shape_vh = detector_shape_vh
        self.total_num_images = len(self.z_pix_per_proj)
        self.phase_margin_pix = phase_margin_pix
        self.pix_size_mm = pixel_size_mm
        self.z_offset_mm = z_offset_mm
        self.angular_tolerance_steps = angular_tolerance_steps

        # internally we use increasing angles, so that in all inequalities, that are used
        # to check the span, only such case has to be contemplated.
        # To do so, if needed, we change the sign of the angles.
        if projection_angles_deg[-1] > projection_angles_deg[0]:
            self.projection_angles_deg_internally = projection_angles_deg
            self.angles_are_inverted = False
        else:
            self.projection_angles_deg_internally = -projection_angles_deg
            self.angles_are_inverted = True
        self.projection_angles_deg = projection_angles_deg

        if (
            len(self.x_pix_per_proj) != self.total_num_images
            or len(self.projection_angles_deg_internally) != self.total_num_images
        ):
            message = f"""
            all the arguments z_pix_per_proj, x_pix_per_proj and projection_angles_deg
            must have the same lenght but their lenght were 
            {len(self.z_pix_per_proj) }, {len(self.x_pix_per_proj) }, {len(self.projection_angles_deg_internally) } respectively """

            raise ValueError(message)

        ## informations to be built are initialised to None here below
        """ For a given slice, the procedure for  obtaining the useful angles,  is based on the "sunshine" image,
        The sunshine image has two dimensions, the  second one is the projection number
        while the first runs over the heights of the slices.
        All the logic is based on this image: when a given pixel of this image  is zero, this corresponds
        to a pair   (height,projection)  for which there is no contribution of that projection to that slice.
        """
        self.sunshine_image = None

        """ This will be an array of integer heights. We use a  one-to-one correspondance beween these integers and slices 
         in the reconstructed volume.

         The value of a given item is the vertical coordinate of an horizontal line in in the dectector
         (or above or below (negative values) ). More precisely the line over which the corresponding slice gets projected 
         at the beginning of the scan ( in other words
         for the first  vertical translation entry of the z_pix_per_proj argument) 
         Illustratively, a view height equal to zero corresponds to 
         a slice which projects on row 0 when translation is given by the first value in self.z_pix_per_proj.
         Negative integers for the heights are possible too, according to the direction of translations, which may bring
         above or below the detector. ( Illustratively
         the values in z_pix_per_proj are alway positive for the simple fact that the sample is above
         the roto-translation stage and the stage must be lowered in height for the beam to hit the sample.
         A scan starts  always from a positive z_pix translation but the z_pix value may either decrease
         or increase. In fact for practical reasons, after having done a scan in one direction it is convenient to scan
         also while coming back after a previous scan)
        """
        self.total_view_heights = None

        """ A list wich will contain for every reconstructable heigth, listed in self.total_view_heights, and in the same order,
        a pair of two integer, the first is the first sequential number of the projection for which the height is projected
        inside the detector, the second integer is the last projection number for which the projection occurs inside the detector.
        """
        self.on_detector_projection_intervals = None

        """ All like self.on_detector_projection_intervals, but considering also the margins (phase, unsharp, etc).
        so that  the height is projected inside the detector but while keeping 
        a safe phase_margin_pix distance from the upper and lower border of the detector. 
        """
        self.within_margin_projection_intervals = None

        """ This will contain projection number i_pro, the integer value given by
            ceil(z_pix_per_proj[i_pro])
        This array, together with the here below array self.fract_complement_to_integer_shift_v
        will be used for cropping  when the data are collected for a given to be reconstructed chunk.
        """
        self.integer_shift_v = np.zeros([self.total_num_images], "i")

        """ The fractional vertical shifts are positive floats  < 1.0 pixels. 
        This is the fractional part which, added to self.integer_shift_v, 
        gives back  z_pix_per_proj.
        Together with integer_shift_v, this array is meant to be used, by other modules,  for cropping  
        when the data are collected for a given to be reconstructed chunk."""
        self.fract_complement_to_integer_shift_v = np.zeros([self.total_num_images], "f")

        self._setup_ephemerides()

        self._setup_sunshine()

    def get_doable_span(self):
        """return an object with two properties:
        view_heights_minmax: containing minimum and maximum doable height ( detector reference at iproj=0)
        z_pix_minmax       : containing minimum and maximum heights above the roto-translational sample stage
        """
        vertical_profile = self.sunshine_image.sum(axis=1)

        doable_indexes = np.arange(len(vertical_profile))[vertical_profile > 0]
        vertical_span = doable_indexes.min(), doable_indexes.max()

        if not (vertical_profile[vertical_span[0] : vertical_span[1] + 1] > 0).all():
            message = """ Something wrong occurred in the span preprocessing.
                          It appears that some intermetiade slices are not doables.
                          The doable span should instead be contiguous. Please signal the problem"""
            raise RuntimeError(message)

        view_heights_minmax = self.total_view_heights[list(vertical_span)]

        hmin, hmax = view_heights_minmax
        d_v, d_h = self.detector_shape_vh
        z_min, z_max = (-self.z_pix_per_proj[0] + (d_v - 1) / 2 - hmax, -self.z_pix_per_proj[0] + (d_v - 1) / 2 - hmin)
        res = {
            "view_heights_minmax": view_heights_minmax,
            "z_pix_minmax": (z_min, z_max),
            "z_mm_minmax": (z_min * self.pix_size_mm, z_max * self.pix_size_mm),
        }
        return DictToObj(res)

    def get_informative_string(self):
        doable_span_v = self.get_doable_span()
        if self.z_pix_per_proj[-1] >= self.z_pix_per_proj[-1]:
            direction = "ascending"
        else:
            direction = "descending"

        s = f"""
        Doable vertical span
        --------------------
             The scan has been performed with an {direction} vertical translation of the rotation axis.
              
             The detector vertical axis is up side down.

             Detector reference system at iproj=0:
                from vertical view height  ...   {doable_span_v.view_heights_minmax[0]}
                up to  (included)     ...   {doable_span_v.view_heights_minmax[1]}

                 The slice that projects to the first line of the first projection 
                 corresponds to vertical heigth = 0

             In voxels, the vertical doable span measures: {doable_span_v.z_pix_minmax[1] - doable_span_v.z_pix_minmax[0]}

             And in millimiters above the stage:
                 from vertical height above stage ( mm units)  ...   {doable_span_v.z_mm_minmax[0] - self.z_offset_mm }
                 up to  (included)                                ...  {doable_span_v.z_mm_minmax[1] - self.z_offset_mm }
        """
        return s

    def get_chunk_info(self, span_v_absolute):
        """

        This method returns an object containing all the information that are needed to reconstruct
        the corresponding chunk

            angle_index_span: a pair of integers indicating the start and the end of useful angles
                              in the array of all the scan angle self.projection_angles_deg
            span_v:  a pair of two integers indicating the start and end of the span relatively  to the lowest value
                     of array self.total_view_heights
            integer_shift_v: an array, containing for each one of the  useful projections of the span,
                             the integer part of vertical shift to be used in cropping,
            fract_complement_to_integer_shift_v :
                             the fractional remainder for cropping.
            z_pix_per_proj: an array, containing for each to be used projection of the span
                            the vertical shift
            x_pix_per_proj: ....the horizontal shit
            angles_rad    :    an array, for each useful projection of the chunk the angle in radian

        Parameters:
        -----------
          span_v_absolute: tuple of integers
             a pair of two integers
              the first  view height ( referred to the detector y axis at iproj=0)
              the second view height
              with the first height smaller than the second.
        """
        span_v = (span_v_absolute[0] - self.total_view_heights[0], span_v_absolute[1] - self.total_view_heights[0])

        sunshine_subset = self.sunshine_image[span_v[0] : span_v[1]]
        angular_profile = sunshine_subset.sum(axis=0)

        angle_indexes = np.arange(len(self.projection_angles_deg_internally))[angular_profile > 0]

        angle_index_span = angle_indexes.min(), angle_indexes.max() + 1
        if not (np.less(0, angular_profile[angle_index_span[0] : angle_index_span[1]]).all()):
            message = """ Something wrong occurred in the span preprocessing.
                          It appears that some intermediate slices are not doables.
                          The doable span should instead be contiguous. Please signal the problem"""
            raise RuntimeError(message)

        chunk_angles_deg = self.projection_angles_deg[angle_indexes]

        my_slicer = slice(angle_index_span[0], angle_index_span[1])
        values = (
            angle_index_span,
            span_v_absolute,
            self.integer_shift_v[my_slicer],
            self.fract_complement_to_integer_shift_v[my_slicer],
            self.z_pix_per_proj[my_slicer],
            self.x_pix_per_proj[my_slicer],
            np.deg2rad(chunk_angles_deg) * (1 - 2 * int(self.angles_are_inverted)),
        )

        key_names = (
            "angle_index_span",
            "span_v",
            "integer_shift_v",
            "fract_complement_to_integer_shift_v",
            "z_pix_per_proj",
            "x_pix_per_proj",
            "angles_rad",
        )

        return DictToObj(dict(zip(key_names, values)))

    def _setup_ephemerides(self):
        """
        A function which will set :

          * self.integer_shift_v
          * self.fract_complement_to_integer_shift_v
          * self.total_view_heights
          * self.on_detector_projection_intervals
          * self.within_margin_projection_intervals
        """

        for i_pro in range(self.total_num_images):
            trans_v = self.z_pix_per_proj[i_pro]
            self.integer_shift_v[i_pro] = math.ceil(trans_v)
            self.fract_complement_to_integer_shift_v[i_pro] = math.ceil(trans_v) - trans_v

        ## The two following line initialize the view height, then considering the vertical translation
        #  the filed of view will be expanded
        total_view_top = self.detector_shape_vh[0]
        total_view_bottom = 0

        total_view_top = max(total_view_top, int(math.ceil(total_view_top + self.z_pix_per_proj.max())))
        total_view_bottom = min(total_view_bottom, int(math.floor(total_view_bottom + self.z_pix_per_proj.min())))

        self.total_view_heights = np.arange(total_view_bottom, total_view_top + 1)

        ## where possible only data from within safe phase margin will be considered. (within_margin)
        ## if it is enough for 360 or more degree.
        ## If it is not enough we'll complete wih data close to the border, provided that data comes from within detector
        ## This will be
        ## the case for the first and last doable slices.
        self.within_margin_projection_intervals = np.zeros(self.total_view_heights.shape + (2,), "i")
        self.on_detector_projection_intervals = np.zeros(self.total_view_heights.shape + (2,), "i")

        self.on_detector_projection_intervals[:, 1] = 0  # empty intervals
        self.within_margin_projection_intervals[:, 1] = 0

        for i_h, height in enumerate(self.total_view_heights):
            previous_is_inside_detector = False
            previous_is_inside_margin = False

            pos_inside_filtered_v = height - self.integer_shift_v

            is_inside_detector = np.less_equal(0, pos_inside_filtered_v)
            is_inside_detector *= np.less(
                pos_inside_filtered_v, self.detector_shape_vh[0] - np.less(0, self.fract_complement_to_integer_shift_v)
            )

            is_inside_margin = np.less_equal(self.phase_margin_pix, pos_inside_filtered_v)
            is_inside_margin *= np.less(
                pos_inside_filtered_v,
                self.detector_shape_vh[0]
                - self.phase_margin_pix
                - np.less(0, self.fract_complement_to_integer_shift_v),
            )

            tmp = np.arange(self.total_num_images)[is_inside_detector]
            if len(tmp):
                self.on_detector_projection_intervals[i_h, :] = (tmp.min(), tmp.max())

            tmp = np.arange(self.total_num_images)[is_inside_detector]
            if len(tmp):
                self.within_margin_projection_intervals[i_h, :] = (tmp.min(), tmp.max())

    def _setup_sunshine(self):
        """It prepares

          * self.sunshine_image

        an image which for every height, contained in self.total_view_heights, and in the same order,
        contains the list of factors, one per every projection of the total list. Each  factor is a backprojection
        weight. A non-doable height corresponds to a line full of zeros.
        A doable height must correspond to a line having one and only one segment of contiguous non zero elements.
        """

        self.sunshine_image = np.zeros(self.total_view_heights.shape + (self.total_num_images,), "f")

        avg_angular_step_deg = np.diff(self.projection_angles_deg_internally).mean()

        projection_angles_for_interp = np.concatenate(
            [
                [self.projection_angles_deg_internally[0] - avg_angular_step_deg],
                self.projection_angles_deg_internally,
                [self.projection_angles_deg_internally[-1] + avg_angular_step_deg],
            ]
        )

        data_container_for_interp = np.zeros_like(projection_angles_for_interp)

        num_angular_periods = math.ceil(
            (self.projection_angles_deg_internally.max() - self.projection_angles_deg_internally.min()) / 360
        )

        for i_h, height in enumerate(self.total_view_heights):
            first_last_on_dect = self.on_detector_projection_intervals[i_h]
            first_last_within_margin = self.within_margin_projection_intervals[i_h]

            if first_last_on_dect[1] == 0:
                # this line never entered in the fov
                continue

            angle_on_dect_first_last = self.projection_angles_deg_internally[first_last_on_dect]
            angle_within_margin_first_last = self.projection_angles_deg_internally[first_last_within_margin]

            # a mask which is positive for angular positions for which the height i_h gets projected within the detector
            mask_on_dect = (
                np.less_equal(angle_on_dect_first_last[0], self.projection_angles_deg_internally)
                * np.less_equal(self.projection_angles_deg_internally, angle_on_dect_first_last[1])
            ).astype("f")

            # a mask which is positive for angular positions for which the height i_h gets projected within the margins
            mask_within_margin = (
                np.less_equal(angle_within_margin_first_last[0], self.projection_angles_deg_internally)
                * np.less_equal(self.projection_angles_deg_internally, angle_within_margin_first_last[1])
            ).astype("f")

            ## create a line which collects contributions from redundant angles
            detector_collector = np.zeros(self.projection_angles_deg_internally.shape, "f")
            margin_collector = np.zeros(self.projection_angles_deg_internally.shape, "f")

            # the following loop tracks, for each projection, the total weight available at the projection angle
            # The additional weight is coming from redundant angles.
            # In this sense the sunshine_image implements a first rudimentary reweighting,
            # which could be in principle used in the full pipeline, althought the regridded pipeline
            # implements a, better, reweighting o its own.
            for i_shift in range(-num_angular_periods, num_angular_periods + 1):
                signus = (
                    1 if (self.projection_angles_deg_internally[-1] > self.projection_angles_deg_internally[0]) else -1
                )

                data_container_for_interp[1:-1] = mask_on_dect

                detector_collector = detector_collector + mask_on_dect * np.interp(
                    (self.projection_angles_deg_internally + i_shift * 360) * signus,
                    signus * projection_angles_for_interp,
                    data_container_for_interp,
                    left=0,
                    right=0,
                )

                data_container_for_interp[1:-1] = mask_within_margin

                margin_collector = margin_collector + mask_within_margin * np.interp(
                    (self.projection_angles_deg_internally + i_shift * 360) * signus,
                    signus * projection_angles_for_interp,
                    data_container_for_interp,
                    left=0,
                    right=0,
                )

            detector_shined_angles = self.projection_angles_deg_internally[detector_collector > 0.99]
            margin_shined_angles = self.projection_angles_deg_internally[margin_collector > 0.99]

            if not len(detector_shined_angles) > 1:
                continue

            avg_step_deg = abs(avg_angular_step_deg)

            if len(margin_shined_angles):
                angular_span_safe_margin = (
                    margin_shined_angles.max()
                    - margin_shined_angles.min()
                    + avg_step_deg * (1.01 + self.angular_tolerance_steps)
                )
            else:
                angular_span_safe_margin = 0

            angular_span_bare_border = (
                detector_shined_angles.max()
                - detector_shined_angles.min()
                + avg_step_deg * (1.01 + self.angular_tolerance_steps)
            )

            if not self.require_redundancy:
                if angular_span_safe_margin >= 360:
                    self.sunshine_image[i_h] = margin_collector
                elif angular_span_bare_border >= 360:
                    self.sunshine_image[i_h] = detector_collector
            else:
                redundancy_angle_deg = 360
                if angular_span_safe_margin >= 360 and angular_span_safe_margin > 2 * (
                    redundancy_angle_deg + avg_step_deg
                ):
                    self.sunshine_image[i_h] = margin_collector
                elif angular_span_bare_border >= 360 and angular_span_bare_border > 2 * (
                    redundancy_angle_deg + avg_step_deg
                ):
                    self.sunshine_image[i_h] = detector_collector

        sunshine_mask = np.less(0.99, self.sunshine_image)

        self.sunshine_image[np.array([True]) ^ sunshine_mask] = 1.0
        self.sunshine_image[:] = 1 / self.sunshine_image
        self.sunshine_image[np.array([True]) ^ sunshine_mask] = 0.0

        shp = self.sunshine_image.shape
        X, Y = np.meshgrid(np.arange(shp[1]), np.arange(shp[0]))

        condition = self.sunshine_image > 0
        self.sunshine_starts = X.min(axis=1, initial=shp[1], where=condition)
        self.sunshine_ends = X.max(axis=1, initial=0, where=condition)
        self.sunshine_ends[self.sunshine_ends > 0] += 1
