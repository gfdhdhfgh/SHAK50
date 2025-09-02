import board
import cv2 as cv
import glob

def show(index: int):
    img = cv.imread(glob.glob("../test/*.*")[index-1])
    proc = board.process_image(img)
    ed = board.edge(proc)
    cv.imshow("Test Preprocess", ed)

def main():
    file_amount = len(glob.glob("../test/*.*"))
    cv.namedWindow("Test Preprocess")
    cv.createTrackbar("Image", "Test Preprocess", 0, file_amount, show)
    
    cv.imshow("Test Preprocess", cv.imread("../test/com1.png"))
    while True:
        if ((cv.waitKey(0) & 0xFF) == ord("q")):
            cv.destroyAllWindows()
            break;
        
main()