import skimage as ski
import matplotlib.pyplot as plt


def plot_his(image):
    # image here should be an array
    his, bins = ski.exposure.histogram(image, normalize=True)
    plt.plot(bins, his)
    plt.show()
    return his, bins


def his_eq(image):
    img_eq = ski.exposure.equalize_hist(image)
    return img_eq


def con_str(image):
    img_str = ski.exposure.rescale_intensity(image)
    return img_str


def log_com(image):
    img_log = ski.exposure.adjust_log(image)
    return img_log


def rev(image):
    img_rev = ski.util.invert(image)
    return img_rev
