import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import timeit


def plot_his(image):
    his, bins = ski.exposure.histogram(image, normalize=True)
    plt.plot(bins, his)
    plt.show()
    return his, bins


def his_eq(image):
    start = timeit.default_timer()
    img_eq = ski.exposure.equalize_hist(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_eq, time_process


def con_str(image):
    start = timeit.default_timer()
    img_str = ski.exposure.rescale_intensity(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_str, time_process


def log_com(image):
    start = timeit.default_timer()
    img_log = ski.exposure.adjust_log(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_log, time_process


def rev(image):
    start = timeit.default_timer()
    img_rev = ski.util.invert(image)
    end = timeit.default_timer()
    time_process = str(end-start)
    return img_rev, time_process


def get_size(image):
    img = ski.color.rgb2gray(image)
    m, n = np.shape(img)
    return m, n
