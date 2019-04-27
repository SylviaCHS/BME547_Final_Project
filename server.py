import logging
import os
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
from Mongo import User
# import matplotlib.pyplot as plt
import base64
import io
from io import BytesIO
import matplotlib.image as mpimg
from PIL import Image
import zl187_image_processing as Process

app = Flask(__name__)


def read_data_as_b64(I_bytes):  # Test me!
    """
    Used for converting input data into base64
    """
    I_buf = io.BytesIO(I_bytes)
    b64_bytes = base64.b64encode(I_bytes)
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def save_b64_image(base64_string):  # Test me!
    """
    Saves base64 string as bytes
    """
    image_bytes = base64.b64decode(base64_string)
    return image_bytes


def bytes_to_plot(bytes, extension):  # Test me!
    """
    Converts raw TIF format in Mongo to numpy array
    """
    image_buf = io.BytesIO(bytes)
    i = mpimg.imread(image_buf, format=extension)
    return i


def plot_to_bytes(plot):
    """
    Converts numpy array into raw TIF format for MongoModel
    """
    img = Image.fromarray(plot, "RGB")
    f = BytesIO()
    img.save(f, format='TIFF')
    data = f.getvalue()
    return data


def convert_to_tif(I):  # Test me!
    """
    Converts raw bytes of any format into tiff
    """
    with BytesIO() as f:
        img = Image.open(io.BytesIO(I)).convert("RGB")
        img.save(f, format='TIFF')
        data = f.getvalue()
    return data


def verify_newuser(ID):
    """
    Checks existence of username
    """
    users = User.objects.raw({})

    x = True
    for u in users:
        if ID == str(u.UserID):
            x = False
    return x


def verify_newimage(filename, ID):
    """
    Checks existence of filename
    """
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
    """
    Post request for new user
    """
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
    """
    Post request for new image
    """
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

            image = save_b64_image(rawimage)
            image_tif = convert_to_tif(image)
            A = bytes_to_plot(image_tif, "tiff")
            [his_raw, bins_raw] = Process.plot_his(A)
            histogram = his_raw
            bins = bins_raw
            [m, n] = Process.get_size(A)
            s = [m, n]
            outstr = save_image(user, filename, image_tif, "None", "None",
                                s, histogram, bins)
            # Store in database that it is the original image user sent in
            user.raw_image.append(bool(1))
            user.save()
        else:
            outstr = "Image already exists. Please select another name."
    else:
        outstr = "User does not exist. Verify username or create new account"
    return outstr


def save_image(user, filename, image_tif, process, latency, size, hist, bins):
    """
    Function that saves image to Mongo (no calls)
    """
    time = datetime.datetime.now()
    Image_Dict = {
                    "File": filename,
                    "Image": image_tif,
                    "Process": process,
                    "Timestamp": time,
                    "Latency": latency,
                    "Size": size,
                    "Histogram": hist,
                    "Histogram Bins": bins,
                 }
    Image_List = user.ImageFile
    Image_List.append(Image_Dict)
    user.filenames.append(filename)
    user.save()
    outstr = "Image saved successfully"
    return outstr


@app.route("/api/get_name/image_list", methods=["GET"])
def get_image_list():
    """
    A route to GET a list of processed image name from MongoDB
    Returns:
    """
    r = request.get_json()
    username = str(r["username"])
    x = verify_newuser(username)
    if x is False:
        pro_filenames = get_process_image_list(username)
        outjson = pro_filenames

    else:
        outjson = ["Image does not exist. Please upload image"]
    return jsonify(outjson)


def get_process_image_list(username):
    """
    Get the list of names of processed image

    Returns:
    """
    user = User.objects.raw({"_id": username}).first()

    pro_filenames = [user.filenames[i] for i, x in
                     enumerate(user.raw_image) if x is False]
    print(user.filenames)
    return pro_filenames


@app.route("/api/get_image", methods=["GET"])
def GetImage():
    """
    Requests single image from database
    """
    r = request.get_json()
    username = str(r["username"])
    filename = str(r["filename"])

    x = verify_newuser(username)

    if x is False:
        y = verify_newimage(filename, username)
        if y is False:
            user = User.objects.raw({"_id": username}).first()
            image = find_image(filename, username)
            I = image["Image"]
            Ib64 = read_data_as_b64(I)
            outjson = {"File": image["File"],
                       "Image": Ib64,
                       "Process": image["Process"],
                       }
        else:
            outjson = "Image does not exist. Please upload image"
    else:
        outjson = "User does not exist. Please upload image"
    return jsonify(outjson)


def find_image(filename, username):
    """
    Queries database for image
    """
    user = User.objects.raw({"_id": username}).first()
    idx = user.filenames.index(filename)
    image = user.ImageFile[idx]
    return image


def process_image(iraw, process):  # Test me!
    """
    Processes image as specified by user
    """
    i_process = 0
    if process == "Histogram Equalization":
        i_process = Process.his_eq(iraw)
    elif process == "Contrast Stretching":
        i_process = Process.con_str(iraw)
    elif process == "Log Compression":
        i_process = Process.log_com(iraw)
    elif process == "Reverse Video":
        i_process = Process.rev(iraw)
    return i_process


@app.route("/api/process_image", methods=["POST"])
def get_process():
    """
    Processes image and saves to database
    """
    r = request.get_json()
    t1 = datetime.datetime.now()
    filename = str(r["filename"])
    username = str(r["username"])
    process = str(r["process"])
    newfilename = filename+"_"+process
    y = verify_newimage(filename, username)
    if y is False:
        x = verify_newimage(newfilename, username)
        if x is True:
            user = User.objects.raw({"_id": username}).first()
            List = user.ImageFile
            I = find_image(filename, username)
            Iraw = I["Image"]
            Imat = bytes_to_plot(Iraw, "tiff")
            [I_process, latency] = process_image(Imat, process)
            [hist_process, bins_process] = Process.plot_his(I_process)
            histogram = hist_process
            bins = bins_process
            [m, n] = Process.get_size(I_process)
            s = [m, n]
            # plt.imshow(I_process, interpolation="nearest")
            # plt.show()
            I_process_bytes = plot_to_bytes(I_process)
            # I_test = bytes_to_plot(I_process_bytes, "tiff")
            # plt.imshow(I_test, interpolation="nearest")
            # plt.show()
            t2 = datetime.datetime.now()
            save_image(user, newfilename, I_process_bytes, t2, latency,
                       s, histogram, bins)
            user.raw_image.append(bool(0))
            user.save()
            outjson = "Image is processed successfully"
        else:
            outjson = "Image is processed successfully"
    else:
        outjson = "Invalid data entry"
    return jsonify(outjson)


@app.route("/api/user_metrics/<username>", methods=["GET"])
def user_metrics():
    r = request.get_json()
    username = r["username"]
    x = verify_newuser(username)
    if x is False:
        outjson = get_metrics(username)
    else:
        outjson = "User does not exist"


def get_metrics(username):
    user = User.objects.raw({"_id": username}).first()
    Image_List = user.ImageFile
    his_eq_mat = find_images("his_eq", Image_List)


def find_images(instr, List):
    count = 0
    for i in List:
        if List["process"] == instr:
            latmat = List["latency"]
            count = count+1
    latarr = np.ndarray(latmat)

    outdict = {"Count": count, }

    return outdict


if __name__ == '__main__':
    """
    Execute the server
    """
    app.run()
