import numpy as np
import matplotlib.pyplot as plt
import math
import os
import pandas as pd
#signal filtering
from scipy import signal
import cv2

class SignalProcessing:
    def SignaltoNoise(self,a, axis=0, ddof=0):
        self.a=a
        self.axis=axis
        self.ddof=ddof
        self.a = np.asanyarray(self.a)
        self.m = self.a.mean(self.axis)
        self.sd = self.a.std(axis=self.axis, ddof=self.ddof)
        return np.where(self.sd == 0, 0, self.m/self.sd)

    def SmoothSignal(self,data,noise_filter,order=1):
        self.data=data
        self.noise_filter=noise_filter
        self.order=order
        if self.noise_filter<=0:
            self.noise_filter==0.05
        self.y=data
        self.x=range(len(self.y))
        #higher values mean higher fit to the real data and less fitler
        self.noise_filter=noise_filter    #find a good value for the filter
        self.b, self.a = signal.butter(self.order, self.noise_filter)
        self.y = signal.filtfilt(self.b, self.a, self.y)
        return self.y

    def NoiseCheck(self,df,window_size,invest_window):
        self.data_sliced=df
        self.window_size=window_size
        self.invest_window=invest_window
        if self.invest_window<=0:
            self.invest_window=1
        self.ex_kernel=[]
        self.kernel=len(self.data_sliced)/self.invest_window
        for i in range(int(self.kernel)):
            self.ex_kernel.append(self.SignaltoNoise(self.data_sliced[i*self.invest_window:(i*self.invest_window)+self.invest_window]))
        self.ex_kernel = np.asanyarray(self.ex_kernel)
        self.noise_index=self.ex_kernel.mean()
        return self.noise_index

    def FilterPara(self,df,window_size,invest_window):
        self.data_sliced=df
        self.window_size=window_size
        self.invest_window=invest_window
        if self.invest_window<=0:
            self.invest_window=1
        self.ex_kernel=[]
        self.kernel=len(self.data_sliced)/self.invest_window

        for i in range(int(self.kernel)):
            self.ex_kernel.append(self.SignaltoNoise(self.data_sliced[i*self.invest_window:(i*self.invest_window)+self.invest_window]))
        self.ex_kernel = np.asanyarray(self.ex_kernel)
        self.noise_index=self.ex_kernel.mean()
        if self.noise_index<=0:
            return 0
        else:
            self.filter_parameter=8.6894*math.pow(self.noise_index,-1.002)
            return self.filter_parameter 

    def SliceSignal(self,x):
        self.x=x
        self.N=0
        self.turning_points=[]
        for i in range(1, len(self.x)-1):
            if ((self.x[i-1] < self.x[i] and self.x[i+1] < self.x[i]) or (self.x[i-1] > self.x[i] and self.x[i+1] > self.x[i])):
                self.N += 1
                self.turning_points.append(i)
        self.counter=0
        self.slice_points=[]
        for i,points in enumerate(self.turning_points):
            if i ==0:
                self.slice_points.append(points)
            self.counter=self.counter+1
            if self.counter==3:
                self.slice_points.append(points)
                self.counter=1
        return self.slice_points
    
  #creating images out of the slices
    def ImageSlices(self,df_x,df_y,slices):
        self.df_x=df_x
        self.df_y=df_y
        self.slices=slices
        self.counter_img=0
        self.image_storage_intermed=[]
        for i in range(2,len(self.slices)):
            self.x_img_slice=self.df_x[self.slices[i-1]:self.slices[i]+1]
            self.y_img_slice=self.df_y[self.slices[i-1]:self.slices[i]+1]
            plt.ioff()
            self.fig = plt.figure()
            self.ax=self.fig.add_subplot(1,1,1)
            self.ax.plot(self.x_img_slice,self.y_img_slice)
            self.ax.axis('off')
            plt.close(self.fig)
            # redraw the canvas
            self.fig.canvas.draw()
            # convert canvas to image
            self.img = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
            self.img  = self.img.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            # img is rgb, convert to opencv's default bgr
            self.img = cv2.cvtColor(self.img,cv2.COLOR_RGB2BGR)
            self.image_storage_intermed.append(self.img)
            plt.clf()
            self.counter_img+=1
        return self.image_storage_intermed

