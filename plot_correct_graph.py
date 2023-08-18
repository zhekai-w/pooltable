import matplotlib.pyplot as plt
import numpy as np

# angle = np.arange(0,np.pi/2,0.1)
# angle_weight = -angle*1273 + 2000

# length = np.arange(0,2000,1)
# length_weight = - length + 2000

# n = np.array([0,1,2])
# n_weight = -n*1000 + 2000

#normalize x axis
angle = np.arange(0,1,0.01)
angle_weight = -angle*1273*(np.pi/2) + 2000

length = np.arange(0,1,0.01)
length_weight = - length*2000 + 2000

n = np.array([0,1/2,1])
n_weight = -n*2000 + 2000

plt.title("angle weight distro")
plt.xlabel("angle in radian/(pi/2)")
plt.ylabel("weight")
plt.plot(angle, angle_weight)
plt.show()

plt.title("length weight distro")
plt.xlabel("length in pixel/2000")
plt.ylabel("weight")
plt.plot(length,length_weight)
plt.show()

plt.title("n weight distro")
plt.xlabel("number of interrupting balls/2")
plt.ylabel("weight")
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