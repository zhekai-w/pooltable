import matplotlib.pyplot as plt
import numpy as np

angle = np.arange(0,1,0.01)
angle_weight = 1/(1+angle*1273)

length = np.arange(0,1,0.01)
length_weight = 1/(1+length*2000)

n = np.array([0,1/2,1])
n_weight = -n+1

plt.title("angle weight distro")
plt.plot(angle, angle_weight)
plt.show()

plt.title("length weight distro")
plt.plot(length,length_weight)
plt.show()

plt.title("n weight distro")
plt.step(n, n_weight)
plt.show()

plt.title("all weight distro")
plt.xlabel("normalize value(min to max)")
plt.ylabel("weight")
plt.plot(angle, angle_weight)
plt.plot(length,length_weight)
plt.step(n, n_weight)
plt.legend(['angle weight distro', 'length weight distro', 'n weight distro']) 
plt.show()