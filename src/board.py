import cv2 as cv
import cv2.typing as cvt
import numpy as np
import numpy.typing as npt

from matplotlib import pyplot as plt
import glob

plt.rcParams["image.cmap"] = "gray"

def load_image(filename: str) -> cvt.MatLike:
    try:
        file = glob.glob(f"{filename}.*")[0]
        img = cv.imread(file)
        return img
    except:
        raise FileNotFoundError("File not found")
    
def process_image(img: cvt.MatLike) -> cvt.MatLike:
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    
    clahe = cv.createCLAHE(2.0, (8, 8))
    equal = clahe.apply(blur)
    
    grad = cv.morphologyEx(equal, cv.MORPH_GRADIENT, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=1)
    grad_blur = cv.GaussianBlur(grad, (5, 5), 0)
    _, thresh = cv.threshold(grad_blur, 100, 255, cv.THRESH_OTSU+cv.THRESH_BINARY)
    return thresh

def edge(img: cvt.MatLike):
    bgr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    lines = cv.HoughLinesP(img, 0.8, np.pi/160, 300, maxLineGap=100, minLineLength=200)
    if type(lines) != type(None):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(bgr, (x1, y1), (x2, y2), (255, 0, 0), 2)
    return bgr