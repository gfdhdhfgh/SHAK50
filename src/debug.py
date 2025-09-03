import board
import cv2 as cv
import glob

def show(index: int):
    img = cv.imread(glob.glob("../test/*.*")[index-1])
    down = board.downsample(img, 0.5)
    proc = board.process_image(down)
    ed = board.edge(proc)
    til = board.tile(ed)
    cv.imshow("Test Preprocess", ed)

def main():
    file_amount = len(glob.glob("../test/*.*"))
    cv.namedWindow("Test Preprocess")
    cv.createTrackbar("Image", "Test Preprocess", 0, file_amount - 1, show)
    
    cv.imshow("Test Preprocess", cv.imread("../test/com_1.png"))
    while True:
        if ((cv.waitKey(0) & 0xFF) == ord("q")):
            cv.destroyAllWindows()
            break;
        
main()