import math
import numpy as np
import os
import cv2

from ._ShapeDetection import ShapeDetection
from ._funcitons_shape_detect import Cropping

def SimilarityFinder(image_storage_intermed):
        sdetect=ShapeDetection()
        image = np.ones((400, 400, 3)) 
        sdetect=ShapeDetection()
        angle=-45
        center = (200, 200) # x,y
        axes = (200, 75) # first, second
        img_ellipse_comp=sdetect.createEllipse(image,angle,center,axes)

        angle=-45
        center = (200, 200) # x,y
        axes = (200, 100) # first, second
        img_ellipse_comp_1=sdetect.createEllipse(image,angle,center,axes)

        angle=-45
        center = (200, 200) # x,y
        axes = (200, 40) # first, second
        img_ellipse_comp_2=sdetect.createEllipse(image,angle,center,axes)
        #ellipse
        cnt_ellipse=sdetect.ContourDetection(img_ellipse_comp) 
        cnt_ellipse_1=sdetect.ContourDetection(img_ellipse_comp_1) 
        cnt_ellipse_2=sdetect.ContourDetection(img_ellipse_comp_2)

        #going over the files and calculate the similarity 
        counter_indx=1
        stiction_counter=0
        similarity_results=[]
        result_counter= '0 / 0'
        for image_invest in image_storage_intermed: #Take every single image that was recently created 
                if len(image_invest.shape) != 2:
                        image_invest = cv2.cvtColor(image_invest, cv2.COLOR_BGR2GRAY)
                shape_open=sdetect.ShapeOpen(image_invest)
                i=0
                while shape_open==True and i <=25:
                        x=i
                        y=i
                        if i ==0:
                                closed_shape=sdetect.CloseShape(image_invest,x,y)
                        closed_shape = cv2.bitwise_not(closed_shape)
                        shape_open=sdetect.ShapeOpen(closed_shape)
                        i=i+1
                if i>0:
                        image_invest=closed_shape
                cnt_1=sdetect.ContourDetection(image_invest) 
                #Calculate the similarity 
                similarity_ellipse=sdetect.ContourComparison(cnt_1,cnt_ellipse)
                similarity_ellipse_1=sdetect.ContourComparison(cnt_1,cnt_ellipse_1)
                similarity_ellipse_2=sdetect.ContourComparison(cnt_1,cnt_ellipse_2)
                if similarity_ellipse<=0.5 or similarity_ellipse_1<=0.5 or similarity_ellipse_2<=0.5:
                        stiction=Cropping(image_invest,img_ellipse_comp)
                        if stiction==True:
                                if similarity_ellipse<=0.5:
                                        similarity_results.append(similarity_ellipse)
                                else:
                                        similarity_results.append(similarity_ellipse_2)
                                #Fit Ellipse 
                                ((centx,centy), (m,n), angle) = cv2.fitEllipse(cnt_1) #width is the major (m) axis and the height is the minor (n) axis
                                #Calculate the sticion value 
                                denominator=m*m*np.sin(np.deg2rad(angle))*np.sin(np.deg2rad(angle))+n*n*np.cos(np.deg2rad(angle))*np.cos(np.deg2rad(angle))
                                root=math.sqrt(denominator)
                                stiction_mag=2*m*n/root
                                stiction_mag_percent=stiction_mag/abs(m-n)
                                similarity_results.append('magnitude')
                                similarity_results.append(stiction_mag_percent)
                                stiction_mag_percent=0
                                similarity_results.append('Placeholder')
                                stiction_counter+=1
                counter_indx+=1
        result_counter=str(stiction_counter)+' / '+str(counter_indx)
        return similarity_results, result_counter
