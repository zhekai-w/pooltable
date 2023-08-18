import cv2
import numpy as np

def split_channels(img):
    (B,G,R) = cv2.split(img)
    return B,G,R

def convert_format(img , t_format):
    if t_format == 'Gray':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if t_format == 'HSV':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if t_format == 'HSV':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else: 
        print("Error")
    return img

def show_img(img,time):
    cv2.namedWindow('test',cv2.WINDOW_FREERATIO)
    cv2.imshow('test',img)
    cv2.waitKey(time)


def filter(src):
    imgG = cv2.GaussianBlur(src, (5, 5),0)
    imgM = cv2.medianBlur(src, 7)
    imgB = cv2.bilateralFilter(src, 51, 10, 10)
    return imgG,imgM,imgB

def do_canny(img):
    canny = cv2.Canny(img,30,200)
    return canny


img = cv2.imread('/home/zack/IDPoolBall/filter table pics/poolballs2.jpeg', cv2.IMREAD_COLOR)
print('Original Dimensions : ',img.shape)
scale_percent = 400 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# cimg = convert_format(resized, 'Gray')
# show_img(cimg,3000)
# imgG, imgM,imgB = fliter(cimg)
# show_img(imgM,3000)
# cannyimg =do_canny(imgM)
# show_img(cannyimg,3000)
# kernal = np.ones((31,31),np.uint8)
# dilateimg = cv2.dilate(cannyimg,kernal,1)
# show_img(dilateimg,3000)

#Convert to HSV
imgG, imgM,imgB = filter(img)
org_cannyed = do_canny(img)
# cv2.imshow("aaa", org_cannyed)
# cv2.waitKey(5000)
# cv2.imshow("aaa",imgG)
# cv2.waitKey(2000)
# cv2.imshow("aaa",imgM)
# cv2.waitKey(2000)
# cv2.imshow("aaa",imgB)
# cv2.waitKey(2000)
Hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imshow("aaa",Hsv)
# cv2.imwrite('/home/zack/IDPoolBall/Hsv.jpeg',Hsv)
cv2.waitKey(10000)
H, S, V = cv2.split(Hsv)
# cv2.imshow("aaa",H)
# cv2.imwrite('/home/zack/IDPoolBall/Hsv_H.jpeg',H)
# cv2.waitKey(2000)
# cv2.imshow("aaa",S)
# cv2.imwrite('/home/zack/IDPoolBall/Hsv_S.jpeg',S)
# cv2.waitKey(2000)
# cv2.imshow("aaa",V)
# cv2.imwrite('/home/zack/IDPoolBall/Hsv_V.jpeg',V)
# cv2.waitKey(2000)
A, B, C = filter(img)
cv2.imshow("aaa",B)
cv2.waitKey(2000)
#cv2.imwrite('/home/zack/IDPoolBall/medianBlur.jpeg',B)
cannyed = do_canny(img)
cv2.imshow("aaa",cannyed)
cv2.waitKey(10000)
#cv2.imwrite('/home/zack/IDPoolBall/org_cannyed.jpeg',cannyed)
# cv2.waitKey(2000)



# #Read image
# img = cv2.imread('/home/zack/IDPoolBall/poolballs1.jpeg',cv2.IMREAD_COLOR)

# #Convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("aaa",gray)
# cv2.imwrite('/home/zack/IDPoolBall/gray.jpeg',gray)
# cv2.waitKey(2000)

# #Blur using 3*3 kernal
# gray_blurred = cv2.blur(gray,(3,3))
# cv2.imshow("aaa",gray_blurred)
# cv2.imwrite('/home/zack/IDPoolBall/gray_blurred.jpeg',gray_blurred)
# cv2.waitKey(2000)

# # Apply Hough transform on the blurred image.
# detected_circles = cv2.HoughCircles(gray_blurred, 
#                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
#                param2 = 30, minRadius = 1, maxRadius = 40)

# cv2.imshow("aaa",detected_circles)
# cv2.imwrite('/home/zack/IDPoolBall/detected_circles.jpeg',detected_circles)
# cv2.waitKey(2000)

#Draw circles that are detected
# if detected_circles is not None:

#     #Convert the circle parameters a, b and r to intergers
#     detected_circles = np.uint16(np.around(detected_circles))

#     for pt in detected_circles[0, :]:
#         a, b, r = pt[0], pt[1], pt[2]

#         #Draw the circumference of the circles
#         cv2.circle(img, (a,b), r, (0, 255, 0), 2)

#         #Draw a small circle (of radius 1) t show the center
#         cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
#         cv2.imshow("Detected Circle", img)
#         cv2.waitKey(0)