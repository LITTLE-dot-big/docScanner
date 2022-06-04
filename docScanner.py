import cv2 as cv
import numpy as np


#####################################################################################################
clr = (0, 0, 255)
ks = 7
thr = 30
sigx = 1
itr = 1
krn = 3
biggest = np.array([])
maxArea = 0
#####################################################################################################


def empty(a):
    pass


def initTrackbars():
    cv.namedWindow('trackbars')
    cv.createTrackbar('thr-canny', 'trackbars', 30, 200, empty)
    cv.createTrackbar('sigx-blur', 'trackbars', 1, 30, empty)
    cv.createTrackbar('itr-erode', 'trackbars', 1, 5, empty)
    cv.createTrackbar('krn-erode', 'trackbars', 3, 10, empty)


def readTracbars():
    global ks, thr, sigx, itr, krn
    thr = cv.getTrackbarPos('thr-canny', 'trackbars')
    sigx = cv.getTrackbarPos('sigx-blur', 'trackbars')
    itr = cv.getTrackbarPos('itr-erode', 'trackbars')
    krn = cv.getTrackbarPos('krn-erode', 'trackbars')


def preProcessing(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (ks, ks), sigx)
    canny = cv.Canny(blur, thr, thr)
    dilate = cv.dilate(canny, np.ones((krn, krn)), iterations=itr)
    erode = cv.erode(dilate, np.ones((krn, krn)), iterations=itr)
    cv.imshow('canny', canny)
    cv.imshow('dilate', dilate)
    cv.imshow('erode', erode)
    return erode


def getBigContours(img):
    global maxArea, biggest
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 5000:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    cv.drawContours(doc, biggest, -1, clr, 30)
    cv.imshow('doc', doc)
    return biggest


if __name__ == '__main__':
    initTrackbars()
    cap = cv.VideoCapture(0)
    while True:
        readTracbars()
        status, doc = cap.read()
        if status:
            processed = preProcessing(doc)
            biggest = getBigContours(processed)

        k = cv.waitKey(1)
        if k > 13:
            break
