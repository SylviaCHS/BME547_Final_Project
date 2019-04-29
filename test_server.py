import pytest
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


def test_process_image():
    from server import process_image
    image = np.ones([2, 2], dtype=np.uint8)
    his_eq = Process.his_eq(image)
    [improcess, latency] = process_image(image, "Histogram Equalization")
    improcess = np.asarray(improcess)
    his_eq = np.asarray(improcess)
    assert his_eq.all() == improcess.all()


def test_find_stats1():
    from server import find_stats
    data_list = []
    data = {
            "Process": "Histogram Equalization",
            "Latency": 0
            }
    data2 = {
            "Process": "Histogram Equalization",
            "Latency": 1
            }
    data3 = {
            "Process": "Reverse Video",
            "Latency": 2
            }
    data_list.append(data)
    data_list.append(data2)
    data_list.append(data3)
    A = find_stats("Histogram Equalization", data_list)
    assert A["Mean latency"] == 0.5


def test_find_stats2():
    from server import find_stats
    data_list = []
    data = {
            "Process": "Histogram Equalization",
            "Latency": 0.0
            }
    data2 = {
            "Process": "Histogram Equalization",
            "Latency": 1.0
            }
    data3 = {
            "Process": "Reverse Video",
            "Latency": 2.0
            }
    data_list.append(data)
    data_list.append(data2)
    data_list.append(data3)
    A = find_stats("Histogram Equalization", data_list)
    assert A["Times used"] == 2


def test_verify_newuser1():
    from server import verify_newuser
    users = ["Kim", "Sylvia", "Tiffany"]
    x = verify_newuser(users, "Kim")
    assert x is False


def test_verify_newuser2():
    from server import verify_newuser
    users = ["Kim", "Sylvia", "Tiffany"]
    x = verify_newuser(users, "Bob")
    assert x is True


def test_verify_newimage1():
    from server import verify_newimage
    files = ["A", "B", "C", "D"]
    x = verify_newimage("A", files)
    assert x is False


def test_verify_newimage2():
    from server import verify_newimage
    files = ["A", "B", "C", "D"]
    x = verify_newimage("E", files)
    assert x is True


def test_read_data_as_b64():
    from server import read_data_as_b64
    a = bytes([1, 2, 3, 4])
    b64_string = read_data_as_b64(a)
    expected = 'AQIDBA=='
    assert b64_string == expected
