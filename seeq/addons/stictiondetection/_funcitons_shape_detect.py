import numpy as np
import cv2 as cv2
from skimage import img_as_float
from ._SignalProcessing import SignalProcessing
from ._ShapeDetection import ShapeDetection

#Image Cropping
def EdgeCropping(imageCrop):
    #loading the basic image
    image_main = imageCrop
    height, width = image_main.shape[:2]
    high_half=int(height/2)
    width_half=int(width/2)
    #slice the investigated window in the image
    #investigate the bottom left corner
    cropped_bottom = image_main[high_half:height,0:width_half]
    #investigate the upper right corner
    cropped_top = image_main[0:high_half,width_half:width]
    return cropped_bottom, cropped_top

def ImgFrame_2(image_invest_frame):
    image_invest_frame_gray=image_invest_frame
    height, width = image_invest_frame_gray.shape[:2]
    locatioin=[]
    #left left
    thresh_x = np.mean(image_invest_frame_gray[0:2,0:2])
    counter=0
    for pixel_x in range(width):
        #investigate the bottom left corner (Y,X) || top left is Zero 
        cropped_x = image_invest_frame_gray[0:height,pixel_x:pixel_x+1]
        cropped_x_mean=np.mean(cropped_x)
        if cropped_x_mean<thresh_x:
            locatioin.append(pixel_x)
            break
        counter=counter+1
    #left right
    counter=0
    for pixel_x in range(width):
        #investigate the bottom left corner (Y,X) || top left is Zero 
        cropped_x = image_invest_frame_gray[0:height,width-pixel_x-1:width-pixel_x]
        cropped_x_mean=np.mean(cropped_x)
        if cropped_x_mean<thresh_x:
            locatioin.append(width-pixel_x)
            break
        counter=counter+1
    #top thresh
    counter=0
    for pixel_y in range(height):
        #investigate the bottom left corner (Y,X) || top left is Zero 
        cropped_y = image_invest_frame_gray[pixel_y:pixel_y+1,0:width]
        cropped_y_mean=np.mean(cropped_y)
        if cropped_y_mean<thresh_x:
            locatioin.append(pixel_y)
            break
        counter=counter+1
    #bottom 
    counter=0
    for pixel_y in range(height):
        #investigate the bottom left corner (Y,X) || top left is Zero 
        cropped_y = image_invest_frame_gray[height-pixel_y-1:height-pixel_y,0:width]
        cropped_y_mean=np.mean(cropped_y)
        if cropped_y_mean<thresh_x:
            locatioin.append(height-pixel_y)
            break
        counter=counter+1
    #result is in the format --> left , right , bottom , top 
    image_invest_frame_gray=image_invest_frame_gray[locatioin[2]:locatioin[3],locatioin[0]:locatioin[1]]
    #print(image)
    return image_invest_frame_gray

#Shape rotation
def RotateElipse(imageRot,compare_ellipse):
    #loading the basic image
    image_main = imageRot
    height, width = image_main.shape[:2]
    high_half=int(height/2)
    width_half=int(width/2)
    #----
    #slice the investigated window in the image
    #investigate the upper left corner
    cropped = image_main[0:high_half,0:width_half]
    image = img_as_float(cropped)
    #calculate the mean luminosity values in the investigated window
    image_mean=np.mean(image)
    #-#-#-#-#
    #investigate the upper right corner
    cropped_2 = image_main[0:high_half,width_half:width]
    image_2 = img_as_float(cropped_2)
    image_mean_2=np.mean(image_2)
    #----
    #Check if the elipse is left or right centered
    if image_mean < image_mean_2:
        left_elipse=True
    else:
        left_elipse=False  
    #----- loading the second image (compared)-------
    image_main = compare_ellipse
    #getting the shape of the image and the center position
    height, width = image_main.shape[:2]
    high_half=int(height/2)
    width_half=int(width/2)
    #----
    #slice the investigated window in the image
    #investigate the upper left corner
    cropped = image_main[0:high_half,0:width_half]
    image = img_as_float(cropped)
    #calculate the mean luminosity values in the investigated window
    image_mean=np.mean(image)
    #-#-#-#-#
    #investigate the upper right corner
    cropped_2 = image_main[0:high_half,width_half:width]
    image_2 = img_as_float(cropped_2)
    image_mean_2=np.mean(image_2)
    #----
    #Check if elipse is left or right centered
    if image_mean < image_mean_2:
        left_elipse_comp=True
    else:
        left_elipse_comp=False
    if left_elipse == True and left_elipse_comp==True or left_elipse==False and left_elipse_comp==False:
        rotate_image=False
        direction='no inverse'
    if left_elipse==True and left_elipse_comp==False:
        rotate_image=True
        direction='inverse right'
    if left_elipse==False and left_elipse_comp==True:
        rotate_image=True
        direction='inverse left'
    return direction
def findCropEdge(cropped_top,cropped_bottom):
    height, width = cropped_top.shape[:2]
    x_location_top=[]
    y_location_top=[]
    #cropped top
    for x in range(0,width):
        #height width
        color_value=cropped_top[height-1:height,x:x+1]
        if color_value<255:
            x_location_top.append(x)
    #cropped bottom
    for y in range(0,height):
        #height width
        color_value=cropped_top[y:y+1,0:1]
        if color_value<255:
            y_location_top.append(y)
    #----------- Bottom -----------
    height, width = cropped_bottom.shape[:2]
    x_location_bottom=[]
    y_location_bottom=[]
    #cropped bottom
    for x in range(0,width):
        #height width
        color_value=cropped_bottom[0:1,x:x+1]
        if color_value<255:
            x_location_bottom.append(x)
    #cropped bottom
    for y in range(height):
        #height width
        color_value=cropped_bottom[y:y+1,width-1:width]
        if color_value<255:
            y_location_bottom.append(y)
    try:       
        return x_location_top[0],y_location_top[0],x_location_bottom[0],y_location_bottom[0]
    except IndexError:
        return 'none','none','none','none'

#----- 
def Cropping(image_invest,compare_ellipse):
    sdetect=ShapeDetection()
    x=SignalProcessing()
    image=ImgFrame_2(image_invest)
    if RotateElipse(image,compare_ellipse)=='inverse right':
        image = cv2.flip(image, 0)
    cropped_bottom,cropped_top=EdgeCropping(image)
    x_top,y_top,x_bottom,y_bottom=findCropEdge(cropped_top,cropped_bottom)
    if x_top=='none':
        return False
    White=[255,255,255]
    #------ top -----------
    height, width = cropped_top.shape[:2]
    line_thickness = 2
    cv2.line(cropped_top, (0, y_top), (x_top, height), (0, 255, 0), thickness=line_thickness)
    cropped_top= cv2.copyMakeBorder(cropped_top,20,20,20,20,cv2.BORDER_CONSTANT,value=White)
    #------ bottom ---------
    height, width = cropped_bottom.shape[:2]
    line_thickness = 2
    cv2.line(cropped_bottom, (x_bottom, 0), (width, y_bottom), (0, 255, 0), thickness=line_thickness)
    #add border space
    cropped_bottom= cv2.copyMakeBorder(cropped_bottom,20,20,20,20,cv2.BORDER_CONSTANT,value=White)
    
    cnt=sdetect.ContourDetection(cropped_top)
    cnt_2=sdetect.ContourDetection(cropped_bottom)
    shape_1=sdetect.detect(cnt)
    shape_2=sdetect.detect(cnt_2)
    stiction=False
    if shape_1 =='triangle' or shape_2 =='triangle':
        stiction=True
        return stiction
    else:
        stiction=False
        return stiction