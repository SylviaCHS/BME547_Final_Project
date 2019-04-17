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
app = Flask(__name__)
connect("mongodb+srv://Kim:Zs14nsnRcSzRJcOF@"
        "cluster0-cxyhs.mongodb.net/test?retryWrites=true")
for handler in logging.root.handlers[:]:  # This line makes the log file work
    logging.root.removeHandler(handler)
logging.basicConfig(filename="server_log.log", filemode="w",
                    level=logging.INFO)


class User(MongoModel):
    """
    MongoDB user class that stores heart rate,
    timestamp of all heart rate data, user age
    patient ID number (Primary key), and
    attending physician email address.
    """
    UserID = fields.CharField(primary_key=True)
    timestamp = fields.ListField()
    ImageFile = fields.ListField()
    Process = fields.ListField()
    Latency = fields.ListField()
    filename = fields.ListField()
