from flask import Flask
from pymodm import connect
from pymodm import MongoModel, fields
app = Flask(__name__)
connect("mongodb+srv://Sylvia:Ks0l8NyUGEBzhZ2Y@bme547-zlm8s.mongodb."
        "net/test?retryWrites=true")


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
