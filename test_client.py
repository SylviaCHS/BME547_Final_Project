def test_read_file_as_b64():
    from client import read_file_as_b64
    a = bytes([1, 2, 3, 4])
    b64_string = read_file_as_b64(a)
    expected = 'AQIDBA=='
    assert b64_string == expected


def test_save_b64_image():
    from client import save_b64_image
    import base64
    import matplotlib.image as mpimg

    with open("KimAndRevcopy.tiff", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    i = save_b64_image(encoded_string)
    I = mpimg.imread('KimAndRevcopy.tiff')
    assert i.all() == I.all()
