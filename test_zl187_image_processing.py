import skimage as ski
import numpy as np


def test_plot_his1():
    from zl187_image_processing import plot_his
    image = np.ones([2, 2], dtype=np.uint8)
    his, bins = plot_his(image)
    his_exp = np.array([1])
    assert his.all() == his_exp.all()


def test_plot_his2():
    from zl187_image_processing import plot_his
    image = np.ones([2, 2], dtype=np.uint8)
    his, bins = plot_his(image)
    bins_exp = np.array([1])
    assert bins.all() == bins_exp.all()


def test_plot_his3():
    from zl187_image_processing import plot_his
    image = np.ones([2, 2, 3], dtype=np.uint8)
    his, bins = plot_his(image)
    his_exp = np.array([[1], [1], [1]])
    assert np.array(his).all() == his_exp.all()


def test_plot_his4():
    from zl187_image_processing import plot_his
    image = np.ones([2, 2, 3], dtype=np.uint8)
    his, bins = plot_his(image)
    bins_exp = np.array([[1], [1], [1]])
    assert np.array(bins).all() == bins_exp.all()


def test_his_eq1():
    from zl187_image_processing import his_eq
    image = np.ones([2, 2], dtype=np.uint8)
    img_eq, _ = his_eq(image)
    img_eq_exp = np.array([[1, 1],
                          [1, 1]])
    assert float(img_eq.all()) == float(img_eq_exp.all())


def test_his_eq2():
    from zl187_image_processing import his_eq
    image = np.ones([2, 2, 3], dtype=np.uint8)
    img_eq, _ = his_eq(image)
    img_eq_exp = np.array([[1, 1, 1],
                          [1, 1, 1]])
    assert float(img_eq.all()) == float(img_eq_exp.all())


def test_con_str():
    from zl187_image_processing import con_str
    image = np.array([0, 1, 1, 0], dtype=np.uint8)
    img_str, _ = con_str(image)
    img_str_exp = np.array([0, 255, 255, 0])
    assert float(img_str.all()) == float(img_str_exp.all())


def test_log_com():
    from zl187_image_processing import log_com
    image = np.array([0, 255, 255, 0])
    img_log, _ = log_com(image)
    img_log_exp = np.array([0, 367, 367, 0])
    assert float(img_log.all()) == float(img_log_exp.all())


def test_rev():
    from zl187_image_processing import rev
    image = np.array([0, 255, 255, 0])
    img_rev, _ = rev(image)
    img_rev_exp = np.array([-1, -2, -2, -1])
    assert float(img_rev.all()) == float(img_rev_exp.all())


def test_get_size1():
    from zl187_image_processing import get_size
    image = ski.data.astronaut()
    m, n = get_size(image)
    m_exp = 512
    assert float(m) == float(m_exp)


def test_get_size2():
    from zl187_image_processing import get_size
    image = ski.data.astronaut()
    m, n = get_size(image)
    n_exp = 512
    assert float(n) == float(n_exp)


def test_check_color_or_gray1():
    from zl187_image_processing import check_color_or_gray
    image = ski.data.astronaut()
    color = check_color_or_gray(image)
    color_exp = 2
    assert float(color) == float(color_exp)


def test_check_color_or_gray2():
    from zl187_image_processing import check_color_or_gray
    image = ski.data.astronaut()
    img = ski.color.rgb2gray(image)
    color = check_color_or_gray(img)
    color_exp = 1
    assert float(color) == float(color_exp)
