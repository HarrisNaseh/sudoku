import cv2
import numpy as np
import imutils
import model
import matplotlib.pyplot as plt
import sudoku

def warp_image(contours, orginal_pic, ratio):

    # contours = sorted(contours, key=cv2.contourArea, reverse=True)

    maxContour = contours[0]

    esp = 0.07 * cv2.arcLength(maxContour, True)
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
# img = cv2.imread("printed.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.imread("printed.jpg", cv2.IMREAD_GRAYSCALE)
ratio = img.shape[0] / 400.
org = img.copy()
img = imutils.resize(img, height = 400)

blur = cv2.GaussianBlur(img, (5,5), 1) 
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

warp = warp_image(contours, org, ratio)

# cv2.imshow("bryg", warp)

# cv2.waitKey()
# cv2.destroyAllWindows()
thresh = cv2.adaptiveThreshold(warp, 255, 1, 1, 11, 2)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# #The 81 biggest contours in the image is now the 81 squares of the sudoko
contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:82]

contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

solver = sudoku.sudoko_solver()
for i in range(0, 81, 9):
    row_contour = contours[i: i + 9]
    row_contour = sorted(row_contour, key= lambda ctr: cv2.boundingRect(ctr)[0])
    for q in range(len(row_contour)):
        x, y, w, h = cv2.boundingRect(row_contour[q])
        # Extract the square from the image
        square = warp[y:y+h, x:x+w]
        number = model.predict(square)

        if q < 3:
            solver.insert((i / 9), 0, number)
        elif q < 6: 
            solver.insert((i / 9), 1, number)
        else:
            solver.insert((i / 9), 2, number)
solver.solve()
print(solver.print_board())


















#used to show contours 

# print(solver.print_board())
# solver.solve()
# print(solver.print_board())                 
# img_color = cv2.cvtColor(warp, cv2.COLOR_GRAY2BGR)
# for i in range(len(contours)):
#     # Get the bounding rectangle for the contour
#     x, y, w, h = cv2.boundingRect(contours[i])

#     # Extract the square from the image
#     square = warp[y:y+h, x:x+w]

#     # number = model.predict(square)
#     # print("Predicted Number: ", number)
#     print(cv2.boundingRect(contours[i]))
#     cv2.drawContours(img_color, contours, i, (0, 255, 0) , 3)
#     cv2.imshow('warped', img_color)
#     # plt.imshow(img_color, cmap='Greys')
#     # plt.show()
#     cv2.waitKey(0)
    
#     cv2.destroyAllWindows()






    
