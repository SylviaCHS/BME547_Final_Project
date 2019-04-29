import pytest
import numpy as np


@pytest.mark.parametrize("size, expected", [
        ([100, 100], [100, 100]),
        ([400, 400], [300, 300]),
        ([100, 400], [75, 300])
         ])
def test_image_size1(size, expected):
    from GUI import image_size
    new_size = image_size(size)
    assert np.array(expected[0]) == np.array(new_size[0])


@pytest.mark.parametrize("size, expected", [
        ([100, 100], [100, 100]),
        ([400, 400], [300, 300]),
        ([100, 400], [75, 300])
         ])
def test_image_size2(size, expected):
    from GUI import image_size
    new_size = image_size(size)
    assert np.array(expected[1]) == np.array(new_size[1])
