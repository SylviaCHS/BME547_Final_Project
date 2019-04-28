import requests
import time
import datetime
import base64
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def main():
    ID = "Kim3"
    Image_List = []
    filename = "Reveille"
    extension = "png"
    filepathname = r"C:\Users\lenno\OneDrive\Documents\KimAndRev copy.png"
    user = {
        "username": ID,
        }
    r3 = requests.post("http://127.0.0.1:5000/api/new_user", json=user)
    print(r3.text)

    I = read_file_as_b64(filepathname)
    userimage = {
        "username": ID,
        "Image": I,
        "filename": filename,
        "extension": extension
    }
    r4 = requests.post("http://127.0.0.1:5000/api/new_image", json=userimage)
    print(r4.text)
    imjson = {
        "username": ID,
        "filename": filename
    }
    r5 = requests.get("http://127.0.0.1:5000/api/get_image", json=imjson)
    outfile = r5.json()
    I2_b64 = outfile["Image"]
    # print(I2_b64)
    save_b64_image(I2_b64)
    pjson = {
        "username": ID,
        "filename": filename,
        "process": "Histogram Equalization"
    }
    r6 = requests.post("http://127.0.0.1:5000/api/process_image", json=pjson)
    newfilename = filename + "_Histogram Equalization"
    imjson = {
        "username": ID,
        "filename": newfilename,
        "process": "Histogram Equalization"
    }
    print(r6.json())
    r7 = requests.get("http://127.0.0.1:5000/api/get_image", json=imjson)
    outfile = r7.json()
    # print(outfile)
    I2_b64 = outfile["Image"]
    # print(I2_b64)
    save_b64_image(I2_b64)
    metjson = {
             "username": ID
            }
    r = requests.get("http://127.0.0.1:5000/api/user_metrics", json=metjson)
    print(r.json())
    metjson = {
             "username": ID,
             "filename": newfilename
            }
    r = requests.get("http://127.0.0.1:5000/api/image_metrics", json=metjson)
    print(r.json())
    djson = {
        "username": ID,
        "filename": newfilename,
        "extension": "JPEG"
    }
    r = requests.get("http://127.0.0.1:5000/api/download_image", json=djson)
    print(r.json())
    outfile = r.json()
    I2_b64 = outfile["Image"]
    download_b64_image(I2_b64, "Reveille_HistogramEq.jpg")


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def save_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='tiff')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return i


def download_b64_image(base64_string, filename):
    image_bytes = base64.b64decode(base64_string)
    with open(filename, "wb") as out_file:
        out_file.write(image_bytes)
    return


if __name__ == "__main__":
    main()
