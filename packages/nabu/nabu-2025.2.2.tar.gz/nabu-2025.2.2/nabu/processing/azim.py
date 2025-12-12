from multiprocessing.pool import ThreadPool
import numpy as np

try:
    from skimage.transform import warp_polar

    __have_skimage__ = True
except ImportError:
    __have_skimage__ = False


def azimuthal_integration(img, axes=(-2, -1), domain="direct"):
    """
    Computes azimuthal integration of an image or a stack of images.

    Parameters
    ----------
    img : `numpy.array_like`
        The image or stack of images.
    axes : tuple(int, int), optional
        Axes of that need to be azimuthally integrated. The default is (-2, -1).
    domain : string, optional
        Domain of the integration. Options are: "direct" | "fourier". Default is "direct".

    Raises
    ------
    ValueError
        Error returned when not passing images or wrong axes.
    NotImplementedError
        In case of tack of images for the moment.

    Returns
    -------
    `numpy.array_like`
        The azimuthally integrated profile.
    """
    if not len(img.shape) >= 2:
        raise ValueError("Input image should be at least 2-dimensional.")
    if not len(axes) == 2:
        raise ValueError("Input axes should be 2.")

    img_axes_dims = np.array((img.shape[axes[0]], img.shape[axes[1]]))
    if domain.lower() == "direct":
        half_dims = (img_axes_dims - 1) / 2
        xx = np.linspace(-half_dims[0], half_dims[0], img_axes_dims[0])
        yy = np.linspace(-half_dims[1], half_dims[1], img_axes_dims[1])
    else:
        xx = np.fft.fftfreq(img_axes_dims[0], 1 / img_axes_dims[0])
        yy = np.fft.fftfreq(img_axes_dims[1], 1 / img_axes_dims[1])
    xy = np.stack(np.meshgrid(xx, yy, indexing="ij"))
    r = np.sqrt(np.sum(xy**2, axis=0))

    img_tr_op = [*range(len(img.shape))]
    for a in axes:
        img_tr_op.append(img_tr_op.pop(a))
    img = np.transpose(img, img_tr_op)
    if len(img.shape) > 2:
        img_old_shape = img.shape[:-2]
        img = np.reshape(img, [-1, *img_axes_dims])

    r_l = np.floor(r)
    r_u = r_l + 1
    w_l = (r_u - r) * img
    w_u = (r - r_l) * img

    r_all = np.concatenate((r_l.flatten(), r_u.flatten())).astype(np.int64)
    if len(img.shape) == 2:
        w_all = np.concatenate((w_l.flatten(), w_u.flatten()))
        return np.bincount(r_all, weights=w_all)
    else:
        num_imgs = img.shape[0]
        az_img = [None] * num_imgs
        for ii in range(num_imgs):
            w_all = np.concatenate((w_l[ii, :].flatten(), w_u[ii, :].flatten()))
            az_img[ii] = np.bincount(r_all, weights=w_all)
        az_img = np.array(az_img)
        return np.reshape(az_img, (*img_old_shape, az_img.shape[-1]))


