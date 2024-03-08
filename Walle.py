import streamlit_authenticator as stauth
import webbrowser
from ast import Param, Return
from asyncio.windows_events import NULL
from cProfile import label
from copy import deepcopy
from enum import unique
from heapq import merge
from msilib.schema import Complus, Font
from operator import index
from pickle import TRUE
from sre_parse import State
from tkinter import font
from tkinter.tix import CELL, COLUMN
from types import CellType
from typing import List
from xmlrpc.client import boolean
from importlib_metadata import files
from numpy import True_, fix, size, true_divide
from openpyxl import Workbook
from openpyxl.utils.cell import get_column_letter
from pyparsing import col, null_debug_action
import streamlit as st
import pandas as pd
import os
import sys
import datetime 
from PIL import Image
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas.io.formats.excel
import yaml as yaml
from streamlit_option_menu import option_menu

#-- constants
exec(compile(source=open('GlobalFilePath.py').read(), filename='GlobalFilePath.py', mode='exec'))

#-- user authorization
exec(compile(source=open('UserAuthorization.py').read(), filename='UserAuthorization.py', mode='exec'))

with open(user_profile_file.replace("[userid]", os.getlogin())) as file:
    config = yaml.safe_load(file)

imag_icon = Image.open(castrLogoPath.replace("[userid]", os.getlogin()))

#-- user authorization
exec(compile(source=open('walleTitle.py').read(), filename='walleTitle.py', mode='exec'))

#----------------------------------------------#
#    input : file - file name                  #
#            sheet - sheet name                #
#    output :dataset                           #
#----------------------------------------------#
def df_GetSheet(file, sheet):
    if sheet == 'AuditConfigurationDetails' or sheet == "Temp_AuditConfigurationDetails":
        converters={'names':str,'ages':str}
        df = pd.DataFrame(pd.read_excel(
        io=file,
        sheet_name= sheet,
        keep_default_na=False,
        skiprows=0,
        converters= {'disployOrder':str}
        ).dropna(how='all'))
        #-- df.fillna('',inplace=True)
        df['unique_index'] = df.reset_index().index
        df.columns=df.columns.map(lambda x: x.replace('\r','').replace('\n', ''))

        return df
    else:
        
        df = pd.DataFrame(pd.read_excel(
        io=file,
        sheet_name= sheet,
        keep_default_na=False,
        skiprows=0,
        ).dropna(how='all'))
        #-- df.fillna('',inplace=True)
        df['unique_index'] = df.reset_index().index
        df.columns=df.columns.map(lambda x: x.replace('\r','').replace('\n', ''))
        return df

#----------------------------------------------#
#    input : df - dataframe                    #
#            allowEdit - True or False         #
#    output : datagrid option configs          #
#----------------------------------------------#
def grid_option(df,allowEdit):
    template = GridOptionsBuilder.from_dataframe(df)
    template.configure_pagination(enabled=True)
    template.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=allowEdit)
    cellstyle_jscode = JsCode("""
        function(params) {
            if (params.value === 'Right To Work') {
                return {
                    'color': 'red',
                    'backgroundColor': 'darkred'
                }
            } else {
                return {
                    'color': 'orange',
                    'backgroundColor': 'white'
                }
            }
        };
        """)
    template.configure_selection(selection_mode='multiple', use_checkbox= True) 
    js_update=JsCode("""
            function(e){
                let api = e.api;
                let sel = api.getSelectedRows();
                api.applyTransaction({update:sel})

            }
            """
            )
    #-- st.markdown('<p class="alert-font"></p>', unsafe_allow_html=True)
    #-- template.configure_column("document", header_name = "document")
    template.configure_grid_options(onRowUpdated=js_update)
    gridoptions = template.build() 
    
    return gridoptions

def grid_builder(df,allowEdit, gridHeight=600, keyVal=0):
    userPermit = False
    if (user_permit.permit == administrator):
        userPermit = True

    gridoptions = grid_option(df,userPermit)
    return AgGrid(
                df, 
                gridOptions=gridoptions,
                height=gridHeight,
                width='100%',
                data_return_mode=DataReturnMode.FILTERED,
                update_mode=GridUpdateMode.MODEL_CHANGED, 
                # -- fit_columns_on_grid_load = True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules = True,
                theme='blue',
                relaod_data=True,
                key=keyVal
            ) 

