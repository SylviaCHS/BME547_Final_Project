import logging
import os
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
from Mongo import User

ID = "Kim"
Image_List = []
time = datetime.datetime.now()
File = "Test.jpg"
Imagename = [1, 2, 3, 4]
imageprocess = "None"
imagetimestamp = time
imageprocesstime = 0
Image_Dict = {
                "File": File,
                "Image": Imagename,
                "Process": imageprocess,
                "Timestamp": time,
                "Latency": imageprocesstime
                }
Image_List.append(Image_Dict)
process = ["None", "None"]
latency = [0, 0]
u = User(ID, timestamp=time, ImageFile=Image_List, filenames=File)
u.save()
