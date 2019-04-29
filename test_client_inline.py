def test_read_file_as_b64():
    from client_inline import read_file_as_b64
    import base64

    with open("KimAndRevcopy.tiff", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    b64_string = str(encoded_string, encoding='utf-8')
    i = read_file_as_b64("KimAndRevcopy.tiff")
    assert i == b64_string


def test_save_b64_image():
    from client_inline import save_b64_image
    import base64
    import matplotlib.image as mpimg

    with open("KimAndRevcopy.tiff", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    i = save_b64_image(encoded_string)
    I = mpimg.imread('KimAndRevcopy.tiff')
    assert i.all() == I.all()

