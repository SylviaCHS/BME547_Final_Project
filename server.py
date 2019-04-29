import logging
from flask import Flask, jsonify, request
import numpy as np
import datetime
from Mongo import User
import base64
import io
from io import BytesIO
import matplotlib.image as mpimg
from PIL import Image
import zl187_image_processing as Process

app = Flask(__name__)


def read_data_as_b64(I_bytes):
    """
    Used for converting input data into base64

    Args:
        I_bytes: image in uint8 bytes
    Returns:
        b64_string: image output string in base 64
    """
    I_buf = io.BytesIO(I_bytes)
    b64_bytes = base64.b64encode(I_bytes)
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def save_b64_image(base64_string):
    """
    Saves base64 string as bytes

    Args:
        base64_string: image output string in base 64

    Returns:
        image_bytes: image in bytes
    """
    image_bytes = base64.b64decode(base64_string)
    return image_bytes


def bytes_to_plot(bytes, extension):
    """
    Converts raw TIF format in Mongo to numpy array

    Args:
        bytes: image in byte
        extension: file format (always tiff)

    Returns:
        i: numpy array version of image
    """
    image_buf = io.BytesIO(bytes)
    i = mpimg.imread(image_buf, format=extension)
    return i


def plot_to_bytes(plot):
    """
    Converts numpy array into raw TIF format for MongoModel

    Args:
        plot: numpy array version of image

    Returns:
        data: image in bytes
    """
    img = Image.fromarray(plot, "RGB")
    f = BytesIO()
    img.save(f, format='TIFF')
    data = f.getvalue()
    return data


def convert_file(I, extension):
    """
    Converts raw bytes of any format into any
    other format

    Args:
        I: byte format of image
        extension: desired output file type
    Returns:
        data: byte format in desired file type
    """
    with BytesIO() as f:
        img = Image.open(io.BytesIO(I)).convert("RGB")
        img.save(f, format=extension)
        data = f.getvalue()
    return data


def verify_newuser(ID):
    """
    Checks existence of username

    Args:
        ID: Username
    Returns:
        x: Boolean value. If x = True, user does
        not exist in database
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

    Args:
        filename: Image name
        ID: Username
    Returns:
        x: Boolean value. If x is true,
        image does not exist in database
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

    Args:
        JSON with input:
        "username": Username
    Returns:
        outstr: String verifying user has been saved
                to database
    """
    r = request.get_json()
    username = r["username"]
    ID = str(username)
    x = verify_newuser(username)
    if x is True:
        u = User(UserID=username)
        u.save()
        outstr = "User saved successfully"
        code = 200
    else:
        outstr = "Error: User already exists. Select new username"
        code = 400
    return jsonify(outstr), code


@app.route("/api/new_image", methods=["POST"])
def NewImage():
    """
    Post request for new image

    Args:
        Input json file:
        "username": username
        "filename": image file name
        "rawimage": image as base 64 string
        "extension": original file type
    Returns:
        outstr: String verifying that image
                has been saved
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
            image_tif = convert_file(image, "TIFF")
            A = bytes_to_plot(image_tif, "tiff")
            [histplot, hist, bins] = Process.plot_his(A)
            histbytes = plot_to_bytes(histplot)
            [m, n] = Process.get_size(A)
            s = [m, n]
            outstr = save_image(user, filename, image_tif, "None", "None",
                                s, histbytes)
            code = 200
            # Store in database that it is the original image user sent in
            user.raw_image.append(bool(1))
            user.save()
        else:
            outstr = "Warning: Image already exists. " \
                     "Will run process on existing Image"
            code = 200
    else:
        outstr = "Error: User does not exist. " \
                 "Verify username or create new account"
        code = 400
    return jsonify(outstr), code


def save_image(user, filename, image_tif, process, latency, size, hist):
    """
    Function that saves image to Mongo database

    Args:
        user: username
        filename: desired file name in database
        image_tif: tiff image in byte format
        process: processing algorithm applied to image
        latency: time to process image
        size: image size
        hist: histogram values of image
        bins: bin locations of image
    Returns:
        outstr: Confirmation that image has been saved

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
    Args:
        Input json keys: "username"
    Returns:
        outjson: list of all images the user has stored
    """
    r = request.get_json()
    username = str(r["username"])
    x = verify_newuser(username)
    if x is False:
        pro_filenames = get_process_image_list(username)
        outjson = pro_filenames
        code = 200
    else:
        outjson = ["Error: User does not exist."]
        code = 400
    return jsonify(outjson), code


def get_process_image_list(username):
    """
    Get the list of names of processed image
    Args:
        JSON input: "username"
    Returns:
        pro_filenames (list): Names of all files that have been
                       processed by the user
    """
    user = User.objects.raw({"_id": username}).first()

    pro_filenames = [user.filenames[i] for i, x in
                     enumerate(user.raw_image) if x is False]
    return pro_filenames


@app.route("/api/get_image", methods=["GET"])
def GetImage():
    """
    Requests single image from database
    Args:
        Input JSON:
                "username": Username
                "filename": name of desired image
    Returns:
        outjson: Dictionary with keys
                 File: filename
                 Image: Image in b64 tiff format
                 Process: processing algorithm applied
        If user/image does not exist, an error message will
        be returned to the client.
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
            code = 200
        else:
            outjson = "Error: Image does not exist. Please upload image"
            code = 400
    else:
        outjson = "Error: User does not exist."
        code = 400
    return jsonify(outjson), code


def find_image(filename, username):
    """
    Queries database for image
    Args:
        Username: username
        filename: name of desired image
    Returns:
        image: dictionary of image along with
               all metadata
    """
    user = User.objects.raw({"_id": username}).first()
    idx = user.filenames.index(filename)
    image = user.ImageFile[idx]
    return image