#-- Widges
exec(compile(source=open('walleWidges.py').read(), filename='walleWidges.py', mode='exec'))

#-- def write_to_excel(df, sheetName):
#--    clicked = castrTempPath.replace("[userid]", os.getlogin())
#--    with pd.ExcelWriter(clicked) as writer:
#--        df.to_excel(writer, sheet_name = sheetName, index = False)
#--        writer.close()

#-- self service template input data validation handler
exec(compile(source=open('selfServiceTemplateInputDataValidator.py').read(), filename='selfServiceTemplateInputDataValidator.py', mode='exec'))

#-- CASTR Rules definder 
exec(compile(source=open('castrRuleDefiner.py').read(), filename='castrRuleDefiner.py', mode='exec'))

#-- Excel file handler
exec(compile(source=open('excelFileHandler.py').read(), filename='excelFileHandler.py', mode='exec'))

#-- session vaiables handler
exec(compile(source=open('sessionVariables.py').read(), filename='sessionVariables.py', mode='exec'))

global excel_file
excel_file = excelFile()

#-- global variable castr_rule_definder
global castr_rule_definder
castr_rule_definder = ruleDefiner()

# ---- globl variable user_permit
user_permit = CastrPermit()
user_permit.productionAccess()

authenticator = stauth. Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# ---- WALLE web page Title ----
status_widget("CASTR-Config Self-Service SSA Tool", "", "")

# Authentication - used when the app is hosted in a web server
#-- #-- choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])
# Obtain User Input for email and password
#-- email = st.sidebar.text_input('Please enter your email address')
#-- password = st.sidebar.text_input('Please enter your password',type = 'password')

name, authentication_status, username = authenticator.login('Login', 'main')
    
if authentication_status == None:
    st.warning('Please enter your username and password')
if authentication_status == False:
    st.error('Username/password is incorrect')

#-- continue to show the App once a user is authticated
if authentication_status:

    #--  Main menu on side bar
    exec(compile(source=open('MainPage-Sidebar.py').read(), filename='MainPage-Sidebar.py', mode='exec'))
    
    #--  handler for stacking file template file or CASTR config file
    if selected == stack_files: 
        exec(compile(source=open('stackFiles.py').read(), filename='stackFiles.py', mode='exec'))

    #--  handler for listing CASTR dashboards
    elif selected == view_quickSight_dashboard:
        exec(compile(source=open('dashboards.py').read(), filename='dashboards.py', mode='exec'))

    #--  handler for dowloading a config from production or create a new self service template for a new onboard region
    elif selected == download_prod_config_file:
        resetUserSelection()
        #--  down load CASTR production config file from workDoc
        #--  or create a brand a new self serive tempalte file
        exec(compile(source=open('castrFileSelections.py').read(), filename='castrFileSelections.py', mode='exec'))

    #--  handler for CASTR tickets
    elif selected == cut_ticket:
        exec(compile(source=open('castrTicketHanlder.py').read(), filename='castrTicketHanlder.py', mode='exec'))

    #--  handler for document requests handler on WALLE user guide, download latest version WALLE, CASTR config rules, WALLE data quality checking     
    elif selected == help_links:
        exec(compile(source=open('walleDocumentsHandler.py').read(), filename='walleDocumentsHandler.py', mode='exec'))

    #--  handler for CASTR file uploader requests handler on UAT, QA and Beta      
    elif selected == upload_configuration_file:    
        exec(compile(source=open('castrConfigFileUploader.py').read(), filename='castrConfigFileUploader.py', mode='exec'))

    #--  handler for self service template requests
    elif selected == create_self_service_template_file:
         exec(compile(source=open('selfServiceTemplateHandler.py').read(), filename='selfServiceTemplateHandler.py', mode='exec'))

    #--  handler for CASTR config file requests
    elif selected == create_configuration_file:
        exec(compile(source=open('castrConfgFileHandler.py').read(), filename='castrConfgFileHandler.py', mode='exec'))

    #--  handler for display order correction 
    elif selected == correct_configFile_displayorder:
        exec(compile(source=open('displayOrderHandler.py').read(), filename='displayOrderHandler.py', mode='exec'))

    #--  default page WALLE introduction page 
    else:
        exec(compile(source=open('walleIntroduction.py').read(), filename='walleIntroduction.py', mode='exec'))
        


