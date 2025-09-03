import sqlite3 as sql
import uuid
import cv2 as cv
from flask import make_response
import os

def db():
    conn = sql.connect("../queue.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS task(name TEXT, finished BOOL, result TINYTEXT)")
    res = cursor.execute("INSERT INTO task VALUES(?)", "fish", False, "")
    conn.commit()
    res.fetchall()
    print(res)
    conn.close()

def add_image(img: bytes):
    id = uuid.uuid4().hex
    with open(f"../data/{id}.img", "wb") as f:
        f.write(img)
    pic = cv.imread(f"../data/{id}.img")
    print(pic.shape)

    if type(pic) == type(None):
        os.remove(f"../data/{id}.img")
        return make_response("Not an image", 400)
    return id

db()