#------------------------------------------------------------------------------------------------------#
#    purpose : correct display order in castr config file or self service template file                #
#    source: CASTR config file or self servcie template file                                           #
#    output : excel file                                                                               #
#------------------------------------------------------------------------------------------------------#

#-- functions on Template builder web page
correct_file_selection_mode = option_menu(
    menu_title= "",
    options= [selection_modes.instruction.value, selection_modes.correct_display_order_self_service_template.value, selection_modes.correct_display_order_castr_config_file.value],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

file_path_name = 'None'
#--  instructions on how to build self service template
if correct_file_selection_mode == selection_modes.instruction.value:

    status_widget("","", "**If you are going to " + selection_modes.correct_display_order_self_service_template.value + " then follow the steps below** - :point_down: to continue. ")
    lst = ["1. Put all self service template file(s) in folder " + file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\", '2. Click **' + selection_modes.correct_display_order_self_service_template.value + '** :point_up:', 
            '3. WALLE will start the process automatically', '4. Once the process completes, WALLE saves a new template file in folder ' + file_location_management.file_correction_folder.value.replace("[userid]", os.getlogin()) +  "\\. Example: correct_Template_AE_Config_Data_May_15_2023_07_19_12_23_03 "]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)


    status_widget("","", "**If you are going to " + selection_modes.correct_display_order_castr_config_file.value + " then follow the steps below** - :point_down: to continue. ")
    lst = ["1. Put all CASTR config file(s) in folder " + file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin()) + "\\", '2. Click **' + selection_modes.correct_display_order_castr_config_file.value + '** :point_up:', 
            '3. WALLE will start the process automatically', '4. Once the process completes, WALLE saves a new config file in folder ' + file_location_management.file_correction_folder.value.replace("[userid]", os.getlogin()) + "\\. Example: correct_AE_Config_Data_May_15_2023_07_19_12_23_03 "]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

#-- prepare the file based on user selection
elif correct_file_selection_mode ==  selection_modes.correct_display_order_self_service_template.value:  
    file_path_name = file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\"
elif correct_file_selection_mode == selection_modes.correct_display_order_castr_config_file.value:        
    file_path_name = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin()) + "\\"

