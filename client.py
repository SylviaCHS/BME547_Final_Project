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
    print(r3.text)


def upload_file(ID, filename, extension, filepathname):
    #Image_List = []

    I = read_file_as_b64(filepathname)
    userimage = {
        "username": ID,
        "Image": I,
        "filename": filename,
        "extension": extension
    }
    r4 = requests.post("http://127.0.0.1:5000/api/new_image", json=userimage)
    print(r4.text)

def receive_image_list():

    imjson = {
        "username": ID,
        "filename": filename
    }
    r5 = requests.get("http://127.0.0.1:5000/api/image_list")


def receive_file():

    r6 = requests.get("http://127.0.0.1:5000/api/get_image", json=imjson)
    outfile = r5.json()
    I2_b64 = outfile["Image"]
    save_b64_image(I2_b64)


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def save_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='tiff')
    #plt.imshow(i, interpolation='nearest')
    #plt.show()
    return i

