import numpy as np
import cv2 as cv2
import os


class ShapeDetection:
    def createEllipse(self,imageEllipse,angle,center,axes): 
        self.imageEllipse=imageEllipse
        self.center=center
        self.axes=axes
        self.angle=angle
        self.imageEllipse = cv2.ellipse(self.imageEllipse, self.center, self.axes, self.angle, 0., 360, (0,0,0))
        self.imageEllipse = 255 * self.imageEllipse # Now scale by 255
        self.finalImage = self.imageEllipse.astype(np.uint8)
        return self.finalImage
    #Check if shape is open
    def ShapeOpen(self,src_img_open):
        self.shape_open_check=False
        self.src = src_img_open
        #Transform source image to gray if it is not already
        if len(self.src.shape) != 2:
            self.gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        else:
            self.gray = self.src
        self.ret, self.thresh = cv2.threshold(self.gray, 200, 255, cv2.THRESH_BINARY_INV)
        self.contours, self.hierarchy = cv2.findContours(self.thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        self.hierarchy = self.hierarchy[0]
        for i, c in enumerate(self.contours):
            if self.hierarchy[i][2] < 0 and self.hierarchy[i][3] < 0:
                self.shape_open_check=True
        return self.shape_open_check
    #Close the shape
    def CloseShape(self,src_img,x,y):
        self.x=x
        self.y=y
        self.src_img_closing_gray=src_img
        self.img_BW_closing =cv2.bitwise_not(self.src_img_closing_gray)
        self.kernel = np.ones((self.x,self.y),np.uint8)
        self.closing = cv2.morphologyEx(self.img_BW_closing, cv2.MORPH_CLOSE, self.kernel)
        return self.closing
    #Contour detection
    def ContourDetection(self,image_invest):
        self.image_invest_gray=image_invest
        if len(self.image_invest_gray.shape) != 2:
            self.image_invest_gray = cv2.cvtColor(self.image_invest_gray, cv2.COLOR_BGR2GRAY)
        else:
            self.image_invest_gray = self.image_invest_gray
        self.image_invest_gray = cv2.bitwise_not(self.image_invest_gray)
        self.thresh_con_detect=cv2.threshold(self.image_invest_gray,70,255,cv2.THRESH_BINARY)[1]
        self.contoursDetect,self.hierarchy=cv2.findContours(self.thresh_con_detect,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contoursDetect[0]
    #Comparison
    def ContourComparison(self,cnt,cnt_2):
        self.cnt=cnt
        self.cnt_2=cnt_2
        self.match=cv2.matchShapes(self.cnt,self.cnt_2,2,0.0) 
        return self.match
    #Detect Shapes
    def detect(self,c):
        self.c=c
        # initialize the shape name and approximate the contour
        self.shapeDetect = "unidentified"
        self.peri = cv2.arcLength(self.c, True)
        self.approx = cv2.approxPolyDP(self.c, 0.04 * self.peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(self.approx) == 3:
            self.shapeDetect = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(self.approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (self.x, self.y, self.w, self.h) = cv2.boundingRect(self.approx)
            self.ar = self.w / float(self.h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            self.shapeDetect = "square" if self.ar >= 0.95 and self.ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(self.approx) == 5:
            self.shapeDetect = "pentagon"
        # otherwise, we assume the shape is a circle
        else:
            self.shapeDetect = "circle"
        # return the name of the shape
        return self.shapeDetect

