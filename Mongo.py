import os
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
import numpy as np
import datetime
import math
app = Flask(__name__)
connect("mongodb+srv://Kim:Zs14nsnRcSzRJcOF@"
        "cluster0-cxyhs.mongodb.net/test?retryWrites=true")


class User(MongoModel):
    """
    Class that stores UserID, timestamp, and images
    for multiple users
    """
    UserID = fields.CharField(primary_key=True)
    timestamp = fields.ListField()
    ImageFile = fields.ListField()
    filenames = fields.ListField()
    raw_image = fields.ListField()
