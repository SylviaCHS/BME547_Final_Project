import requests
import time
import datetime
import base64
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def post_new_user(ID):
    """
    POST request to save new user name to MongoDB

    Args:
        ID (str): user name
    """
    user = {
        "username": ID,
    }
    r3 = requests.post("http://127.0.0.1:5000/api/new_user", json=user)
    return r3.text


def upload_file(ID, filename, extension, filepathname):
    """
    Upload files to server/database

    Args:
        ID (str): user name
        filename (str): filename with no path and extension
        extension (str): image type
        filepathname (str): full filename with path and extension

    Returns:
        r4.text (str): message from server
    """

    I = read_file_as_b64(filepathname)
    userimage = {
        "username": ID,
        "Image": I,
        "filename": filename,
        "extension": extension
    }
    r4 = requests.post("http://127.0.0.1:5000/api/new_image", json=userimage)
    return r4.text


def get_image_list(username):
    """
    Get list of processed image names

    Args:
        username (str): user name

    Returns:
        outfile (list or str): List of processed image names or error message

    """

    r5 = requests.get('http://127.0.0.1:5000/api/get_name/image_list',
                      json={"username": username})
    outfile = r5.json()
    return outfile


def get_image_file(ID, filename):
    """
    Get image file
    Args:
        ID (str): user name
        filename (str): file name

    Returns:
        r6.json()(dict or str): Dictionary with keys
                                File: filename
                                Image: Image in b64 tiff format
                                Process: processing algorithm applied
        If user/image does not exist, an error message will
        be returned to the client.

    """
    imjson = {
        "username": ID,
        "filename": filename
    }
    r6 = requests.get("http://127.0.0.1:5000/api/get_image", json=imjson)
    return r6.json()


def get_image(outfile):
    """
    Decode images to numpy arrary

    Args:
        outfile (dict): Dictionary with keys
                        File: filename
                        Image: Image in b64 tiff format
                        Process: processing algorithm applied

    Returns:
        img (nparray): Decoded image from server
        method (str): Method used to process this image

    """
    I2_b64 = outfile["Image"]
    img = save_b64_image(I2_b64)
    method = outfile["Process"]
    return img, method


def process_image(ID, filename, method):
    """
    POST request the user to process the image

    Args:
        ID (str): user name
        filename (str): filename that should exist in database
        method (str): processing method

    Returns:
        r6.json() (str): Confirmation that image was processed or error message
    """
    pjson = {
        "username": ID,
        "filename": filename,
        "process": method
    }
    r6 = requests.post("http://127.0.0.1:5000/api/process_image", json=pjson)
    print(r6.json)
    return r6.json()


def user_metrics(ID):
    """
    GET user metrics from server
    Args:
        ID (str): user name
    Returns:
        r7.json() (dict): Dictionary containing the user metrics of
                         number of times used and latency for each method
    """
    mjson = {
        "username": ID
    }
    r7 = requests.get("http://127.0.0.1:5000/api/user_metrics", json=mjson)
    return r7.json()


def image_metrics(ID, filename):
    """
     GET image metrics from server
     Args:
         ID (str): user name
     Returns:
         r7.json() (dict): Dictionary containing the image metrics
                        example: outdict = {
                                "timestamp": ...,
                                "size": [100, 100],
                                "latency": 1,
                                "process": 'Reverse Video'}
     """
    mjson = {
        "username": ID,
        "filename": filename
    }
    r8 = requests.get("http://127.0.0.1:5000/api/image_metrics", json=mjson)
    return r8.json()


def get_histogram(ID, filename):
    """
    GET request to get histogram image from server/database
    Args:
        ID (str): user name
        filename (str): filename

    Returns:
        i (nparray) : array of histogram image

    """
    djson = {
        "username": ID,
        "filename": filename,
    }
    r = requests.get("http://127.0.0.1:5000/api/get_histogram", json=djson)
    outfile = r.json()
    I2_b64 = outfile["Histogram"]
    i = save_b64_image(I2_b64)
    return i


def read_file_as_b64(image_path):
    """
    Encode image file or image from zip archive to base64

    Args:
        image_path (bytes or str): if from a zip archive, it is an image in
                                   bytes;
                                   if from local directory, it should be a
                                   string specifying the filepath

    Returns:
        b64_string (str): encoded image file ready to be sent to server
    """
    # If input is from zip archive, it will be in bytes
    if type(image_path) is bytes:
        b64_bytes = base64.b64encode(image_path)
    else:  # Or it is from a directory
        with open(image_path, "rb") as image_file:
            b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')

    return b64_string


def save_b64_image(base64_string):
    """
        Saves base64 string as bytes, then covert it back to an image array in
        tiff format

        Args:
            base64_string: image output string in base 64

        Returns:
            i (nparray): image array
    """

    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='tiff')
    return i
