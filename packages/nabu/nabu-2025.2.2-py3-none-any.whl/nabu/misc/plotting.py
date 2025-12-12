from math import sqrt, ceil
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def clip_std(arr, n=3):
    m = np.mean(arr)
    s = np.std(arr)
    return np.clip(arr, m - n * s, m + n * s)


def ims(img, cmap="gray", legend=None, colorbar=True, share=True, rescale_n_std=None):
    """
    image visualization utility.

    img: 2D numpy.ndarray, or list of 2D numpy.ndarray
        image or list of images
    cmap: string
        Optionnal, name of the colorbar to use.
    legend: string, or list of string
        legend under each image
    colorbar: bool
        Whether to show colorbar (default is True)
    share: bool
        if True, the axis are shared between the images, so that zooming in one image
        will zoom in all the corresponding regions of the other images. Default is True
    """
    if not (isinstance(img, (list, tuple))):
        img = [img]
    if isinstance(img, np.ndarray) and img.ndims == 3:
        img = [im for im in img]
    nimg = len(img)
    if legend is not None and not (isinstance(legend, (list, tuple))):
        legend = [legend]

    def _get_num_rows_cols(nimg):
        ncols = ceil(sqrt(nimg))
        nrows = ceil(nimg / ncols)
        return nrows, ncols

    subplot_kwargs = {}
    imshow_kwargs = {"interpolation": "nearest", "cmap": cmap}

    nrows, ncols = _get_num_rows_cols(nimg)
    plt.figure()
    for i in range(nimg):
        current_subplot = [nrows, ncols, i + 1]
        image = img[i]
        if rescale_n_std is not None:
            image = clip_std(image, n=rescale_n_std)
        if share and nimg > 1 and i == 0:
            ax0 = plt.subplot(*current_subplot)
            subplot_kwargs.update({"sharex": ax0, "sharey": ax0})
        else:
            plt.subplot(*current_subplot, **subplot_kwargs)

        plt.imshow(image, **imshow_kwargs)
        if legend:
            plt.xlabel(legend[i])
        if colorbar:
            plt.colorbar()

    plt.show()
