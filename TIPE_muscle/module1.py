import numpy as np
import cv2 as cv

circless = []
for loop in range(100) :
    img = cv.imread(r"D:\tipe2\bulle00"+str(108000+loop)+".jpg",0)
    #img = cv.medianBlur(img,5)
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=60,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:][:2]:
        print(i)
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    circless.append(cimg)
for i in range(100) :
    cv.imshow('detected circles',circless[i])
cv.waitKey(0)
cv.destroyAllWindows()
