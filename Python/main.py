#!/usr/bin/python3

import cv2

from picamera2 import Picamera2
from libcamera import Transform
from datetime import datetime


import serial
import time

ser = serial.Serial('/dev/ttyUSB0',115200)

print("Init serial ",ser.name)

time.sleep(1)

print(ser.readline())

start_time = time.time()
# Grab images as numpy arrays and leave everything else to OpenCV.

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)},transform=Transform(vflip=True,hflip=True)))
picam2.start()

greenLower = (40, 86, 6)
greenUpper = (85, 255, 255)

r_max=120
r_min=90

x_max=640/2+60
x_min=640/2-60

now=datetime.now()

dt_string_filename = now.strftime("log/%Y-%m-%d_%H-%M_exp_log.csv")

f=open(dt_string_filename,"a")
f.write("X;Y;R;T\n")

while True:
    
    try:
        im = picam2.capture_array()

        blurred = cv2.GaussianBlur(im, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found

        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid

            area=0
            c=None

            for c_t in cnts:

                area_t = cv2.contourArea(c_t)
                if area_t > area:
                    area = area_t
                    c = c_t

                
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(im, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(im, center, 5, (0, 0, 255), -1)
                
                log = "Target position x:{:4.1f} y:{:4.1f} r:{:4.1f}".format(center[0],center[1],radius)
                f.write("{:4.2f};{:4.2f};{:4.2f};{:8.4f}\n".format(center[0],center[1],radius,time.time()-start_time))
                print(log)
                Lcom=0
                Rcom=0

                if radius < r_min :
                    Lcom+=1
                    Rcom+=1
                if radius > r_max :
                    Lcom-=1
                    Rcom-=1
                if center[0] > x_max:
                    Lcom+=0
                    Rcom-=1

                if center[0] < x_min:
                    Lcom-=1
                    Rcom+=0

                ser.write(bytes("R{}L{}\r\n".format(Rcom,Lcom),   'utf-8'))
                time.sleep(0.2)

    except KeyboardInterrupt:

        f.close()
        break

#    cv2.imshow("Camera", im)
#    cv2.imshow("mask", mask)
#    cv2.waitKey(1)
