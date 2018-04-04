import numpy as np
import argparse
import cv2
import tkinter

url = 'video1.mp4'

try:
    cap = cv2.VideoCapture(url)
    ret, image = cap.read()
except:
    print("error opening video")
while(True):
    if (cap.isOpened()):
        try:
            ret, image = cap.read()
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #lower_blue = np.array([66,100,100], dtype = "uint8")
            #upper_blue = np.array([130,255,255], dtype = "uint8")
            lower_blue = np.array([100, 40, 4], dtype="uint8")
            upper_blue = np.array([250, 170, 80], dtype="uint8")
            mask_blue = cv2.inRange(image, lower_blue, upper_blue)
            # mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

            mask_b_image = cv2.bitwise_and(grey_image, mask_blue)
            cv2.imshow("image", mask_b_image)
            cv2.waitKey(50)

        except cv2.error as e:
            print("Couldnt load next image: %s" % (e))

    else:
    	print("----------unable to open cap. incoming crash----------------")


image = cv2.imread("image.png")

#Below is assorted shit that i may use
# yellowboundary = ([66, 20, 4], [250, 170, 80])
# blueboundary = ([100, 150, 150], [150, 255, 255])
# # loop over the boundaries
# lower, upper = blueboundary
# lower = np.array(lower, dtype = "uint8")
# upper = np.array(upper, dtype = "uint8")
#
# mask = cv2.inRange(image, lower, upper)
# outputb = cv2.bitwise_and(image, image, mask = mask)
#
# lower, upper = yellowboundary
# lower = np.array(lower, dtype = "uint8")
# upper = np.array(upper, dtype = "uint8")
#
# mask = cv2.inRange(image, lower, upper)
# outputy = cv2.bitwise_and(image, image, mask = mask)
#
# cv2.imshow("images", np.hstack([image, outputb, outputy]))
# cv2.waitKey(0)

# for (lower, upper) in boundaries:
#     # create NumPy arrays from the boundaries
#     lower = np.array(lower, dtype = "uint8")
#     upper = np.array(upper, dtype = "uint8")
#     # find the colors within the specified boundaries and apply
#     # the mask
#     mask = cv2.inRange(image, lower, upper)
#     output = cv2.bitwise_and(image, image, mask = mask)
#
#     # show the images
#     p = tkinter.Tk()
#     while(True):
#         (xpos,ypos) = p.winfo_pointerxy()
#         if (xpos > 1348):
#             xpos = 1348
#         if (ypos > 786):
#             ypos = 786
#         print(image[ypos,xpos])
#         #print(image.shape)
#         #cv2.circle(image, (xpos,ypos), 1, (40,255,40),3,8,0)
#
#         cv2.waitKey(1)
#         cv2.imshow("images", np.hstack([image, output]))
