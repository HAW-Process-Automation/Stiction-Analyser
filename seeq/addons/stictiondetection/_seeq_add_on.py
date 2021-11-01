import ipyvuetify as v
from ipyvuetify.generated.Row import Row
import ipywidgets as widgets
import numpy as np
import pandas as pd
from seeq import spy
from IPython.display import clear_output
import math

from ._CreatePVOP import CreatePVOP
from ._pushSignals import PushSignals,PushSignalsOsci
from ._utils import get_workbook_worksheet_workstep_ids, get_worksheet_url

class HamburgerMenu(v.Menu):
    def __init__(self, **kwargs):
        self.hamburger_button = v.AppBarNavIcon(v_on='menuData.on')
        self.help_button = v.ListItem(value='help',
                                      ripple=True,
                                      href='mailto: applied.research@seeq.com?subject=Correlation Feedback',
                                      children=[v.ListItemAction(class_='mr-2 ml-0',
                                                                 children=[v.Icon(color='#212529',
                                                                                  children=['fa-life-ring'])]),
                                                v.ListItemActionText(children=[f'Send Support Request'])
                                                ])
        self.items = [v.Divider(), self.help_button, v.Divider()]

        super().__init__(offset_y=True,
                         offset_x=False,
                         left=True,
                         v_slots=[{
                             'name': 'activator',
                             'variable': 'menuData',
                             'children': self.hamburger_button,
                         }]
                         ,
                         children=[
                             v.List(children=self.items)
                         ]
                         , **kwargs)
class CustomData(v.DataTable):
    def __init__(self):
        # create a btn to click on  
        # create the object 
        super().__init__() 
         # a header 
        self.headers = [
            { 'text': 'Start / End Time of the Oscillation', 'value': 'name'},
            { 'text': 'Stiction / total Oscillations Cycles', 'value': 'stiction_cases' },
            { 'text': 'Mean Magnitude of Stiction in %', 'value': 'magnitude_stiction' },
        ]
        # 3 initial items
    def FirstItem(self,time_start,time_end,stiction_cases,mean_mag_stic):
        self.time_start=time_start
        self.time_end=time_end
        self.stiction_cases=stiction_cases
        self.mean_mag_stic=mean_mag_stic
        self.items = [
        {
            'name': self.time_start+' / '+ self.time_end,
            'stiction_cases': stiction_cases,
            'magnitude_stiction': self.mean_mag_stic
        }
        ]
    def DeleteItem(self):
        self.items = []
    def AddItem(self,time_start,time_end,stiction_cases,mean_mag_stic):
        self.time_start=time_start
        self.time_end=time_end
        self.stiction_cases=stiction_cases  
        self.mean_mag_stic=mean_mag_stic
        new_item = {
            'name': self.time_start+' / '+ self.time_end,
            'stiction_cases': stiction_cases,
            'magnitude_stiction': self.mean_mag_stic
          } 
        #self.items.append(new_item)
        self.items = self.items + [new_item] 
        return self
