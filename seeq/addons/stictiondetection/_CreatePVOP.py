import ipyvuetify as v
import pandas as pd
from seeq import spy
import ipywidgets as widgets
import time
import numpy as np
from IPython.display import clear_output
import matplotlib.pyplot as plt
import os

from ._SignalProcessing import SignalProcessing
from ._OsciFinder import OsciFinder
from ._SimilarityFinder import SimilarityFinder

def CreatePVOP(df_1,df_2,start_index_osci,df_op_main,df_pv_main):
    #header_osci.children=['Calculate if the Signals are Oscillating']
    df_PV_invest=df_1
    df_OP=df_op_main
    df_PV=df_pv_main
    x=SignalProcessing()
    #Find the start and entpoints of oscillations
    try:
        df_invest_sm=x.SmoothSignal(df_PV_invest,0.05,1)
    except ValueError:
        df_invest_sm=df_PV_invest
    df_invest_sm=pd.DataFrame(df_invest_sm,index=df_PV_invest.index)
    osci_index=OsciFinder(df_invest_sm,start_index_osci) #Give a list containing the indexes of the start and end of the oscillations
    #print(osci_index)
    osci_index_final=[]
    for i,content in enumerate(osci_index):
        if content =='start':
            interm_list=[]
            interm_list=osci_index[i+1:i+3]
            osci_index_final.append(interm_list)
    if len(osci_index_final)==0:
        return 'none',[['none']]
    #should go in to the nested elements
    number_oscillations=len(osci_index_final)
    image_storage=[]
    for i in range(number_oscillations):
        image_storage.append([])   
    similarity_results=[]
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#--#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#------      STARTING BIG LOOP TO GO OVER THE OSCILLATIONS      ------------
    for i,content in enumerate(image_storage): 
        start_inx=osci_index_final[i][0]
        end_inx=osci_index_final[i][1]
        try:
            noise_index=x.NoiseCheck(df_OP[start_inx:end_inx+1],int(len(df_OP[start_inx:end_inx+1])),int(len(df_OP[start_inx:end_inx+1])/4))
            noisy_signal=False
            if noise_index<=50:
                df_smooth_OP_slicing=x.SmoothSignal(df_OP[start_inx:end_inx+1],0.04,1)
            else:
                filter_para=x.FilterPara(df_OP[start_inx:end_inx+1],int(len(df_OP[start_inx:end_inx+1])),int(len(df_OP[start_inx:end_inx+1])/4))
                filter_para_slicing=filter_para
                if filter_para_slicing<=0.01:
                    filter_para_slicing=0.01
                if filter_para_slicing>=0.3:
                    filter_para_slicing=0.3
                df_smooth_OP_slicing=x.SmoothSignal(df_OP[start_inx:end_inx+1],filter_para_slicing,1)
        except ValueError:
            filter_para_slicing=0.05
            df_smooth_OP_slicing=df_OP[start_inx:end_inx+1]
            noisy_signal=True
        slicing_points=[]
        slicing_points=x.SliceSignal(df_smooth_OP_slicing)
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #soft smoothing for furhter use
        #Smoothing PV signal
        try:
            noise_index_2=x.NoiseCheck(df_PV[start_inx:end_inx+1],int(len(df_PV[start_inx:end_inx+1])),int(len(df_PV[start_inx:end_inx+1])/4))
            if noise_index_2<=50:
                df_smooth_PV=x.SmoothSignal(df_PV[start_inx:end_inx+1],0.3,1)
            else:
                filter_para_2=x.FilterPara(df_PV[start_inx:end_inx+1],int(len(df_PV[start_inx:end_inx+1])),int(len(df_PV[start_inx:end_inx+1])/4))
                if filter_para_2<=0.01 or filter_para_2>=0.1:
                    filter_para_2=0.01
                df_smooth_PV=x.SmoothSignal(df_PV[start_inx:end_inx+1],filter_para_2,1)

            if noisy_signal==True:
                filter_para=filter_para
                if filter_para<=0.01:
                    filter_para=0.01
                df_smooth_OP=x.SmoothSignal(df_OP[start_inx:end_inx+1],filter_para,1)
            else:
                df_smooth_OP=x.SmoothSignal(df_OP[start_inx:end_inx+1],0.3,1)
        except ValueError:
            df_smooth_PV=df_PV[start_inx:end_inx+1]
            df_smooth_OP=df_OP[start_inx:end_inx+1]
            
        if len(slicing_points)<=1 or slicing_points=="":
            continue
        else:
            image_storage_intermed=x.ImageSlices(df_smooth_OP,df_smooth_PV,slicing_points)
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #-#-#-#-#-#-#-# Loop over the folders #-#-#-#-#-#-##-#-#-#-#
            similarity,result_counter=SimilarityFinder(image_storage_intermed)
            similarity_results.append('start')
            similarity_results.append(start_inx)
            similarity_results.append('end')
            similarity_results.append(end_inx)
            similarity_results.append(result_counter)
            if len(similarity)>0:
                similarity_results.append(similarity)
            else:
                similarity_results.append('none')

    return similarity_results,osci_index_final