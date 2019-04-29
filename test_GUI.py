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


@pytest.mark.parametrize("filenames, expected", [
        ([1], bool(1)),
        ([1, 2], bool(0)),
        ([1, 2, 3], bool(0))
         ])
def test_check_multi_single(filenames, expected):
    from GUI import check_multi_single
    single = check_multi_single(filenames)
    assert single == expected


@pytest.mark.parametrize("msg, expected", [
        ('there is an Error', [bool(1), 'there is an Error']),
        ('there is a Warning',
         [bool(0), 'Success! Warning: Image already exists.'
          'Processing ran on existing image']),
        ('everythin is fine', [bool(0), 'Image saved successfully'])
         ])
def test_check_msg1(msg, expected):
    from GUI import check_msg
    err, msg = check_msg(msg)
    assert err == expected[0]


@pytest.mark.parametrize("msg, expected", [
        ('there is an Error', [bool(1), 'there is an Error']),
        ('there is a Warning',
         [bool(0), 'Success! Warning: Image already exists. ' \
          'Processing ran on existing image']),
        ('everythin is fine', [bool(0), 'Image saved successfully'])
         ])
def test_check_msg2(msg, expected):
    from GUI import check_msg
    err, msg = check_msg(msg)
    assert msg == expected[1]