def do_radial_distribution(ip, X0, Y0, mR, nBins=None, use_calibration=False, cal=None, return_radii=False):
    """
    Translates the Java method `doRadialDistribution` (from imagej) into Python using NumPy.
    Done by chatgpt-4o on 2024-11-08

    Args:
    - ip: A 2D numpy array representing the image.
    - X0, Y0: Coordinates of the center.
    - mR: Maximum radius.
    - nBins: Number of bins (optional, defaults to 3*mR/4).
    - use_calibration: Boolean indicating if calibration should be applied.
    - cal: Calibration object with attributes `pixel_width` and `units` (optional).
    """
    if nBins is None:
        nBins = int(3 * mR / 4)

    Accumulator = np.zeros((2, nBins))

    # Define the bounding box
    height, width = ip.shape
    xmin = max(int(X0 - mR), 0)
    xmax = min(int(X0 + mR), width)
    ymin = max(int(Y0 - mR), 0)
    ymax = min(int(Y0 + mR), height)

    # Create grid of coordinates
    x = np.arange(xmin, xmax)
    y = np.arange(ymin, ymax)
    xv, yv = np.meshgrid(x, y, indexing="ij")

    # Calculate the radius for each point
    R = np.sqrt((xv - X0) ** 2 + (yv - Y0) ** 2)

    # Bin calculation
    bins = np.floor((R / mR) * nBins).astype(int)
    bins = np.clip(bins - 1, 0, nBins - 1)  # Adjust bins to be in range [0, nBins-1]

    # Accumulate values
    sub_image = ip[xmin:xmax, ymin:ymax]  # prevent issue on non-square images
    for b in range(nBins):
        mask = bins == b
        Accumulator[0, b] = np.sum(mask)
        Accumulator[1, b] = np.sum(sub_image[mask])

    # Normalize integrated intensity
    Accumulator[1] /= Accumulator[0]

    if use_calibration and cal is not None:
        # Apply calibration if units are provided
        radii = cal.pixel_width * mR * (np.arange(1, nBins + 1) / nBins)
        # units = cal.units
    else:
        # Use pixel units
        radii = mR * (np.arange(1, nBins + 1) / nBins)
        # units = "pixels"

    if return_radii:
        return radii, Accumulator[1]
    else:
        return Accumulator[1]


# OK-ish, but small discrepancy with do_radial_distribution.
# 20-40X faster than above methods for (2048, 2048) images
# Also it assumes a uniform sampling
# No idea why there is this "offset=1", to be investigated - perhaps radius=0 is also calculated ?
def azimuthal_integration_skimage(img, center=None, offset=1):
    shape2 = [int(s // 2 * 1.4142) for s in img.shape]
    s = min(img.shape) // 2
    img_polar = warp_polar(img, output_shape=shape2, center=center)
    return img_polar.mean(axis=0)[offset : offset + s]


def _apply_on_images_stack(func, images_stack, n_threads=4, func_args=None, func_kwargs=None):
    func_args = func_args or []
    func_kwargs = func_kwargs or {}

    def _process_image(img):
        return func(img, *func_args, **func_kwargs)

    with ThreadPool(n_threads) as tp:
        res = tp.map(_process_image, images_stack)
    return np.array(res)


def _apply_on_patches_stack(func, images_stack, n_threads=4, func_args=None, func_kwargs=None):
    (n_images, n_patchs_y, img_shape_y, n_patchs_x, img_shape_x) = images_stack.shape
    func_args = func_args or []
    func_kwargs = func_kwargs or {}
    out_sample = func(images_stack[0, 0, :, 0, :], *func_args, **func_kwargs)
    out_shape = out_sample.shape
    out_dtype = out_sample.dtype

    def _process_image(img):
        res = np.zeros((n_patchs_y, n_patchs_x) + out_shape, dtype=out_dtype)
        for i in range(n_patchs_y):
            for j in range(n_patchs_x):
                res[i, j] = func(img[i, :, j, :], *func_args, **func_kwargs)
        return res

    with ThreadPool(n_threads) as tp:
        res = tp.map(_process_image, images_stack)
    return np.array(res)


def azimuthal_integration_imagej_stack(images_stack, n_threads=4):
    if images_stack.ndim == 3:
        img_shape = images_stack.shape[-2:]
        _apply = _apply_on_images_stack
    elif images_stack.ndim == 5:
        img_shape = np.array(images_stack.shape)[[-3, -1]]
        _apply = _apply_on_patches_stack
    else:
        raise ValueError
    s = min(img_shape)
    return _apply(
        do_radial_distribution,
        images_stack,
        n_threads=n_threads,
        func_args=[s // 2, s // 2, s // 2],
        func_kwargs={"nBins": s // 2, "return_radii": False},
    )


def azimuthal_integration_skimage_stack(images_stack, n_threads=4):
    if images_stack.ndim == 3:
        return _apply_on_images_stack(azimuthal_integration_skimage, images_stack, n_threads=n_threads)
    elif images_stack.ndim == 5:
        return _apply_on_patches_stack(azimuthal_integration_skimage, images_stack, n_threads=n_threads)
    else:
        raise ValueError
