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

def display_color(light, dark):
    l_square = np.full((10, 10, 3), light, dtype=np.uint8) / 255.0
    d_square = np.full((10, 10, 3), dark, dtype=np.uint8) / 255.0
    plt.subplot(1, 2, 1)
    plt.imshow(l_square)
    plt.subplot(1, 2, 2)
    plt.imshow(d_square)
    plt.show()

def plot_3dspace(img):
    r, g, b = cv2.split(img)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red or Hue")
    axis.set_ylabel("Green or Saturation")
    axis.set_zlabel("Blue or Value")
    plt.show()

def show_image(img):
    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyWindow("img")

img_cv = cv2.imread('/home/zack/IDPoolBall/poolballs2.jpeg')
img_plt = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

plt.imshow(img_plt)
plt.show()

# plot_3dspace(img_plt)

#DEFINE BILLARD BALL COLOR
light_red = (255,100,100)
dark_red = (100,0,0)
display_color(light_red, dark_red)

pure_white = (255,255,255)
off_white = (215,215,215)
display_color(pure_white, off_white)

off_black = (40,40,40)
pure_black = (0,0,0)
display_color(off_black, pure_black)



red_mask = cv2.inRange(img_plt, dark_red, light_red)
white_mask = cv2.inRange(img_plt, off_white, pure_white)
black_mask = cv2.inRange(img_plt, pure_black, off_black)
# show_image(red_mask)
# show_image(white_mask)
# show_image(black_mask)
result = cv2.bitwise_and(img_plt, img_plt, mask=red_mask+white_mask+black_mask)
plt.imshow(result)
plt.show()

