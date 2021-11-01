import ipyvuetify as v
import ipywidgets as widgets
import numpy as np
import pandas as pd
from seeq import spy
from IPython.display import clear_output
import math

from ._CreatePVOP import CreatePVOP
from ._pushSignals import PushSignals,PushSignalsOsci

def ExecutePullSignal(df):
 #-----------------------------------------------# 
    df_OP=df['OP']
    df_PV=df['Error']
    indexes_stored=[]
    indexes_stored.append(0)
    indexes_stored.append(len(df_OP))   
    print(indexes_stored)
    results=[]
    osci_index_final=[]
    #Create here the project folder
    counter_folder=0
    for i in range(len(indexes_stored)+1):
        if i%2==0 and i >0:
            start=indexes_stored[i-2]
            end=indexes_stored[i-1]
            df_invest_OP=df_OP[start:end+1]
            df_invest_PV=df_PV[start:end+1]
            if len(df_invest_PV)>3 or len(df_invest_OP)>3:
                counter_folder+=1 
                results_sim,osci_index=CreatePVOP(df_invest_PV,df_invest_OP,start,df_OP,df_PV) 
                results.append(results_sim)
                osci_index_final.append(osci_index)

    results_append=[]
    for res in results:
        if len(res)>0 and res!='none':
            results_append.append(res)
    flat_list = [item for sublist in results_append for item in sublist]
    results=flat_list
    #Oscillation #-#-#-#-#-#
    flat_list = [item for sublist in osci_index_final for item in sublist]
    flat_list = [item for sublist in flat_list for item in sublist]
    osci_index_final_res=[]
    osci_index_final_date=[]
    for i,osci in enumerate(flat_list):
        if osci!='none':
            osci_index_final_res.append(osci)
    for i in range(len(osci_index_final_res)+1):
        if i%2==0 and i>0:
            osci_index_final_date.append(str(df.index[osci_index_final_res[i-2]])) 
            osci_index_final_date.append(str(df.index[osci_index_final_res[i-1]])) 
    #-#-#-#-#-#
    mean_stiction_list_interm=[]
    mean_stiction_list=[]
    mean_stiction=0
    counter=0
    counter_osci=0
    for k in range(len(results)):
        counter+=1
        if counter==6:
            counter=0
            counter_osci+=1
            if results[k]=='none':
                mean_stiction=0
            else:
                for i,value in enumerate(results[k]):
                    if value=='magnitude':
                        mean_stiction_list_interm.append(results[k][i+1])
                mean_stiction=np.array(mean_stiction_list_interm).mean()
                is_NaN = math.isnan(mean_stiction)
                if is_NaN==True:
                    mean_stiction=0
            mean_stiction_list.append('Oscillation '+str(counter_osci))
            mean_stiction_list.append(str(df.index[results[k-4]]))
            mean_stiction_list.append(str(df.index[results[k-2]]))
            mean_stiction_list.append(mean_stiction)
            mean_stiction_list.append(results[k-1])

    #Results Section
    counter=0
    osci_counter=1
    for i in range(len(mean_stiction_list)):
        counter+=1
        if counter==5:
            if osci_counter==1:
                start_date=mean_stiction_list[i-3]
                end_date=mean_stiction_list[i-2]
                stiction_cases=mean_stiction_list[i]
                mean_mag_stic=round(mean_stiction_list[i-1],2)
                is_NaN = math.isnan(mean_mag_stic)
                if is_NaN==True:
                    mean_mag_stic=0
                counter=0
                osci_counter+=1
            else:
                start_date=mean_stiction_list[i-3]
                end_date=mean_stiction_list[i-2]
                stiction_cases=mean_stiction_list[i]
                mean_mag_stic=round(mean_stiction_list[i-1],2)
                is_NaN = math.isnan(mean_mag_stic)
                if is_NaN==True:
                    mean_mag_stic=0
                counter=0
                osci_counter+=1
    return mean_stiction_list,osci_index_final_date