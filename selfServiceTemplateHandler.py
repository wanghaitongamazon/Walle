#---------------------------------------------------------------#
#    purpose : create self service template file                #
#    source: CASTR config file                                  #
#    output : excel file with with a tab, tab name is Tempalte  #
#---------------------------------------------------------------#

#-- functions on Template builder web page
template_action_selection_mode = option_menu(
    menu_title= "",
    options= [selection_modes.instruction.value, selection_modes.build_self_service_template.value],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

#-- defined folder location where CASTR configuration file 
file_path_name = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin()) + "\\"

#--  instructions on how to build self service template
if template_action_selection_mode == selection_modes.instruction.value:

    status_widget("","", "**If you are going to create a self service template base off a config file then follow the steps below** - :point_down: to continue. ")
    lst = ["1. CASTR config must exist in folder " + file_path_name, '2. Click **' + selection_modes.build_self_service_template.value + '** :point_up:', 
            '3. WALLE validates input data and builds a self service template', '4. Once the process completes, WALLE saves the template file in folder ' + file_path_name + "\\. Example: Template_AE_Config_Data_May_15_2023_07_19_12_23_03 "]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

#--  start to build self service template
elif template_action_selection_mode == selection_modes.build_self_service_template.value:     

    #-- load model file
    excel_file.load_file(file_location_management.modelFilePath.value.replace("[userid]", os.getlogin()), "")
    dirs = os.listdir( file_path_name )

    fileCount = 0
    #-- loop folder to process each input source file
    for each in dirs:
        fileCount = fileCount + 1
        status_widget("", "", "Source input file: " + file_path_name + "\\" + each )

        #-- reset session variables
        resetUserSelection()
        
        source_file = file_path_name + "\\" + each

        #-- exit, no file found in source folder
        if excel_file.load_file(source_file, "") == False:
            source_file = None

        #-- source file found, continute to processing this file
        if source_file is not None:    
            
            #-- continue to build template only if sheets AuditConfigurationDetails, AuditRules, DataFacts and DataFactSources are availalbe in source input file
            if st.session_state.gd_dataFacts and st.session_state.gd_dataFactSources and st.session_state.gd_auditRules and st.session_state.gd_configurationDetails:
                with st.spinner("Self service template file is being built..."):                    
                    #-- This is dataframe has all available columns for any update later
                    excel_file.create_template_column_list()

                    df_new_template_1 = excel_file.df_auditConfigurationDetails
                    df_new_template_1 = pd.merge(df_new_template_1, excel_file.df_auditRules, how="left", left_on='aspectId', right_on='id').drop(labels='unique_index_y', axis=1)
                    df_new_template_1.rename(columns={'unique_index_x':'unique_index'}, inplace=True)
                    df_new_template_1['FactName_1 (Later Date/Larger Number)'] = ""
                    df_new_template_1['Fact_Operator'] = ""
                    df_new_template_1['FactName_2 (Earlier Date/Smaller Number)'] = ""

                    #-- non calculate datafacts only      
                    df_new_template_1 = pd.merge(df_new_template_1, excel_file.df_dataFacts, how="left", left_on='dataFacts', right_on='id').drop(labels='id_y', axis=1).drop(labels='unique_index_y', axis=1)
                    df_new_template_1.rename(columns={'unique_index_x':'unique_index'}, inplace=True)
                    df_new_template_1.rename(columns={'name':'dataFactName'}, inplace=True)
                    df_new_template_1.rename(columns={'id_x':'id'}, inplace=True)
                    df_new_template_1 = pd.merge(df_new_template_1, excel_file.df_dataFactSources, how="left", left_on='dataFactSourceId', right_on='id').drop(labels='id_y', axis=1).drop(labels=['unique_index_y'], axis=1)
                    df_new_template_1.rename(columns={'name':'document'}, inplace=True)
                    df_new_template_1.rename(columns={'id_x':'id'}, inplace=True)
                    df_new_template_1.rename(columns={'unique_index_x':'unique_index'}, inplace=True)           
                    df_new_template_1['calculation'] = ""
                    df_new_template_1['FactID_2'] = ""
                    df_new_template_1['FactID_1'] = ""

                    # calculate datafacts - need to split datafacts to fact1_name/fact2_name
                    where1 = df_new_template_1['dataFacts'].str.contains(',', na=False)
                    df_1 = df_new_template_1[where1]
                    if (len(df_1)> 0):
                        #-- new data frame with split value columns
                        new = df_1["dataFacts"].str.split(",", n = 2, expand = True)
                        df_1["dataFacts_1_new"] = new[0].str.strip()
                        df_1["dataFacts_2_new"] = new[1].str.strip()
                        df_1["dataFacts_3_new"] = new[2].str.strip()

                        #-- calculation
                        df_1 = pd.merge(df_1.drop(labels=['type','expression','dataFactName','displayInputUnit','FactName_1 (Later Date/Larger Number)','FactID_1','FactID_2','dataFactSourceId','entity', 'calculation'], axis=1), excel_file.df_dataFacts, how="left", left_on='dataFacts_3_new', right_on='id').drop(labels='id_y', axis=1).drop(labels=['unique_index_y'], axis=1)
                        df_1.rename(columns={'id_x': 'id', 'name': 'dataFactName','dataFacts_1_new':'FactID_1', 'dataFacts_2_new':'FactID_2', 'dataFacts_3_new':'calculation'}, inplace=True)
                
                        #-- datafact_1 name, inputComponent
                        df_1 = pd.merge(df_1, excel_file.df_dataFacts[['id','name','type', 'dataFactSourceId']], how="left", left_on='FactID_1', right_on='id').drop(labels='id_y', axis=1)
                        df_1.rename(columns={'id_x': 'id', 'type_x':'type', 'name':'FactName_1 (Later Date/Larger Number)', 'type_y':'FactName_1_inputComponent', 'dataFactSourceId_x':'dataFactSourceId', 'dataFactSourceId_y':'dataFactSourceId_1', 'unique_index_x':'unique_index'}, inplace=True)
                        
                        #-- datafact_1 document 
                        df_1 = pd.merge(df_1, excel_file.df_dataFactSources[['id','name']], how="left", left_on='dataFactSourceId_1', right_on='id').drop(labels='id_y', axis=1)
                        df_1.rename(columns={'id_x': 'id', 'name':'FactName_1_Document'}, inplace=True)

                        # datafact_2, name, inputComponent
                        df_1 = pd.merge(df_1.drop(labels=['FactName_2 (Earlier Date/Smaller Number)'], axis=1), excel_file.df_dataFacts[['id','name','type','dataFactSourceId']], how="left", left_on='FactID_2', right_on='id').drop(labels='id_y', axis=1)
                        df_1.rename(columns={'id_x': 'id', 'type_x':'type', 'name':'FactName_2 (Earlier Date/Smaller Number)','type_y':'FactName_2_inputComponent', 'dataFactSourceId_x':'dataFactSourceId', 'dataFactSourceId_y':'dataFactSourceId_2'}, inplace=True)
                        
                        #-- datafact_2 document 
                        df_1 = pd.merge(df_1, excel_file.df_dataFactSources[['id','name']], how="left", left_on='dataFactSourceId_2', right_on='id').drop(labels='id_y', axis=1)
                        df_1.rename(columns={'id_x': 'id', 'name':'FactName_2_Document'}, inplace=True)

                        df_1['Fact_Operator'] = "\"-\""
                        df_1['document'] = 'Calculated'

                        df_new_template_1 = pd.concat([df_new_template_1[~where1], df_1], ignore_index=True) 

                    #-- make sure new template sheet has all fields from CASTR config file and model file
                    cols = df_1.columns.values.tolist()
                    for column in excel_file.selfService_template_column_list:
                        if column not in (cols):
                            df_new_template_1[column] = ""

                    #-- mark S, sepcial handling row if rows without aspect id and signed a default display order number
                    where1 = df_new_template_1['aspectId'].str.strip() == ''
                    for ind in df_new_template_1.index:
                        if (df_new_template_1['aspectId'][ind] == ''):
                            df_new_template_1['ModifyDeleteNew'][ind] = 'S'
                            df_new_template_1['displayOrder'][ind] = 999999999 

                    #-- split displayOrder to topic_displayOrder, test_displayOrder and aspect_displayOrder
                    df_new_template_1['displayOrder_1'] = df_new_template_1['displayOrder'].astype(int)
                    df_new_template_1['displayOrder_1'] = df_new_template_1['displayOrder_1'].apply(lambda x: f'{x:09d}')
                    df_new_template_1['topic_displayOrder'] = df_new_template_1['displayOrder_1'].str[:3]
                    df_new_template_1['topic_displayOrder'] = df_new_template_1['topic_displayOrder'].astype(int)
                    df_new_template_1['test_displayOrder'] = df_new_template_1['displayOrder_1'].str[3:6]
                    df_new_template_1['test_displayOrder'] = df_new_template_1['test_displayOrder'].astype(int)
                    df_new_template_1['aspect_displayOrder'] = df_new_template_1['displayOrder_1'].str[6:9]
                    df_new_template_1['aspect_displayOrder'] = df_new_template_1['aspect_displayOrder'].astype(int)
                                                                                                                            
                    #-- create conditional test sheet
                    excel_file.createConditionalTestsTab(df_new_template_1)
                    
                    #-- hiding ID fields to avoid any confusion on weg page
                    excel_file.display_template_required_column(df_new_template_1)

                    #-- display Template on web page
                    grid_builder(excel_file.df_template_display, False, 600, fileCount)
                    
                    #-- continue to save the final file
                    with st.spinner("WALLE is saving template file..."):        
                        file_name = "Template_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"        
                        save_file_path_name =file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\" + file_name
                        excel_file_save = excelFile()
                        excel_file_save.create_writer(save_file_path_name ) 
                        with excel_file_save.writer as writer:    
                            #save conditional test tab
                            excel_file.df_conditionTests.to_excel(writer, sheet_name = "ConditionalTests", index = False)
                            
                            df_1 = df_new_template_1[excel_file.selfService_template_column_list]
                            df_1 = pd.DataFrame(df_1[excel_file.selfService_template_column_list]).drop(labels='unique_index', axis=1)
                            df_1.to_excel(writer, sheet_name = "Template", index = False)
                            worksheet = writer.sheets['Template']
                            workbook = writer.book
                        
                            # read only column Green fill with dark green text.
                            green_format = workbook.add_format({'bg_color':   '#C6EFCE',
                                                        'font_color': '#006100'})

                            # Create a cell format with protection properties.
                            unlocked = workbook.add_format({'locked': False})
                            
                            cols = df_1.columns.values.tolist()
                            filterRange = ""
                            for column in cols:
                                col_idx = cols.index(column)
                                if column in (excel_file.df_SST_template_ReadOnlyColumns_list):
                                    #hidden
                                    worksheet.set_column(get_column_letter(col_idx + 1) + ':' + get_column_letter(col_idx + 1), None,  green_format, {'hidden': True})
                                else:
                                    worksheet.set_column(get_column_letter(col_idx + 1) + ':' + get_column_letter(col_idx + 1), None,  unlocked)
                                    filterRange = get_column_letter(col_idx + 1)
                            
                            filterRange = "A1" + ":" + filterRange + "1"
                            worksheet.autofilter(filterRange)
                            # Turn worksheet protection on.
                            worksheet.protect('',{'insert_rows': True, 'format_columns': True, 'autofilter':True,'format_cells':True})

                            (excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_DataFactSources", index = False)
                            worksheet = writer.sheets['Template_DataFactSources']
                            worksheet.hide()
                            (excel_file.df_dataFacts.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_DataFacts", index = False)
                            worksheet = writer.sheets['Template_DataFacts']
                            worksheet.hide()
                            (excel_file.df_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_AuditRules", index = False)
                            worksheet = writer.sheets['Template_AuditRules']
                            worksheet.hide()
                            (excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Temp_AuditConfigurationDetails", index = False)
                            worksheet = writer.sheets['Temp_AuditConfigurationDetails']
                            worksheet.hide()
                            writer.close()

                            ## with open(file_path_name, 'rb') as my_file:
                            ##s download_button_str = st.download_button(label = 'Click me to download the file and save it to your local computer', data = my_file, file_name = file_name, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      
                            status_widget("","", "Above data has been saved in: " + save_file_path_name)

                
            else:
                status_widget("", "WALLE Stopped - load source configuration file:  ","")
                if not st.session_state.gd_dataFacts:
                    info_widget("","tab " + castr_config_file.datafacts.value  + " is missing! ",'error')
                if not st.session_state.gd_dataFactSources:
                    info_widget("","tab " + castr_config_file.dataFactSources.value + " is missing! ",'error')
                if not st.session_state.gd_auditRules:
                    info_widget("","tab " + castr_config_file.auditRules.value + " is missing! ",'error')      
    
    if fileCount == 0:
        info_widget("", "No file found in " + file_path_name,"success")
    else:
        info_widget("", "You can update self service template offline" ,"success")