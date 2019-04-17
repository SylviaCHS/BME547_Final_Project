import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
from Mongo import User


# class Image:
    # def __init__(self, filename, image, process, timestamp, processtime):
        # self.filename = filename
        # self.image = image
        # self.process = process
        # self.timestamp = timestamp
        # self.processtime = processtime
        

ID = "Kim"
Image_List = []
time = datetime.datetime.now()
File = "Test.jpg"
Imagename = [1, 2,3, 4]
imageprocess = "None"
imagetimestamp= time
imageprocesstime = 0
#Image_List.append(Image(File, Imagename, imageprocess, imagetimestamp, imageprocesstime))
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
u = User(ID, time, Image_List, File)
u.save()