def seeq_add_on(sdl_notebook_url):
    def pull_only_signals(url, grid=None):
        #login
        worksheet = spy.utils.get_analysis_worksheet_from_url(url)
        try:
            if  text_field_date_start_signal_1.v_model == '':
                start = worksheet.display_range['Start']
                end = worksheet.display_range['End']
        except NameError:
            start = worksheet.display_range['Start']
            end = worksheet.display_range['End']
        search_df = spy.search(url, estimate_sample_period=worksheet.display_range, quiet=True)
        if search_df.empty:
            return pd.DataFrame()
        search_signals_df = search_df[search_df['Type'].str.contains('Signal')]
        search_capsules_df = search_df[search_df['Type'].str.contains('Condition')]
        df = spy.pull(search_signals_df, start=start, end=end, grid=grid, header='ID',shape='samples', quiet=True,status=spy.Status(quiet=True))
        df_1=df.index[0]
        df_2=df.index[1]
        differnece=df_2-df_1
        sampling_rate = differnece.total_seconds()
        sampling_rate=sampling_rate/60
        df_capsule = spy.pull(search_capsules_df, start=start, end=end, grid=str(sampling_rate)+'min',shape='samples',header='Name', quiet=True,status=spy.Status(quiet=True))
        if df.empty:
            df= pd.DataFrame()
        else:
            df.columns = df.query_df['Name']
        if df_capsule.empty:
            df_capsule= pd.DataFrame()
        clear_output()
        return df,df_capsule,search_signals_df
            
    def ExecutePullSignal(df):
        global df_signal_1
        global df_signal_2
        global Signals_Pulled
        Signals_Pulled=True
        
        #The user should not select something during the calculation
        text_field_date_start_signal_1.disabled=True
        text_field_date_end_signal_1.disabled=True
        select_error.disabled=True
        select_op.disabled=True
        select_capsule.disabled=True
        btn_continue.loading=True

        column_1=select_error.v_model
        column_2=select_op.v_model
    #------ Pull the user selection -----------------#
        #When the user wants to use the display range
        if text_field_date_start_signal_1.v_model==df_start_displayed and text_field_date_end_signal_1.v_model==df_end_displayed:
            df_OP=df[column_2]
            df_PV=df[column_1]
            if select_capsule.v_model=='':
                indexes_stored=[]
                indexes_stored.append(0)
                indexes_stored.append(len(df_OP))
        #when the user wants to give in a certain time range
        if text_field_date_start_signal_1.v_model!=df_start_displayed or text_field_date_end_signal_1.v_model!=df_end_displayed:
            start_date=text_field_date_start_signal_1.v_model
            end_date=text_field_date_end_signal_1.v_model
            df=spy.pull(worksheet_url, start=start_date, end=end_date,grid=None,header='Name')
            df_OP=df[column_2]
            df_PV=df[column_1]
            if select_capsule.v_model=='':
                indexes_stored=[]
                indexes_stored.append(0)
                indexes_stored.append(len(df_OP))
        #if a capsule is selected
        if select_capsule.v_model!='':
            capsule=select_capsule.v_model
            df_capsule=df[capsule]
            indexes_stored_inter=[]
            indexes_stored=[]
            capsule_start=True
            counter_cap=0
            for i in range(len(df_capsule)):
                if df_capsule[i:i+1].values==1:
                    indexes_stored_inter.append(i)
                    if i==len(df_capsule)-1:
                        start=min(indexes_stored_inter)
                        end=max(indexes_stored_inter)
                        indexes_stored.append(start)
                        indexes_stored.append(end)
                        indexes_stored_inter=[] 
                if df_capsule[i:i+1].values==0:
                    try:
                        start=min(indexes_stored_inter)
                        end=max(indexes_stored_inter)
                        indexes_stored.append(start)
                        indexes_stored.append(end)
                        indexes_stored_inter=[]
                    except ValueError:
                        indexes_stored_inter=[]
                counter_cap+=1
    #-----------------------------------------------#      
        results=[]
        osci_index_final=[]
        #Create here the project folder
        counter_folder=0
        for i in range(len(indexes_stored)+1):
            if i%2==0 and i >0:
                #print(indexes_stored[i-2:i])
                start=indexes_stored[i-2]
                end=indexes_stored[i-1]
                df_invest_OP=df_OP[start:end+1]
                df_invest_PV=df_PV[start:end+1]
                if len(df_invest_PV)>3 or len(df_invest_OP)>3:
                    counter_folder+=1 
                    results_sim,osci_index=CreatePVOP(df_invest_PV,df_invest_OP,start,df_OP,df_PV) #here should be another value to differenciate between the osci groups
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
                    container_3.FirstItem(start_date,end_date,stiction_cases,mean_mag_stic)
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
                    container_3.AddItem(start_date,end_date,stiction_cases,mean_mag_stic)
                    osci_counter+=1
        #shutil.rmtree(path_compare_img)
        return mean_stiction_list,osci_index_final_date

    def on_click(widget, event, data):
        global overall_results
        global overall_results_oscillation
        overall_results,overall_results_oscillation=ExecutePullSignal(df)
        btn_continue.loading=False
        #Reset disable 
        text_field_date_start_signal_1.disabled=False
        text_field_date_end_signal_1.disabled=False
        select_error.disabled=False
        select_op.disabled=False
        select_capsule.disabled=False
    
    def on_click_cancel(widget, event, data):
        text_field_signal_name.v_model=''
        text_field_signal_name_osci.v_model=''
        select_capsule.v_model=''
        container_3.DeleteItem()

    def on_click_clean_table(widget, event, data):
        container_3.DeleteItem()

    def on_click_push(widget, event, data):
        try:
            button_to_seeq.loading=True
            #Push Stiction Signal to Seeq
            if len(overall_results)>0 and checkbox_selected_stiction.v_model==True:
                name=text_field_signal_name.v_model
                status=PushSignals(df,overall_results,worksheet_url,name)
            #Push Oscillation Signal to Seeq
            if len(overall_results_oscillation)>0 and checkbox_selected_oscillation.v_model==True:
                name=text_field_signal_name_osci.v_model
                status=PushSignalsOsci(df,overall_results_oscillation,worksheet_url,name)
            button_to_seeq.loading=False
        except ValueError:
            button_to_seeq.loading=False

    def on_click_scedule(widget, event, data):
        scedule_data={'Job Name':text_field_job_name.v_model,'Frequency':text_field_job_frequency.v_model,'Start Date':text_field_job_start.v_model,'Investigated Time':text_field_job_invest_time.v_model,'Error Signal':select_error.v_model,'OP Signal':select_op.v_model,'Capsule':select_capsule.v_model,'Push Stiction Signal':checkbox_selected_stiction.v_model,'Stiction Signal Name':text_field_signal_name.v_model,'Push Oscillation Signal':checkbox_selected_oscillation.v_model,'Oscillation Signal Name':text_field_signal_name_osci.v_model,'Worksheet URL':sdl_notebook_url}
        global df_scedule_data
        df_scedule_data=pd.DataFrame(scedule_data,index=[0])
        #spy.jobs.push(df_scedule_data)

    def on_click_scedule_cancel(widget, event, data):
        text_field_job_name.v_model=''
        text_field_job_frequency.v_model=''
        text_field_job_start.v_model=''
        text_field_job_invest_time.v_model=''

    def on_click_checkbox_stiction(widget, event, data):
        pass
        #checkbox_selected_stiction.v_model=True
    def on_click_checkbox_oscillation(widget, event, data):
        pass
    #checkbox_selected_oscillation.v_model=True
    #Pull the signals
    global worksheet_url
    global df
    global df_capsule
    worksheet_url = get_worksheet_url(sdl_notebook_url) 
    #worksheet_url=sdl_notebook_url #Just for testing
    df,df_capsule,search_signals_df=pull_only_signals(worksheet_url)
    global df_start_displayed
    global df_end_displayed
    df_start_displayed=df.index[0]
    df_end_displayed=df.index[-1]
    #Items Signals
    items=df.columns
    items=list(df.columns)
    #Items Conditions
    items_cond=df_capsule.columns
    items_cond=list(df_capsule.columns)
    df=pd.concat([df, df_capsule.reindex(df.index)], axis=1)

    container_3=CustomData()
    #Text field
        #Deploy Jobs
    text_field_job_name=v.TextField(v_model='',disabled=False,label='Job Name')
    text_field_job_frequency=v.TextField(v_model='',disabled=False,label='Frequency')
    text_field_job_start=v.TextField(v_model='',disabled=False,label='Start Date')
    text_field_job_start.v_model=df_start_displayed
    text_field_job_invest_time=v.TextField(v_model='',disabled=False,label='Investigated Time')
    text_field_job_E_Mail=v.TextField(v_model='',disabled=False,label='E-Mail Notification to')
        #UI without Jobs
    text_field_date_start_signal_1=v.TextField(v_model='',disabled=False,label='Start-Date')
    text_field_date_start_signal_1.v_model=df_start_displayed
    text_field_date_end_signal_1=v.TextField(v_model='',disabled=False,label='End-Date')
    text_field_date_end_signal_1.v_model=df_end_displayed
    text_field_signal_name=v.TextField(style_='height: 60px',v_model='',disabled=False,label='Signal Name for Stiction (Existing Signal will be appended)')
    text_field_signal_name_osci=v.TextField(style_='height: 60px',v_model='',disabled=False,label='Signal Name for Oscillation (Existing Signal will be appended)')

    #Buttons
    btn_continue=v.Btn(color='#00695C',dark=True,loading=False,children=['Analyse'])
    btn_continue.on_event('click', on_click)
    btn_exit=v.Btn(class_='ml-12',color='#00695C',dark=True,children=['Cancel'])
    btn_exit.on_event('click', on_click_cancel)
        #Send to workbook stiction
    button_to_seeq=v.Btn(class_='ma-10',color='#00695C',loading=False,dark=True,children=['Send Signal to Workbook'])
    button_to_seeq.on_event('click',on_click_push)
        #Send to workbook oscillation
    button_to_seeq_osci=v.Btn(class_='ma-10',color='#00695C',loading=False,dark=True,children=['Send Oscillation to Workbook'])
    button_to_seeq_osci.on_event('click',on_click_push)
        #clear table
    button_clear_table=v.Btn(class_='ma-10',color='#00695C',loading=False,dark=True,children=['Clear Table'])
    button_clear_table.on_event('click',on_click_clean_table)
        #job Button
    btn_add_scedule=v.Btn(color='#00695C',dark=True,loading=False,children=['Add to Job Manager'])
    btn_add_scedule.on_event('click', on_click_scedule)
    btn_add_scedule_cancel=v.Btn(color='#00695C',dark=True,loading=False,children=['Clear'])
    btn_add_scedule_cancel.on_event('click', on_click_scedule_cancel)
    #button_ex=v.Btn(class_='mr-10 ml-2',style_='fond',loading=False,color='#00695C',dark=True,children=['Execute'])

    #expansion Stiction
    explanation_head_stic=v.ExpansionPanelHeader(no_gutters=True,color='#E0E0E0',dark=True,children=['What is Stiction?'])
    explanation_expl_stic=v.ExpansionPanelContent(no_gutters=True,color='#E0E0E0',children=['Stiction is a valve suffering that could occour when there is too much friction inside the valve. Because of the higher friction the valve stemp resist to move until the moving force overcome the resiting force.'])
    expansion_final=v.ExpansionPanels(children=[v.ExpansionPanel(children=[explanation_head_stic,explanation_expl_stic])])
    #Expansion panel PV/OP
    explanation_head_PV_OP=v.ExpansionPanelHeader(color='#E0E0E0',dark=True,children=['What is Error / OP Data?'])
    explanation_expl_PV_OP=v.ExpansionPanelContent(color='#E0E0E0',children=['The Error data is revered to as the setpoint minus the process variable. In case of a cascade loop the error data are needed for the calculation. The OP is the output of controller. Both values helps the process engineer to detect mechanical valve problems. One of them is reffered to as stiction. '])
    expansion_final_PV_OP=v.ExpansionPanels(children=[v.ExpansionPanel(children=[explanation_head_PV_OP,explanation_expl_PV_OP])])
    #expansion job scedule 
    explanation_head_scedule=v.ExpansionPanelHeader(class_="white--text",color='#00695C',dark=True,children=['Deploy Stiction Analysis'])
    explanation_expl_scedule=v.ExpansionPanelContent(color='#E0E0E0',dark=True,children=[
        v.Row(children=[
                v.Col(lg='6',children=[text_field_job_name]),
                v.Col(lg='6',children=[text_field_job_frequency])]),
        v.Row(children=[
                v.Col(lg='6',children=[text_field_job_start]),
                v.Col(lg='6',children=[text_field_job_invest_time])]),
        v.Row(children=[
            v.Col(lg='5',children=[btn_add_scedule]),
            v.Col(lg='5',children=[btn_add_scedule_cancel])])])
    expansion_final_scedule=v.ExpansionPanels(children=[v.ExpansionPanel(children=[explanation_head_scedule,explanation_expl_scedule])])

    #Checkbox
    checkbox_selected_stiction=v.Checkbox(v_model=False,disabled=False,label='Send Stiction Signal')
    checkbox_selected_stiction.on_event('checkbox', on_click_checkbox_stiction)

    checkbox_selected_oscillation=v.Checkbox(v_model=False,disabled=False,label='Send Oscillation Signal')
    checkbox_selected_oscillation.on_event('checkbox', on_click_checkbox_oscillation)

    # App layout
    hamburger_menu = HamburgerMenu()
    appBar = v.AppBar(
        color='#00695C',
        dense=True,
        dark=True,
        children=[v.ToolbarTitle(children=['Stiction Detection']),
                    v.Spacer(),
                    v.Divider(vertical=True),
                    hamburger_menu])

    #Header
    head_line_results=v.Html(tag='h3',style_='color:white ; background:#546E7A',class_='text-center',color='#00695C',background_color='#00695C',children=['Results'])

    #Select signals
    select_error=v.Select(items=items,class_='mt-3',disabled=False,label='Select Error Signal',v_model='')
    select_op=v.Select(items=items,class_='mt-3',disabled=False,label='Select OP Signal',v_model='')
    select_capsule=v.Select(items=items_cond,class_='mt-3',disabled=False,label='Select Condition',v_model='')

    container_time_select=v.Container(disabled=True,children=[
                v.Row(lg='12',children=[
                    v.Col(lg='12',children=[
                        text_field_date_start_signal_1,
                        text_field_date_end_signal_1, 
                        select_capsule])])])      

    #Card
    container_results=v.Card(class_='',color='grey lighten-3',height='100%',children=[
        head_line_results,container_3,
        v.Row(no_gutters=True,children=[
            v.Col(lg='12',children=[text_field_signal_name,checkbox_selected_stiction]),v.Col(lg='12',children=[text_field_signal_name_osci,checkbox_selected_oscillation])]),
        v.Row(class_='ma-1',no_gutters=True,children=[button_to_seeq]),
        v.Row(class_='ma-0',no_gutters=True,children=[button_clear_table])])

    card_results=v.Card(class_='',color='grey lighten-3',height='100%',children=[container_results])

    #Container
    container_1=v.Container(fluid=True,children=[
            v.Row(no_gutters=True,children=[
                v.Col(lg='12',children=[
                select_error])]),
            v.Row(no_gutters=True,lg='12',children=[
                v.Col(lg='12',children=[select_op])]),
            v.Row(class_='pt-10'),
            v.Row(class_='pt-12',children=[
                v.Col(lg='4',children=[
                    btn_continue]),
                v.Col(lg='4',children=[
                    btn_exit])])])

    container_expansion=v.Container(children=[
            v.Row(children=[v.Col(lg='12',children=[expansion_final_scedule])]),
            v.Row(children=[v.Col(lg='12',children=[expansion_final])]),
            v.Row(children=[v.Col(lg='12',children=[expansion_final_PV_OP])])])

    global container_final
    container_final=v.Container(fluid=True,children=[
        appBar,
        v.Card(color='grey lighten-4',children=[
        v.Row(no_gutters=False,children=[
            v.Col(cols='7',children=[
                v.Row(lg='12',children=[
                    v.Col(lg='6',children=[container_1]),
                    v.Col(lg='6',children=[container_time_select]),
                ]),
                v.Row(children=[v.Col(lg='12',children=[container_expansion])])
        ]),
            v.Col(no_gutters=False,cols='5',children=[card_results])
        ])])])
    container_3.DeleteItem()
    return container_final