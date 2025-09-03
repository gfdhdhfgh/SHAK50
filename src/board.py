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
    
    canny = cv.Canny(blur, 50, 150)
    dilate = cv.dilate(canny, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)))

    grad = cv.morphologyEx(blur, cv.MORPH_GRADIENT, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=1)
    _, thresh = cv.threshold(grad, 100, 255, cv.THRESH_OTSU+cv.THRESH_BINARY)
    return thresh

def edge(img: cvt.MatLike):
    bgr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    blank = np.zeros(img.shape, dtype=np.uint8)
    lines = cv.HoughLinesP(img, 0.8, np.pi/160, 300, maxLineGap=50, minLineLength=200)
    if type(lines) != type(None):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(blank, (x1, y1), (x2, y2), (255, 0, 0), 2)
    return blank

def downsample(img: cvt.MatLike, percent: float) -> cvt.MatLike:
    w, h = img.shape[:2]
    size = cv.resize(img, (int(w*percent), int(h*percent)))
    return size

def tile(img: cvt.MatLike):
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if (1000 < cv.contourArea(contour) < 10000):
            eps = cv.arcLength(contour, False) * 0.2
            approx = cv.approxPolyDP(contour, eps, True)

            if (len(approx) == 4):
                cv.drawContours(img, [contour], -1, (0, 0, 255), 2)
            