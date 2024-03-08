 #---------------------------------------------------------------#
#    purpose : stack excel files to a single file                #
#    source: 1> CASTR config file; 2> self service template file #
#    output : excel file                                         #
#---------------------------------------------------------------_#

#-- functions on Template builder web page
file_selection_mode = option_menu(
    menu_title= "",
    options= [selection_modes.instruction.value, selection_modes.stack_castr_config_file.value, selection_modes.stack_self_service_template.value, buildAuditTypesSheet, buildMilestonesSheet],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

#--  instructions on how to build self service template
if file_selection_mode == selection_modes.instruction.value:
    status_widget("","", "**If you are going to " + selection_modes.stack_castr_config_file.value + " then follow the steps below** - :point_down: to continue. ")
    lst = ["1. CASTR config files must be located in folder " + file_location_management.castr_config_file_folder.value, '2. Click **' + selection_modes.stack_castr_config_file.value + '** :point_up:', 
            '3. Once the process completes, WALLE saves a stacked file in folder ' + file_location_management.castr_config_file_folder.value + "\\. Example: stack_AE_Config_Data_May_15_2023_07_19_12_23_03 "]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    status_widget("","", "**If you are going to " + selection_modes.stack_self_service_template.value + " then follow the steps below** - :point_down: to continue. ")
    lst = ["1. Self service template files must be located in folder " + file_location_management.self_service_template_file_folder.value, '2. Click **Start to Stack Self Service Template** :point_up:', 
            '3. Once the process completes, WALLE saves a stacked file in folder ' + file_location_management.self_service_template_file_folder.value + "\\. Example: stack_Template_AE_Config_Data_May_15_2023_07_19_12_23_03 "]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

#-- stack self service template
elif file_selection_mode == selection_modes.stack_self_service_template.value:
    fileCount = 0
    file_path = file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\"
    df_stack_template =pd.DataFrame()            
    for each in os.listdir(file_path):
        fileCount = fileCount + 1
        if os.path.isfile( file_path + "\\" + each):                  
            excel_file.load_file(file_path + "\\" + each, "")
            df_stack_template = pd.concat([df_stack_template, excel_file.df_template.drop(labels='unique_index', axis=1)])
        else:
            new_path = (file_path + each + "\\")
            for sub_each in os.listdir(new_path):
                excel_file.load_file(new_path + "\\" + sub_each, "")
                df_stack_template = pd.concat([df_stack_template, excel_file.df_template.drop(labels='unique_index', axis=1)])

    if fileCount == 0:
        info_widget("", "No file found in " + file_path,"success")
    else:   
        with st.spinner("The source file(s) has been stacked successfully! WALLE is saving these data to a file.."):               
            status_widget("","","Stacked Template(s)")
            gd_stack_template =grid_builder(df_stack_template, user_permit.permit)

            info_widget("","The source file(s) has been stacked successfully. ","success")

            excel_file_save = excelFile()
            file_path_name = file_path  + "stack_template_configuration_file_" + datetime.datetime.now().strftime('%Y_%m_%d') + ".xlsx"
            excel_file_save.create_writer(file_path_name) 
            with excel_file_save.writer as writer:                 
                df_stack_template.to_excel(writer, sheet_name = "Template", index = False)
                writer.close()

            status_widget("","Above data has been saved in this file: " + file_path_name,"")

#-- stack castr config file
elif file_selection_mode == selection_modes.stack_castr_config_file.value:
    fileCount = 0
    file_path = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin()) + "\\"
    df_stack_auditRules = pd.DataFrame()
    df_stack_auditConfigurationDetails = pd.DataFrame()
    df_stack_dataFacts = pd.DataFrame()
    df_stack_dataFactSources = pd.DataFrame()
    with st.spinner("WALLE is stacking file(s)..."):                
        for each in os.listdir(file_path):
            fileCount = fileCount + 1
            excel_file.load_file(file_path + "\\" + each, "")
            df_stack_auditRules =  pd.concat([df_stack_auditRules,excel_file.df_auditRules.drop(labels='unique_index', axis=1)])
            df_stack_auditConfigurationDetails =  pd.concat([df_stack_auditConfigurationDetails,excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)])
            df_stack_dataFacts =  pd.concat([df_stack_dataFacts,excel_file.df_dataFacts.drop(labels='unique_index', axis=1)])
            df_stack_dataFactSources =  pd.concat([df_stack_dataFactSources,excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)]) 
        
        if fileCount == 0:
            info_widget("", "No file found in " + file_path,"success")
        else: 
            status_widget("","","AuditConfiguratioDetails")
            gd_stack_auditConfigurationDetails =grid_builder(df_stack_auditConfigurationDetails, user_permit.permit, 600, fileCount)
            status_widget("","","AuditRules")
            gd_stack_auditRules =grid_builder(df_stack_auditRules,user_permit.permit,600, fileCount+1000)
            status_widget("","","DataFacts")
            gd_stack_dataFacts =grid_builder(df_stack_dataFacts, user_permit.permit, 600, fileCount+2000)
            status_widget("","","DataFactSources")
            gd_stack_dataFactSources =grid_builder(df_stack_dataFactSources, user_permit.permit, 600, fileCount+3000)
        
            info_widget("","The source file(s) has been stacked successfully. ","success")
            excel_file_save = excelFile()
            file_path_name = file_path  + "stack_configuration_file_" + datetime.datetime.now().strftime('%Y_%m_%d') + ".xlsx"
            excel_file_save.create_writer(file_path_name) 
        
            with excel_file_save.writer as writer: 
                df_stack_auditConfigurationDetails.to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)
                df_stack_auditRules.to_excel(writer, sheet_name = "AuditRules", index = False)
                df_stack_dataFacts.to_excel(writer, sheet_name = "DataFacts", index = False)
                df_stack_dataFactSources.to_excel(writer, sheet_name = "DataFactSources", index = False)
                writer.close()
                
            status_widget("","","Above data has been saved in this file: " + file_path_name)  
    df_stack_auditRules = pd.DataFrame()
    df_stack_auditConfigurationDetails = pd.DataFrame()
    df_stack_dataFacts = pd.DataFrame()
    df_stack_dataFactSources = pd.DataFrame()
    with st.spinner("WALLE is stacking file(s)..."):                
        for each in os.listdir(file_path):
            fileCount = fileCount + 1
            excel_file.load_file(file_path + "\\" + each, "")
            df_stack_auditRules =  pd.concat([df_stack_auditRules,excel_file.df_auditRules.drop(labels='unique_index', axis=1)])
            df_stack_auditConfigurationDetails =  pd.concat([df_stack_auditConfigurationDetails,excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)])
            df_stack_dataFacts =  pd.concat([df_stack_dataFacts,excel_file.df_dataFacts.drop(labels='unique_index', axis=1)])
            df_stack_dataFactSources =  pd.concat([df_stack_dataFactSources,excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)]) 
        
        if fileCount == 0:
            info_widget("", "No file found in " + file_path,"success")
        else: 
            status_widget("","","AuditConfiguratioDetails")
            gd_stack_auditConfigurationDetails =grid_builder(df_stack_auditConfigurationDetails, user_permit.permit, 600, fileCount)
            status_widget("","","AuditRules")
            gd_stack_auditRules =grid_builder(df_stack_auditRules,user_permit.permit,600, fileCount+1000)
            status_widget("","","DataFacts")
            gd_stack_dataFacts =grid_builder(df_stack_dataFacts, user_permit.permit, 600, fileCount+2000)
            status_widget("","","DataFactSources")
            gd_stack_dataFactSources =grid_builder(df_stack_dataFactSources, user_permit.permit, 600, fileCount+3000)
        
            info_widget("","The source file(s) has been stacked successfully. ","success")
            excel_file_save = excelFile()
            file_path_name = file_path  + "stack_configuration_file_" + datetime.datetime.now().strftime('%Y_%m_%d') + ".xlsx"
            excel_file_save.create_writer(file_path_name) 
        
            with excel_file_save.writer as writer: 
                df_stack_auditConfigurationDetails.to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)
                df_stack_auditRules.to_excel(writer, sheet_name = "AuditRules", index = False)
                df_stack_dataFacts.to_excel(writer, sheet_name = "DataFacts", index = False)
                df_stack_dataFactSources.to_excel(writer, sheet_name = "DataFactSources", index = False)
                writer.close()
                
            status_widget("","Above data has been saved in this file: " + file_path_name,"")                 

