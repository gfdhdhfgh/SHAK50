import sqlite3 as sql
import uuid
import cv2 as cv
from flask import make_response
import os

def start_row(filename: str):
    conn = sql.connect("../queue.db")
    cursor = conn.cursor()
    res = cursor.execute("SELECT name FROM sqlite_master")
    if (res.fetchone()[0] != "task"):
        cursor.execute("CREATE TABLE task (Filename TEXT, Finished BOOL, Result TINYTEXT)")
    conn.execute("INSERT INTO task VALUES(?, FALSE, \"\")", (filename,))
    conn.commit()
    conn.close()

def delete_row(filename: str):
    conn = sql.connect("../queue.db")
    conn.execute("DELETE FROM task WHERE Filename=?;", (filename, ))
    conn.commit()
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