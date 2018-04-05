import numpy as np
import argparse
import cv2

# Name of Video to Open. Works well on 1,2,6
videonumber = 1
url = ('Videos/video' + str(videonumber) + '.mp4')

# Loading Video
cap = cv2.VideoCapture(url)
ret, image = cap.read()
lv = 0
rv = 0
while(True):
    if (cap.isOpened()):
        try:
            # Reads image of video and adds border to remove horizon
            ret, image = cap.read()
            image2 = image[430:720,0:960]
            bordersize = 430
            image2 = cv2.copyMakeBorder(image2, top = bordersize, bottom = 0, left = 0, right = 0, borderType = cv2.BORDER_CONSTANT, value = [0,0,0])

            # Define Colour boundaries and apply masks
            # Will need to work with hsl values instead of rgb for better accuracy
            grey_image = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            lower_purple = np.array([90,70,100], dtype = "uint8")
            upper_purple = np.array([165,130,210], dtype = "uint8")
            lower_yellow = np.array([100,200,200], dtype = "uint8")
            upper_yellow = np.array([180,255,255], dtype = "uint8")
            lower_blue = np.array([100, 40, 4], dtype="uint8")
            upper_blue = np.array([255, 185, 80], dtype="uint8")
            mask_blue = cv2.inRange(image, lower_blue, upper_blue)
            mask_yellow = cv2.inRange(image, lower_yellow, upper_yellow)
            mask_purple = cv2.inRange(image, lower_purple, upper_purple)
            mask_yw = cv2.bitwise_or(mask_blue, mask_yellow)

            mask_image = cv2.bitwise_and(grey_image, mask_yw)
            mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR) #need 3 colour chanels for hstack

            # Smooth out the image
            kernel_size = 5
            blur_image = cv2.GaussianBlur(mask_image, (kernel_size, kernel_size), 0)

            # Basic Edge Detection (not implemented)
            low_threshold = 50
            high_threshold = 150
            canny_image = cv2.Canny(blur_image, low_threshold, high_threshold)
            canny_image = cv2.cvtColor(canny_image, cv2.COLOR_GRAY2BGR)

            # Stack source image with lane image and display
            def laneDetect(numbers):
                numbers = numbers.flatten()
                value = 0
                count = 0
                for i in range(300):
                    if (numbers[i] > 0):
                        value = value + 1 * i
                        count = count + 1
                if(count > 0):
                    value = (int) (value / count)
                return value

            leftPixels =  cv2.cvtColor(blur_image[500:501,100:400], cv2.COLOR_BGR2GRAY)
            rightPixels =  cv2.cvtColor(blur_image[500:501, (960 - 400): (960 - 100)], cv2.COLOR_BGR2GRAY)
            if(laneDetect(leftPixels) > 0 or lv == None):
                lv = laneDetect(leftPixels)
            if(laneDetect(rightPixels) > 0 or rv == None):
                rv = laneDetect(rightPixels)


            #cv2.line(image, (100,500), (400, 500), (0,255,0), 2, 8, 0)
            #cv2.line(image, (960 - 400,500), (960 - 100, 500), (0,255,0), 2, 8, 0)
            cv2.line(blur_image, (100,500), (400, 500), (0,255,0), 2, 8, 0)
            cv2.line(blur_image, (960 - 400,500), (960 - 100, 500), (0,255,0), 2, 8, 0)

            cv2.line(blur_image, ((100 + lv), 450), ((100 + lv), 550 ) , (255,100,0), 2, 8, 0)
            cv2.line(blur_image, ((560 + rv), 450), ((560 + rv), 550 ) , (255,100,0), 2, 8, 0)






            display = np.hstack((image, blur_image))
            display = cv2.resize(display, (1080,500))
            cv2.imshow("Lane Detection", display)
            cv2.waitKey(50)



        except cv2.error as e:
            print("Couldnt load next image: %s" % (e))
    else:
        print("----------unable to open cap. incoming crash----------------")

        exit()
