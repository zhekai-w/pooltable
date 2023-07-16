import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

# cv2 to do image prosseccing
#matplot to show but why ? because matplot auto resized image to show and remain the same dimensions

img = plt.imread('/home/zack/IDPoolBall/filter table pics/GOPR0435.JPG')
plt.imshow(img)

click_event_list = [[]*2]

def on_move(event):
    if event.inaxes:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')


# def on_click(event):
#     if event.button is MouseButton.RIGHT:
#         print('disconnecting callback')
#         plt.disconnect(binding_id)

def save_on_click(event):
    if event.button is MouseButton.LEFT:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')
        print("click saved")
        #save xdata and ydate to list
        click_event_list.append([event.xdata, event.ydata])


binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', save_on_click)
plt.show()
#delete first index of list cuz it's 0 somehow
del click_event_list[0]
print(click_event_list)
#convert list to numpy array
click_event = np.array(click_event_list)
round_clickpoint = np.around(click_event, decimals=0)
print(click_event)
print(round_clickpoint)


