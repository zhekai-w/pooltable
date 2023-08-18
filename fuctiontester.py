import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

  
x1, y1 = [-1, 12], [1, 4]
x2, y2 = [1, 10], [3, 2]
plt.plot(x1, y1, x2, y2, color='black', marker = 'o')
plt.show()


maxL = math.sqrt(abs(1920)**2+abs(914)**2)

Vx = [[0]*6]*5
print(Vx)
print(maxL)

