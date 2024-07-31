import cv2
import numpy as np
import imutils
 

def warp_image(contours, orginal_pic):

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    maxContour = contours[0]

    esp = 0.015 * cv2.arcLength(maxContour, True)
    approx = cv2.approxPolyDP(maxContour, esp, True)

    pts = approx.reshape(4, 2)

    rect = np.zeros((4, 2), dtype= "float32")

    s = pts.sum(axis= 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)

    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    rect *= ratio

    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orginal_pic, M, (maxWidth, maxHeight))

    return warp

# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("handwritten.png", cv2.IMREAD_GRAYSCALE)
# im2 = cv2.imread("Media.jpg", cv2.IMREAD_GRAYSCALE)
ratio = img.shape[0] / 400.
org = img.copy()
img = imutils.resize(img, height = 400)

blur = cv2.GaussianBlur(img, (5,5), 0) 
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

warp = warp_image(contours, org)

thresh = cv2.adaptiveThreshold(warp, 255, 1, 1, 11, 2)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)



img_color = cv2.cvtColor(warp, cv2.COLOR_GRAY2BGR)
cv2.drawContours(img_color, contours, 10, (0, 255, 0) , 3)

cv2.imshow('warped', img_color)

cv2.waitKey(0)
cv2.destroyAllWindows()






    
