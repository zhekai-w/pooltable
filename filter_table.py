import cv2 
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

def filter(src):
    imgG = cv2.GaussianBlur(src, (5, 5),0)
    imgM = cv2.medianBlur(src, 1)
    imgB = cv2.bilateralFilter(src, 51, 10, 10)
    return imgG,imgM,imgB

def do_canny(img):
    canny = cv2.Canny(img,30,200)
    return canny


img = cv2.imread('/home/zack/IDPoolBall/poolballs2.jpeg')


pool = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv_pool = cv2.cvtColor(pool, cv2.COLOR_RGB2HSV)
G, M, B = filter(pool)
# plt.imshow(M)
# plt.show()
 
# #PLOT R,G,B OR H,S,V VALUE IN 3D 
# r, g, b = cv2.split(M)
# fig = plt.figure()
# axis = fig.add_subplot(1, 1, 1, projection="3d")
# pixel_colors = M.reshape((np.shape(M)[0]*np.shape(M)[1], 3))
# norm = colors.Normalize(vmin=-1.,vmax=1.)
# norm.autoscale(pixel_colors)
# pixel_colors = norm(pixel_colors).tolist()
# axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
# axis.set_xlabel("Red")
# axis.set_ylabel("Green")
# axis.set_zlabel("Blue")
# plt.show()

light_green = (100,255,150)
dark_green = (3,80,30)

lo_square = np.full((10, 10, 3), light_green, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_green, dtype=np.uint8) / 255.0
# plt.subplot(1, 2, 1)
# plt.imshow(lo_square)
# plt.subplot(1, 2, 2)
# plt.imshow(do_square)
# plt.show()

mask = cv2.inRange(M, dark_green, light_green)
cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.destroyWindow("mask")
result = cv2.bitwise_and(M, M, mask=mask)

# plt.subplot(1, 2, 1)
# plt.imshow(mask, cmap="gray")
# cv2.imwrite('/home/zack/IDPoolBall/mask.jpeg',mask)
# plt.show()
# plt.subplot(1, 2, 2)
# plt.imshow(M-result)
# cv2.imwrite('/home/zack/IDPoolBall/M.jpeg',M-result)
# plt.show()

imgM = cv2.medianBlur(mask, 7)
cv2.imshow("imgM", imgM)
cv2.waitKey(0)
cv2.destroyWindow("imgM")
    
cannyed = do_canny(imgM)
cv2.imshow("cannyed", cannyed)
cv2.waitKey(0) 
cv2.destroyWindow("cannyed")

## TO CHANGE RGB TO BGR FOR OPENCV
# h = cv2.cvtColor(M-result, cv2.COLOR_RGB2BGR)
# cv2.imshow("aaa",h)
# cv2.imwrite('/home/zack/IDPoolBall/M1.jpeg',h)
# cv2.waitKey(0)
