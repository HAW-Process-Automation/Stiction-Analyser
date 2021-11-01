from seeq import spy
import pandas as pd 
import numpy as np


def PushSignals(df,mean_stiction_list,worksheet_url,name):    
    signal_seeq=[]
    max_counter=len(mean_stiction_list)/5
    counter=0
    osci_counter=1
    start=False
    stop=False
    for i in range(len(df)):
        if stop ==False and str(df.index[i])==mean_stiction_list[osci_counter+1]:
            start=False
            osci_counter=osci_counter+5
            counter+=1
            if counter==max_counter:
                stop=True
        if stop==False and str(df.index[i])==mean_stiction_list[osci_counter] or start==True: 
            start=True
            signal_seeq.append(round(mean_stiction_list[osci_counter+2],2))

        if start == False:
                signal_seeq.append(0)
    df_results=pd.DataFrame(signal_seeq,index=df.index)
    df_results.columns=[name]
    spy.push(data=df_results,workbook=worksheet_url,quiet=True)
    return df_results

def PushSignalsOsci(df,osci_index_final_date,worksheet_url,name):   
    #------- Oscillation ---------
    signal_seeq_osci=[]
    max_counter=len(osci_index_final_date)/2
    counter=0
    osci_counter=0
    start=False
    stop=False
    for i in range(len(df)):
        if stop ==False and str(df.index[i])==osci_index_final_date[osci_counter+1]:
            start=False
            osci_counter=osci_counter+2
            counter+=1
            if counter==max_counter:
                stop=True
        if stop==False and str(df.index[i])==osci_index_final_date[osci_counter] or start==True: 
            start=True
            signal_seeq_osci.append(1)
        if start == False:
                signal_seeq_osci.append(0)
    df_results_osci=pd.DataFrame(signal_seeq_osci,index=df.index)
    df_results_osci.columns=[name]
    spy.push(data=df_results_osci,workbook=worksheet_url,quiet=True)
    return df_results_osci
