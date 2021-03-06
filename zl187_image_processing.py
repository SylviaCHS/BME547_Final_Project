import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import timeit


def plot_his(image):
    """Plot histogram for an input image

    Args:
        image: input image data (should be ndarray)

    returns:
        his: normalized histogram value
        bins: graylevel scale values
    """
    color = check_color_or_gray(image)
    if color != 0:
        if color == 1:
            his, bins = ski.exposure.histogram(image, normalize=True)
            plt.plot(bins, his)
            plt.show()
            plt.tight_layout()
            outfig = make_figbw(his, bins)
            plt.close()
        if color == 2:
            his1, bins1 = ski.exposure.histogram(image[:, :, 0],
                                                 normalize=True)
            his2, bins2 = ski.exposure.histogram(image[:, :, 1],
                                                 normalize=True)
            his3, bins3 = ski.exposure.histogram(image[:, :, 2],
                                                 normalize=True)

            his = np.array([his1, his2,
                            his3])
            bins = np.array([bins1, bins2,
                             bins3])
            # plt.plot(bins1, his1)
            # plt.plot(bins2, his2)
            # plt.plot(bins3, his3)
            # plt.show()
            # plt.tight_layout()
            # plt.savefig(fname)
            outfig = make_fig(his1, bins1, his2, bins2, his3, bins3)
            plt.close()
    else:
        outfig = ("The image format is not correct.")
        his = 0
        bins = 0
    return [outfig, his, bins]


def make_fig(his1, bins1, his2, bins2, his3, bins3):
    """ Converts histogram into image to
        be returned to user
    Args:
        his1: histogram values of red channel
        his2: histogram values of green channel
        his3: histogram values of blue channel
        bins1: bins for red channel
        bins2: bins for green channel
        bine3: bins for blue channel
    Returns:
        fig: Image of 3 channel histogram
    """
    fig = plt.figure()
    plt.plot(bins1, his1)
    plt.plot(bins2, his2)
    plt.plot(bins3, his3)
    plt.tick_params(labelsize=20)
    plt.tight_layout()
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data


def make_figbw(his1, bins1):
    """ Converts histogram into image that can
        be returned to user
    Args:
        his1: histogram values
        bins1: bins
    Returns:
        fig: Image of 1 channel histogram
    """
    fig = plt.figure()
    plt.plot(bins1, his1)
    plt.tick_params(labelsize=20)
    plt.tight_layout()
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close()
    return data


def his_eq(image):
    """Doing histogram equalization and count the time for processing

    Args:
        image: input image data (should be ndarray)

    returns:
        img_eq: image after histogram equalization
        time_process: time for doing the processing
    """
    from skimage import img_as_ubyte
    color = check_color_or_gray(image)
    if color != 0:
        if color == 1:
            start = timeit.default_timer()
            img_eq = ski.exposure.equalize_hist(image)
            end = timeit.default_timer()
            time_process = str(end-start)
        if color == 2:
            start = timeit.default_timer()
            img_eq1 = ski.exposure.equalize_hist(image[:, :, 0])
            img_eq2 = ski.exposure.equalize_hist(image[:, :, 1])
            img_eq3 = ski.exposure.equalize_hist(image[:, :, 2])
            img_eq = np.dstack((img_eq1, img_eq2, img_eq3))

            # EDIT KKL 2019/04/25: histogram equalization converts to float
            img_eq = img_as_ubyte(img_eq)

            end = timeit.default_timer()
            time_process = str(end-start)
    else:
        print("The image format is not correct.")
    return img_eq, time_process


def con_str(image):
    """Doing contrast stretch and count the time for processing

    Args:
        image: input image data (should be ndarray)

    returns:
        img_str: image after contrast stretch
        time_process: time for doing the processing
    """
    start = timeit.default_timer()
    img_str = ski.exposure.rescale_intensity(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_str, time_process


def log_com(image):
    """Doing log compression and count the time for processing

    Args:
        image: input image data (should be ndarray)

    returns:
        img_str: image after log compression
        time_process: time for doing the processing
    """
    start = timeit.default_timer()
    img_log = ski.exposure.adjust_log(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_log, time_process


def rev(image):
    """Doing reverse video and count the time for processing

    Args:
        image: input image data (should be ndarray)

    returns:
        img_rev: image after reverse video
        time_process: time for doing the processing
    """
    start = timeit.default_timer()
    img_rev = ski.util.invert(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_rev, time_process


def get_size(image):
    """Get the size of the image

    Args:
        image: input image data (should be ndarray)

    returns:
        m: number of the rows of the image data
        n: number of the columns of the image data
    """
    img = ski.color.rgb2gray(image)
    m, n = np.shape(img)
    return m, n


def check_color_or_gray(image):
    """Check the image is in color or grayscale

    Args:
        image: input image data (should be ndarray)

    returns:
        color: a number that indicates whether the image is in color
               or grayscale
    """
    color = 0
    siz = np.shape(image)
    dim = len(siz)
    if dim == 2:
        color = 1
    if dim == 3:
        color = 2
    if color == 0:
        print("The image format is not correct.")
    return color
