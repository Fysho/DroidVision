import numpy as np
import argparse
import cv2
import tkinter
videonumber = 1
url = ('video' + str(videonumber) + '.mp4')

try:
    cap = cv2.VideoCapture(url)
    ret, image = cap.read()
except:
    print("error opening video")
while(True):
    if (cap.isOpened()):
        try:
            ret, image = cap.read()
            image2 = image[430:720,0:960]
            bordersize = 430
            image2 = cv2.copyMakeBorder(image2, top = bordersize, bottom = 0, left = 0, right = 0, borderType = cv2.BORDER_CONSTANT, value = [0,0,0])

            grey_image = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            lower_yellow = np.array([100,200,200], dtype = "uint8")
            upper_yellow = np.array([160,255,255], dtype = "uint8")
            lower_blue = np.array([100, 40, 4], dtype="uint8")
            upper_blue = np.array([250, 170, 80], dtype="uint8")
            mask_blue = cv2.inRange(image, lower_blue, upper_blue)
            mask_yellow = cv2.inRange(image, lower_yellow, upper_yellow)
            mask_yw = cv2.bitwise_or(mask_blue, mask_yellow)

            mask_image = cv2.bitwise_and(grey_image, mask_yw)
            mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)

            kernel_size = 15
            blur_image = cv2.GaussianBlur(mask_image, (kernel_size, kernel_size), 0)
            #mask_image = cv2.filter2D(mask_image,0,kernel_size)

            low_threshold = 50
            high_threshold = 150
            canny_image = cv2.Canny(blur_image, low_threshold, high_threshold)
            canny_image = cv2.cvtColor(canny_image, cv2.COLOR_GRAY2BGR)

            display = np.hstack((image, blur_image))
            display = cv2.resize(display, (1080,500))
            cv2.imshow("image", display)
            cv2.waitKey(50)



        except cv2.error as e:
            print("Couldnt load next image: %s" % (e))

    else:
    	print("----------unable to open cap. incoming crash----------------")
