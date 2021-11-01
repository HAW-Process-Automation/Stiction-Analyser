import pandas as pd
import numpy as np
import datetime

def OsciFinder(df_invest,start):
    df_1=df_invest.index[0] #move to more general point and add for loop
    df_2=df_invest.index[1]
    differnece=df_2-df_1
    try:
        sampling_rate = differnece.total_seconds()
    except AttributeError:
        sampling_rate=1 #in Seconds
    if sampling_rate<=0:
        sampling_rate=1 #in Seconds
    #sampling_rate=12
    df_invest=np.array(df_invest)
    a=0.01 #Percent 
    n_lim=10
    load=[]
    counter=0
    waves=0
    iae=0
    number_osci=0
    counter_crossing=0
    counter_limit=30
    counter_index=0
    #to ensure that there is also a check on the time line
    n=0
    max_samples=-1
    end_index=[]
    list_osci_slices=[]
    intermend_res_list=[]
    tsup_start=False
    last_osci=False
    time_counter=0
    #for i,sample in enumerate(range(int(number_samples),len(df))):
    for i in range(1,len(df_invest)): #seems to be wrong index. Pass the indexes from the overall dataframe and start with the passed index 
        sign_old=int(np.sign(df_invest[i-1:i]))
        sign_current=int(np.sign(df_invest[i:i+1]))
        if last_osci==True:
            time_counter+=1
        if time_counter==max_samples*1.5:
            last_osci=False
            time_counter=0
        if tsup_start==True:
            n+=1
        if sign_current==sign_old:
            iae = iae + float(abs(df_invest[i:i+1]) * sampling_rate)
            load.append(0)
            counter+=1
        else:
            intermend_res_list.append(i+start)
            counter_index+=1
            if counter_index==2:
                start_ind=intermend_res_list[-2]
                end_ind=intermend_res_list[-1]
                between=end_ind-start_ind
                max_samples=between*10
                tsup_start=True
                n=0
            waves+=1
            if counter==0:
                counter=1
            omega_i=2*3.14159/(counter*sampling_rate)
            iae_lim = 2 * a / omega_i
            counter=0
            counter_crossing+=1
            if iae>iae_lim:
                number_osci+=1
                end_index.append(i+start)
                load.append(1)
            else:
                load.append(0)
            iae=float(abs(df_invest[i:i+1]) * sampling_rate)
        if counter_crossing==counter_limit or n==max_samples:
            n=0
            tsup_start=False
            if number_osci>=n_lim:
                if last_osci==True:
                    list_osci_slices[-2]=(max(end_index))
                else:
                    list_osci_slices.append('start')
                    list_osci_slices.append(min(end_index))
                    list_osci_slices.append(max(end_index))
                    list_osci_slices.append('end')
                last_osci=True
            else:
                last_osci=False

            end_index=[]                 
            counter_crossing=0
            number_osci=0
            counter_index=0
            time_counter=0
                
    list_results=[]
    counter=0 
    intermed_value=0
    for i in range(3,len(list_osci_slices)):
        if list_osci_slices[i-3] =='start' and list_osci_slices[i] =='end' and intermed_value>0:
            list_results.append(list_osci_slices[i-1])
            list_results.append('end')
            intermed_value=0
            counter=0
        if list_osci_slices[i-3] =='start' and list_osci_slices[i] =='end':
            list_results.append('start')
            list_results.append(list_osci_slices[i-2])
            list_results.append(list_osci_slices[i-1])
            list_results.append('end')
    if intermed_value>0:
        list_results.append(intermed_value)
        list_results.append('end')
    return list_results