#-- build a milestone sheet from auditConfiguarionDetails sheet
elif file_selection_mode == buildMilestonesSheet:
    resetUserSelection()
    config_file_path = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin())
    correction_file_path = file_location_management.file_correction_folder.value.replace("[userid]", os.getlogin()) + "\\"
    for each in os.listdir(config_file_path):
        source_file = config_file_path + "\\" + each
        excel_file.load_file(source_file, "") 
        if st.session_state.gd_configurationDetails:
            excel_file.createMilestonesTab(excel_file.df_auditConfigurationDetails)
            #-- save the file
            with st.spinner("WALLE is saving the file..."):  
                file_name = "correct_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"   
                save_file_path_name = correction_file_path + file_name     
                excel_file_save = excelFile()
                excel_file_save.create_writer(save_file_path_name ) 
                #-- excel_file.create_template_column_list()
                
                with excel_file_save.writer as writer:                      
                    (excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFactSources", index = False)
                    (excel_file.df_dataFacts.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFacts", index = False)
                    (excel_file.df_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditRules", index = False)
                    (excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)
                    if st.session_state.gd_mr_auditTypes: 
                        excel_file.df_mr_auditTypes.to_excel(writer, sheet_name = "MR_AuditTypes", index = False)
                    if st.session_state.gd_mr_milestones: 
                        excel_file.df_mr_milestones.to_excel(writer, sheet_name = "MR_Milestones", index = False)    
                    writer.close()
                    status_widget("","Above data has been saved in: " + save_file_path_name,"")

#-- build a audit type sheet from auditConfiguarionDetails sheet
elif file_selection_mode == buildAuditTypesSheet:
    resetUserSelection()
    config_file_path = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin())
    correction_file_path = file_location_management.file_correction_folder.value.replace("[userid]", os.getlogin()) + "\\"
    for each in os.listdir(config_file_path):
        source_file = config_file_path + "\\" + each
        excel_file.load_file(source_file, "") 

        if st.session_state.gd_configurationDetails:
            excel_file.createAuditTypesTab(excel_file.df_auditConfigurationDetails)
            #-- save the file
            with st.spinner("WALLE is saving the file..."):    
                file_name = "correct_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"   
                save_file_path_name = correction_file_path + file_name     
                excel_file_save = excelFile()
                excel_file_save.create_writer(save_file_path_name ) 
                #-- excel_file.create_template_column_list()
                
                with excel_file_save.writer as writer:                      
                    (excel_file.df_dataFactSources.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFactSources", index = False)
                    (excel_file.df_dataFacts.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "DataFacts", index = False)
                    (excel_file.df_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditRules", index = False)
                    (excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)
                    if st.session_state.gd_mr_auditTypes: 
                        excel_file.df_mr_auditTypes.to_excel(writer, sheet_name = "MR_AuditTypes", index = False)
                    if st.session_state.gd_mr_milestones: 
                        excel_file.df_mr_milestones.to_excel(writer, sheet_name = "MR_Milestones", index = False) 
                    
                    writer.close()
                    status_widget("","Above data has been saved in: " + save_file_path_name,"")