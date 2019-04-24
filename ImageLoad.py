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
import matplotlib.image as mpimg


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def view_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return


def save_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    with open("new-img.jpg", "wb") as out_file:
        out_file.write(image_bytes)
    return


def NewUser(username):
    Image_List = []
    u = User(ID)
    u.save()
    str = "User saved successfully"
    return str


def NewImage(username, image, filename):
    user = User.objects.raw({"_id": username}).first()
    time = datetime.datetime.now()
    Image_Dict = {
                    "File": filename,
                    "Image": image,
                    "Process": "None",
                    "Timestamp": time,
                    "Latency": "None"
                  }
    Image_List.append(Image_Dict)
    u.save()


def main():
    ID = "Kim"
    Image_List = []
    filename = "KimAndRev copy"
    filepathname = r"C:\Users\lenno\OneDrive\Documents\KimAndRev copy.png"
    NewUser(ID)


if __name__ == "__main__":
    main()