#--  continue to correct display order in the file founded
if file_path_name != 'None':  
    #load model file
    excel_file.load_file(file_location_management.modelFilePath.value.replace("[userid]", os.getlogin()), "")
    dirs = os.listdir( file_path_name )

    fileCount = 0
    #lopp folder to process each file
    for each in dirs:
        fileCount = fileCount + 1
        status_widget("", "", "Source input file: " + file_path_name + "\\" + each )
        resetUserSelection()
        
        source_file = file_path_name + "\\" + each
        if excel_file.load_file(source_file, "") == False:
            source_file = None

        if source_file is not None:    
            #-- check if sheet Template is availalbe
            if st.session_state.gd_template:
                #-- topic displayorder
                df_topic_order = castr_rule_definder.createDisplayorder(excel_file.df_template, 'topic',  None)
                #-- test displayorder
                df_test_order = castr_rule_definder.createDisplayorder(excel_file.df_template, 'test',  None)
                #-- aspect displayorder
                df_aspect_order = castr_rule_definder.createDisplayorder(excel_file.df_template, 'aspect',  None)
                #-- loop template to sign a displayOrder for topic/test/aspect         
                tmp_template = pd.merge( excel_file.df_template, df_topic_order,how="left", left_on=['topic'], right_on='topic')              
                tmp_template.rename(columns={'displayOrder_y': 'topic_displayOrder', 'displayOrder_x':'displayOrder'}, inplace=True)
                tmp_template = pd.merge( tmp_template, df_test_order,how="left", left_on=['test'], right_on='test')
                tmp_template.rename(columns={'displayOrder_y': 'test_displayOrder', 'displayOrder_x':'displayOrder'}, inplace=True)
                tmp_template = pd.merge( tmp_template, df_aspect_order,how="left", left_on=['aspect'], right_on='aspect')

                tmp_template.rename(columns={'displayOrder_y': 'aspect_displayOrder', 'displayOrder_x':'displayOrder'}, inplace=True)
                tmp_template['order_created'] = tmp_template['topic_displayOrder'] + tmp_template['test_displayOrder'] + tmp_template['aspect_displayOrder']
                tmp_template['order_created'] = tmp_template['order_created'].astype(int)
                

                with st.spinner("WALLE is saving template file..."):        
                    file_name = "correct_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"        
                    save_file_path_name = file_location_management.correction_file_path.value.replace("[userid]", os.getlogin()) + "\\" + file_name
                    excel_file_save = excelFile()
                    excel_file_save.create_writer(save_file_path_name ) 
                    excel_file.create_template_column_list()
                    
                    with excel_file_save.writer as writer: 
                        #-- (tmp_template[excel_file.selfService_template_column_list].drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template", index = False)                       
                        tmp_template[excel_file.selfService_template_column_list].to_excel(writer, sheet_name = "Template", index = False)                       
                        (excel_file.df_template_dataFactSources.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_DataFactSources", index = False)
                        (excel_file.df_template_dataFacts.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_DataFacts", index = False)
                        (excel_file.df_template_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Template_AuditRules", index = False)
                        (excel_file.df_template_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "Temp_AuditConfigurationDetails", index = False)

                        writer.close()
                        status_widget("","Above data has been saved in: " + save_file_path_name,"")

            #-- check if the Template/Template_AuditRules/Template_DataFacts/Template_DataFactSources are availalbe
            if st.session_state.gd_dataFacts and st.session_state.gd_dataFactSources and st.session_state.gd_auditRules and st.session_state.gd_configurationDetails:
                #-- topic displayorder
                df_topic_order = castr_rule_definder.createDisplayorder(excel_file.df_auditRules, 'topic',  excel_file.df_auditConfigurationDetails)
                #-- test displayorder
                df_test_order = castr_rule_definder.createDisplayorder(excel_file.df_auditRules, 'test',  excel_file.df_auditConfigurationDetails)
                #-- aspect displayorder
                df_aspect_order = castr_rule_definder.createDisplayorder(excel_file.df_auditRules, 'aspect',  excel_file.df_auditConfigurationDetails)

                #-- loop auditRules to sign a displayOrder for topic/test/aspect                           
                tmp_auditRules = pd.merge( excel_file.df_auditRules, df_topic_order,how="left", left_on=['topic'], right_on='topic')
                tmp_auditRules.rename(columns={'displayOrder': 'topic_displayOrder'}, inplace=True)
                
                tmp_auditRules = pd.merge( tmp_auditRules, df_test_order,how="left", left_on=['test'], right_on='test')
                tmp_auditRules.rename(columns={'displayOrder': 'test_displayOrder'}, inplace=True)
                tmp_auditRules = pd.merge( tmp_auditRules, df_aspect_order,how="left", left_on=['aspect'], right_on='aspect')
                tmp_auditRules.rename(columns={'displayOrder': 'aspect_displayOrder'}, inplace=True)
                tmp_auditRules['order_created'] = tmp_auditRules['topic_displayOrder'] + tmp_auditRules['test_displayOrder'] + tmp_auditRules['aspect_displayOrder']
                
                #-- tmp_auditRules
                tmp_auditRules['order_created'] = tmp_auditRules['order_created'].astype(int)
                                            
                #-- merge to auditDetails to correct display Order
                excel_file.df_auditConfigurationDetails = pd.merge( excel_file.df_auditConfigurationDetails, tmp_auditRules[['id','topic','test','aspect','order_created']] ,how="left", left_on=['aspectId'], right_on='id')
                #-- replace display order with new created order
                excel_file.df_auditConfigurationDetails['displayOrder'] = excel_file.df_auditConfigurationDetails['order_created']
                # -- keep columns required by CASTR only
                excel_file.df_auditConfigurationDetails = excel_file.df_auditConfigurationDetails[excel_file.auditConfigurationDetails_column_list]

                with st.spinner("WALLE is saving template file..."):        
                    file_name = "correct_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"        
                    save_file_path_name = root_folder.replace("[userid]", os.getlogin()) + "\\Correction\\" + file_name
                    excel_file_save = excelFile()
                    excel_file_save.create_writer(save_file_path_name ) 
                    with excel_file_save.writer as writer:                        
                        (excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFactSources", index = False)
                        (excel_file.df_dataFacts.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFacts", index = False)
                        (excel_file.df_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditRules", index = False)
                        (excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)

                        writer.close()
                        status_widget("","Above data has been saved in: " + save_file_path_name,"")
                
        if fileCount == 0:
            info_widget("", "No file found in " + file_path_name,"success")    
