import requests
import time
import datetime
import base64
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def post_new_user(ID):
    user = {
        "username": ID,
    }
    r3 = requests.post("http://127.0.0.1:5000/api/new_user", json=user)
    return r3.text


def upload_file(ID, filename, extension, filepathname):

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

    r5 = requests.get('http://127.0.0.1:5000/api/get_name/image_list',
                      json={"username": username})
    outfile = r5.json()
    return outfile


def get_image(ID, filename):
    imjson = {
        "username": ID,
        "filename": filename
    }

    r6 = requests.get("http://127.0.0.1:5000/api/get_image", json=imjson)
    outfile = r6.json()
    I2_b64 = outfile["Image"]
    img = save_b64_image(I2_b64)
    method = outfile["Process"]
    return img, method


def process_image(ID, filename, method):
    pjson = {
        "username": ID,
        "filename": filename,
        "process": method
    }
    r6 = requests.post("http://127.0.0.1:5000/api/process_image", json=pjson)
    return r6.json()


def user_metrics(ID):
    mjson = {
        "username": ID
    }
    r7 = requests.get("http://127.0.0.1:5000/api/user_metrics", json=mjson)
    return r7.json()


def image_metrics(ID, filename):
    mjson = {
        "username": ID,
        "filename": filename
    }
    r8 = requests.get("http://127.0.0.1:5000/api/image_metrics", json=mjson)
    return r8.json()


def get_histogram(ID, filename):
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
    # If input is from zip archive, it will be in bytes
    if type(image_path) is bytes:
        b64_bytes = base64.b64encode(image_path)
    else:  # Or it is from a directory
        with open(image_path, "rb") as image_file:
            b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')

    return b64_string


def save_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='tiff')
    return i
