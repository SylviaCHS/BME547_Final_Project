import logging
import os
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
from Mongo import User
import matplotlib.pyplot as plt
import base64
import io
from io import BytesIO
import matplotlib.image as mpimg
from PIL import Image


app = Flask(__name__)


def read_file_as_b64(I_bytes):
    I_buf = io.BytesIO(I_bytes)
    b64_bytes = base64.b64encode(I_bytes)
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def save_b64_image(base64_string, extension):
    image_bytes = base64.b64decode(base64_string)
    bytes_to_plot(image_bytes, extension)
    return image_bytes


def bytes_to_plot(bytes, extension):
    image_buf = io.BytesIO(bytes)
    i = mpimg.imread(image_buf, format=extension)
    plot.imshow(i, interpolation='nearest')
    plt.show()


def convert_to_tif(I):
    with BytesIO() as f:
        img = Image.open(io.BytesIO(I))
        img.show()
        img.save(f, format='TIFF')
        data = f.getvalue()
    i_buf = io.BytesIO(data)
    i = mpimg.imread(i_buf, format="tiff")
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return data


def verify_newuser(ID):
    users = User.objects.raw({})
    x = True
    for u in users:
        if ID == str(u.UserID):
            x = False
    return x


def verify_newimage(filename, ID):
    u = User.objects.raw({"_id": ID}).first()
    x = True
    cursor = u.filenames
    if cursor == []:
        x = True

    else:
        for i in cursor:
            if i == filename:
                x = False
    return x


@app.route("/api/new_user", methods=["POST"])
def NewUser():
    r = request.get_json()
    username = r["username"]
    ID = str(username)
    x = verify_newuser(username)
    if x is True:
        u = User(UserID=username)
        u.save()
        outstr = "User saved successfully"
    else:
        outstr = "User already exists. Select new username"
    return jsonify(outstr)


@app.route("/api/new_image", methods=["POST"])
def NewImage():
    r = request.get_json()
    username = str(r["username"])
    filename = str(r["filename"])
    rawimage = str(r["Image"])
    extension = str(r["extension"])
    y = verify_newuser(username)

    if y is False:
        x = verify_newimage(filename, username)

        if x is True:
            user = User.objects.raw({"_id": username}).first()
            time = datetime.datetime.now()
            image = save_b64_image(rawimage, extension)
            image_tif = convert_to_tif(image)
            Image_Dict = {
                            "File": filename,
                            "Image": image_tif,
                            "Process": "None",
                            "Timestamp": time,
                            "Latency": "None"
                          }
            Image_List = user.ImageFile
            Image_List.append(Image_Dict)
            filenames = user.filenames
            filenames.append(filename)
            user.save()
            outstr = "Image saved successfully"
        else:
            outstr = "Image already exists. Please select another name."
    else:
        outstr = "User does not exist. Verify username or create new account"
    return outstr


@app.route("/api/get_image", methods=["POST"])
def GetImage():
    r = request.get_json()
    username = str(r["username"])
    filename = str(r["filename"])

    x = verify_newuser(username)
    if x is False:
        y = verify_newimage(filename, username)
        if y is False:
            user = User.objects.raw({"_id": username}).first()
            Image_List = user.ImageFile
            userfiles = user.filenames
            idx = userfiles.index(filename)
            image = Image_List[idx]
            I = image["Image"]
            Ib64 = read_file_as_b64(I)
            outjson = {"File": image["File"],
                       "Image": Ib64,
                       "Process": image["Process"],
                       }

        else:
            outjson = "Image does not exist. Please upload image"
    else:
        outjson = "User does not exist. Please upload image"
    return jsonify(outjson)

# @app.route("/api/save_image", methods = ["POST"])
# @app.route("/api/download_image", methods=["POST"])