def process_image(iraw, process):  # Test me!
    """
    Processes image as specified by user

    Args:
        iraw: Image to be processed
        process: processing method

    Returns:
        i_process: list with 2 entries: processed image
                   and time to process image
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

    Args:
        Input json:
        "username": username
        "filename": name of image to be processed
        "process": Desired processing algorithm

    Returns:
        outjson: Confirmation that image was processed
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
            [histplot, hist, bins] = Process.plot_his(I_process)
            histbytes = plot_to_bytes(histplot)
            [m, n] = Process.get_size(I_process)
            s = [m, n]
            # plt.imshow(I_process, interpolation="nearest")
            # plt.show()
            I_process_bytes = plot_to_bytes(I_process)
            # I_test = bytes_to_plot(I_process_bytes, "tiff")
            # plt.imshow(I_test, interpolation="nearest")
            # plt.show()
            save_image(user, newfilename, I_process_bytes, process,
                       latency, s, histbytes)
            user.raw_image.append(bool(0))
            user.save()
            outjson = "Image is processed successfully"
        else:
            outjson = "Image is processed successfully"
    else:
        outjson = "Invalid data entry"
    return jsonify(outjson)


@app.route("/api/user_metrics", methods=["GET"])
def user_metrics():
    """
    Return metrics for given user
    Args:
        Input json: "username:: username
    Returns:
        outjson: dictionary of all image processing
        algorithms, times used, and time to execute

    """
    r = request.get_json()
    username = r["username"]
    x = verify_newuser(username)
    if x is False:
        outjson = get_metrics(username)
    else:
        outjson = "User does not exist"
    return jsonify(outjson)


@app.route("/api/image_metrics", methods=["GET"])
def image_metrics():
    """
    Obtain metrics for a certain image

    Args:
        Input json:
            "username": username
            "filename": name of image
    Returns:
        outdict: List of all algorithms with
                 number of times used and time
                 to execute
    """
    r = request.get_json()
    username = r["username"]
    filename = r["filename"]
    x = verify_newuser(username)
    if x is False:
        user = User.objects.raw({"_id": username}).first()
        y = verify_newimage(filename, username)
        if y is False:
            I = find_image(filename, username)
            outdict = {
                      "timestamp": I["Timestamp"],
                      "size": I["Size"],
                      "latency": I["Latency"],
                      "process": I["Process"]
                      }
        else:
            outdict = ["This image does not exist"]
    else:
        outdict = ["User does not exist"]
    return jsonify(outdict)


def get_metrics(username):
    """
    Searches database for relevant user metrics
    Args:
        Username: username
    Returns:
        Outdict: List of all algorithms with
                 times used and mean time to
                 execute
    """
    user = User.objects.raw({"_id": username}).first()
    Image_List = user.ImageFile
    his_eq_dict = find_stats("Histogram Equalization", Image_List)
    con_str_dict = find_stats("Gontrast Stretching", Image_List)
    log_com_dict = find_stats("Log Compression", Image_List)
    rev_dict = find_stats("Reverse Video", Image_List)
    outdict = {
              "Histogram Equalization": his_eq_dict,
              "Log Compression": log_com_dict,
              "Contrast Stretching": con_str_dict,
              "Reverse Video": rev_dict
              }
    return outdict


def find_stats(instr, List):
    """
    Finds number of times a specific algorithm
    has been used by a user

    Args:
        instr: Processing method
        List: List of all images from a user

    Returns:
        info: list with 2 elements:
              count: number of times algorithm
                     was used
              latmean: average time to execute
    """
    count = 0
    latmat = []
    for i in List:
        if i["Process"] == instr:
            latmat.append(float(i["Latency"]))
            count = count+1
        if latmat == []:
            latmean = "N/A"
        else:
            latarr = np.asarray(latmat)
            latmean = np.mean(latmat)
    info = {"Times used": count,
            "Mean latency": latmean
            }
    return info


@app.route("/api/download_image", methods=["GET"])
def download_image():
    """
    Returns a base 64 string of any file format
    requested by user

    Args:
        Input JSON:
                    "username": username
                    "filename": name of image in database
                    "extension": desired file type'
    Returns:
        Outstring: Dictionary with one entry
                   "Image": image in base 64 string
    """
    r = request.get_json()
    username = r["username"]
    filename = r["filename"]
    extension = r["extension"]
    x = verify_newuser(username)
    if x is False:
        y = verify_newimage(filename, username)
        if y is False:
            I = find_image(filename, username)
            file = I["Image"]
            outfile = convert_file(file, extension)
            outstring = {"Image": read_data_as_b64(outfile)}
        else:
            outstring = "Image does not exist"
    else:
        outstring = "User does not exist"
    return jsonify(outstring)


@app.route("/api/get_histogram", methods=["GET"])
def get_histogram():
    """
    Server request for image of histogram
    Args:
        Input JSON:
            Username: username
            Filename: filename
    Returns:
        outstring: base 64 string of histogram image
    """
    r = request.get_json()
    username = r["username"]
    filename = r["filename"]
    x = verify_newuser(username)
    if x is False:
        y = verify_newimage(filename, username)
        if y is False:
            I = find_image(filename, username)
            file = I["Histogram"]
            outstring = {"Histogram": read_data_as_b64(file)}
        else:
            outstring = "Image does not exist"
    else:
        outstring = "User does not exist"
    return jsonify(outstring)


if __name__ == '__main__':
    """
    Execute the server
    """
    app.run()
