import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time
import os
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pygwalker as pyg
import streamlit.components.v1 as components
from dotenv import load_dotenv
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

st.set_page_config(
    page_title= "Datawise",
    page_icon= ":white flower:",
    layout="wide",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Main Menu
app = option_menu(
    menu_title= "My DataWise",
    options= ["Home", "Wrap Dataset","Insights", "Visualization",  "Just Ask", "Directory"],
    icons= ["house-fill", "envelope-paper-fill", "signpost-split-fill", "pc-display", "chat-left-fill", "people-fill"],
    menu_icon= "disc-fill",
    default_index=0,
    orientation='horizontal',
)
#Home
if app == "Home":
    st.header("Welcome to your own enWise Data Account")
    st.subheader(":moneybag:")
    #st.image(Logo, width=500)

#Wrap Data
if app == "Wrap Dataset":
     st.subheader("Wrap your data")
     tab1, tab2, tab3 = st.tabs(["Put Dataset","Generate Key", "Productwise Policy"])
     col1, col2 = st.columns(2)    
     with tab1:
         st.subheader("Please upload the Dataset")
         st.markdown('Please upload the Dataset you wish to share with a concerned person, with corresponding details')
         with col1:
          with st.form("dataInputForm"):
            fileName = st.text_input('Title of the Dataset')
            validity = st.number_input('Validity in hrs', step=1)
            with col2:
             file = st.file_uploader('Put the Dataset', type='csv')

            @st.cache_data
            def load_csv():
                csv = pd.read_csv(file)
                return csv
            df1 = load_csv()
            st.write("Please type a secret key. It will be matched while giving access to the Dataset")
            secKey = st.text_input("Secret Key (Max 8 characters)", max_chars=8, type='password')
            filepath = str(fileName)+' '+str(secKey)+' '+str(validity*3600)+'.csv'
            st.warning('Anyone having the Title of dataset & secret key can use your Gateway')
            allowInsights = st.toggle('Generate Gateway for Insights')
            allowVisual = st.toggle('Generate Gateway for Visualization')
            allowAI = st.toggle('Generate Gateway for AI powered answers')
            shareButton = st.form_submit_button('Generate the Gateway')
            if shareButton:
                if allowInsights:
                   df1.to_csv('Insights'+'/'+filepath, index=False)
                if allowVisual:
                   df1.to_csv('Visualization'+'/'+filepath, index=False)
                if allowAI:
                   df1.to_csv('AI Answers'+'/'+filepath, index=False)
                if secKey and fileName and validity and file:
                   st.success("Great!! Gateway for your dataset has been created. You can share the Key & title of the dataset with concerned user")
                if allowAI is False and allowInsights is False and allowVisual is False:
                    st.error("Please select at least one Gateway option")
                if secKey is None or fileName is None or validity is None or file is None:
                    st.error("Please check whether the title, key and validity are added, and the Dataset is uploaded")

#Insights
if app == 'Insights':
   st.subheader('Get Overview of a Dataset')
   with st.form('Insight_form'):
      inFile = st.text_input('Please enter the exact title of the dataset')
      inSeckey = st.text_input("Secret Key of the Dataset", max_chars=8, type='password')
      inFileVal = st.number_input('Validity of Dataset', step=1)
      inFilename = 'Insights'+'/'+str(inFile)+' '+str(inSeckey)+' '+str(inFileVal*3600)+'.csv'
      inRequest = st.form_submit_button('Connect')
      if inRequest:
         def inFilename_age(inFilename):
            ctime = os.stat(inFilename).st_ctime
            return ctime
         if os.path.isfile(inFilename):
            if time.time()- inFilename_age(inFilename)>inFileVal*3600:
               os.remove(inFilename)
               st.warning('Gateway for this Dataset has been expired')
            else:
               @st.cache_data
               def load_in():
                  in_csv = pd.read_csv(inFilename)
                  return in_csv
               dfi= load_in()
               ov = ProfileReport(dfi, explorative=True)
               st.success("Insights for the dataset are as below")
               st_profile_report(ov)
         if os.path.isfile(inFilename) is False:
            st.error('Please enter correct Title & Secret Key for the dataset. Also check the validity.')
      else:
          st.warning("Please enter correct Title & Secret Key for the dataset")

#Visualization
if app == "Visualization":
   st.subheader('Interact with the dataset to visualize')

   with st.form('Visualization_form'):
      visFile = st.text_input('Please enter the exact title of the dataset')
      visSeckey = st.text_input("Secret Key of the Dataset", type='password')
      visFileVal = st.number_input('Validity of Dataset', step=1)
      visFilename = 'Visualization'+'/'+str(visFile)+' '+str(visSeckey)+' '+str(visFileVal*3600)+'.csv'
      visRequest = st.form_submit_button('Connect')
      if visRequest:
         def visFilename_age(visFilename):
            vctime = os.stat(visFilename).st_ctime
            return vctime
         if os.path.isfile(visFilename) is False:
            st.error('Please enter correct Title & Secret Key for the dataset. Also check the validity.')
         if os.path.isfile(visFilename):
            if time.time()- visFilename_age(visFilename)>visFileVal*3600:
               os.remove(visFilename)
               st.warning('Gateway for this Dataset has been expired')
            
            else:
               @st.cache_data
               def load_vis():
                  vis_csv = pd.read_csv(visFilename)
                  return vis_csv
               dfv= load_vis()
               st.success('Visualization is as below')
               # hide_tabl_style = """
               # <style>
               # #kanaries-logo {visibility: hidden;}
               # footer {visibility: hidden;}
               # header {visibility: hidden;}
               # </style>
               # """
               
               pyg_html = pyg.to_html(dfv, return_html = True, dark='media', hideDataSourceConfig=True)
               components.html(pyg_html, height=1000)   
 
      else:
          st.warning("Please enter the Title & Secret Key for the dataset")
      
#AI Chat
if app == "Just Ask":
   st.subheader("AI powered answers")
   with st.form('AI_form'):
      aiFile = st.text_input('Please enter the exact title of the dataset')
      aiSeckey = st.text_input("Secret Key of the Dataset", type='password')
      aiFileVal = st.number_input('Validity of Dataset', step=1)
      aiFilename = 'AI Answers'+'/'+str(aiFile)+' '+str(aiSeckey)+' '+str(aiFileVal*3600)+'.csv'
      aiRequest = st.form_submit_button('Connect')
      if aiRequest:
         def aiFilename_age(aiFilename):
            actime = os.stat(aiFilename).st_ctime
            return actime
         if os.path.isfile(aiFilename) is False:
            st.error('Please enter correct Title & Secret Key for the dataset. Also check the validity.')         
         if os.path.isfile(aiFilename):
            if time.time()- aiFilename_age(aiFilename)>aiFileVal*3600:
               os.remove(aiFilename)
               st.warning('Gateway for this Dataset has been expired')
            else:
               @st.cache_data
               def load_ai():
                  ai_csv = pd.read_csv(aiFilename)
                  return ai_csv
               dfa= load_ai()
               st.success('Connection to the dataset has been established')
               st.write('Random 3 rows from the dataset are shown below, for insight')
               st.write(dfa.sample(n=3))
               load_dotenv(".env")
               API_KEY = os.getenv('OPEN_API_KEY')
               llm = OpenAI(api_token=str(API_KEY))
               pandas_ai = PandasAI(llm)
               question = st.text_area('Please type your question about the dataset here')
               if st.form_submit_button('Generate AI response'):
                  if question:
                     st.write('AI response is being generated. Please wait for some time...')
                     st.write(pandas_ai.run(dfa, prompt=question))
                  else:
                     st.warning('Please enter a question')

#Directory
if app == "Directory":
    st.header("Directory for offers & requests of datasets will be updated soon.")