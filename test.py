import cv2
 
# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("Media.jpg", cv2.IMREAD_GRAYSCALE)
blur = cv2.GaussianBlur(img, (7,7), 0) 
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
# contours, mat = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# print(len(contours))

cv2.imshow('Gaussian', thresh) 
cv2.waitKey(0) 
# Creating GUI window to display an image on screen
# first Parameter is windows title (should be in string format)
# Second Parameter is image array
# cv2.imshow("image", thresh)

  


 
# To hold the window on screen, we use cv2.waitKey method
# Once it detected the close input, it will release the control
# To the next line
# First Parameter is for holding screen for specified milliseconds
# It should be positive integer. If 0 pass an parameter, then it will
# hold the screen until user close it.
cv2.waitKey(0)
 
# It is for removing/deleting created GUI window from screen
# and memory
cv2.destroyAllWindows()


