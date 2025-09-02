import sqlite3 as sql
import uuid
import cv2 as cv
from flask import make_response
import os

def add_image(img: bytes):
    id = uuid.uuid4().hex
    with open(f"../data/{id}.img", "wb") as f:
        f.write(img)
    pic = cv.imread(f"../data/{id}.img")
    print(pic.shape)
    if type(pic) == type(None):
        #os.remove(f"../data/{id}.img")
        return make_response("Not an image", 400)
    return id