#----------------------------------------------------------------------------------------------------------------------------#
#    purpose : create CASTR config file                                                                                      #
#    source: self service template file                                                                                      #
#    output : excel file with with 4 tabs, tab name is auditrules, auditconfigurationdetails, datafacts and datafactsources  #
#----------------------------------------------------------------------------------------------------------------------------#



#-- functions on config file builder web page
user_selection_mode = option_menu(
    menu_title= "",
    options= [selection_modes.instruction.value, selection_modes.build_castr_config_file.value, selection_modes.add_conditional_test.value],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

#-- defined folders for CASTR configuration file, self service template file and conditional tests file
file_path_name = file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\"
config_file_path = file_location_management.castr_config_file_folder.value.replace("[userid]", os.getlogin()) + "\\"
correction_file_path = file_location_management.file_correction_folder.value.replace("[userid]", os.getlogin()) + "\\"

#--  instructions on how to build castr configuration file
if user_selection_mode == selection_modes.instruction.value:
    status_widget("","", "**If you are going to create a " + file_name_management.castr_config_file.value + " then the steps below - :point_down: to continue.** ")
    lst = ["1. Template file must exist in folder " + file_path_name, '2. Must have folder ready  ' + file_location_management.castr_config_file_folder.value , '3. Click **' +  selection_modes.build_castr_config_file.value + '** :point_up:', 
            '4. WALLE validates input data and builds a ' + file_name_management.castr_config_file.value, '5. WALLE stops when a invalid data input in a template.', '6. User must follow the instruction on the page and fix a error off line.', 
            '7. Once the process completes, WALLE saves the ' + file_name_management.castr_config_file.value + ' in folder ' + file_location_management.castr_config_file_folder.value + "\\.  Example, US_configuration_file_2023_07_19", 
            '8. *This part of process does not include condtional test handling*',
            '9. *Notify TAP team if there is a new audit type intruduced in the file*']
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    status_widget("","", "**If you are going to " + selection_modes.add_conditional_test.value + " then the steps below - :point_down: to continue.** ")
    lst = ["1. Must finalize test aspects in CASTR config before adding condtional test ", "2. Config file must have a tab named ConditionalTests", "3. Config file must be located in folder " + config_file_path, 
            '3. Must have folder ready  ' + file_location_management.file_correction_folder.value + ". Final file is saved in this folder ", '4. in tab ConditionalTests, each dependentTestAspect and its dependentTest must be in a single row  ', 
            '5. in tab ConditionalTests, must provide topic, parentTest, parentTestAspect and dependentTest and dependentTestAspect  ',  '6. in tab ConditionalTests, leave parentTestAspectId and dependentTestAspectId blank ',
            '7. Click ** ' + selection_modes. add_conditional_test.value + ' ** :point_up:']
            
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

#--  start to build castr config file
elif user_selection_mode == selection_modes.build_castr_config_file.value:

    lst = ['1. *This part of process does not include condtional test handling*',
            '2. *Notify TAP team if there is a new audit type intruduced in the file*']
    
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    #-- load model file
    excel_file.load_file(file_location_management.modelFilePath.value.replace("[userid]", os.getlogin()), "")

    fileCount = 0
    #-- loop folder to process each input source file
    for each in os.listdir(file_path_name):
        fileCount = fileCount + 1
        status_widget("", "", str(fileCount) + ". Source input file: " + file_path_name + "\\" + each )

        #-- reset session variables
        resetUserSelection()
        
        source_file = file_path_name + "\\" + each
        #-- exit, no file found in source folder
        if excel_file.load_file(source_file, create_configuration_file) == False:
            source_file = None
            
        bValid = False
        #-- source file found, continute to processing this file
        if source_file is not None:   
            #-- continue to build config file on if the Template/Template_AuditRules/Template_DataFacts/Template_DataFactSources are availalbe
            if st.session_state.gd_template_dataFacts and st.session_state.gd_template_dataFactSources and st.session_state.gd_template_auditRules and st.session_state.gd_template:
                bValid = True     
                if  bValid == True:
                    #-- delete aspect id from AuditConfigurationDetails and AuditRules if there any 
                    if len(excel_file.df_template_delete) > 0:
                        #-- delete from AuditConfigurationDetails by business/aspectid
                        where1 = excel_file.df_template_auditConfigurationDetails['aspectId'].str.lower().isin( excel_file.df_template_delete['aspectId'].str.lower().values.tolist())
                        where2 = excel_file.df_template_auditConfigurationDetails['business'].str.lower().isin( excel_file.df_template_delete['business'].str.lower().values.tolist())
                        excel_file.df_template_auditConfigurationDetails = excel_file.df_template_auditConfigurationDetails[~(where1 & where2)]

                        #-- Only delete this aspectId from AuditRules if it is being used in only one business
                        if len(excel_file.df_template_auditConfigurationDetails[where1]) == 0: 
                            where1 = excel_file.df_template_auditRules['id'].str.lower().isin( excel_file.df_template_delete['aspectId'].str.lower().values.tolist())
                            excel_file.df_template_auditRules = pd.DataFrame(excel_file.df_template_auditRules[~where1])

                    #-- modified aspectId if there any 
                    if len(excel_file.df_template_modification) > 0:

                        castr_rule_definder.location = excel_file.df_template_modification['location'].unique()
                        
                        unique_index = 9999
                        # iterate through each row and select
                        for ind in excel_file.df_template_modification.index:
                            unique_index = unique_index + 1
                            tmp_id = excel_file.df_template_modification['aspectId'][ind]
                            # -- exclude holiday list                   
                            if (excel_file.df_template_modification['location'][ind] not in excel_file.holiday_location_list):         

                                castr_rule_definder.rule_id_prefix(excel_file.df_template_modification['business'][ind])

                                #-- document change
                                if (excel_file.df_template_modification['document'][ind].lower() in excel_file.df_template_dataFactSources['name'].str.lower().values.tolist()):
                                    #-- existing document
                                    where1 =  excel_file.df_template_dataFactSources['name'] == excel_file.df_template_modification['document'][ind]
                                    excel_file.df_template_modification['dataFactSourceId'][ind] = excel_file.df_template_dataFactSources[where1]['id'].values[0]
                                else:
                                    #-- create a new datafactsource Id for non calculate test aspect
                                    if (excel_file.df_template_modification['FactName_1 (Later Date/Larger Number)'][ind] == ''):
                                        if (excel_file.df_template_modification['inputComponent'][ind] == 'Number' and excel_file.df_template_modification['document'][ind] == 'Calculated' and excel_file.df_template_modification['entity'][ind] == 'Employee'):
                                            excel_file.df_template_modification['DataFactSourceId'][ind]=excel_file.df_template_modification['location'] + "_Calculated"
                                        elif (excel_file.df_template_modification['inputComponent'][ind] == "Number" and excel_file.df_template_modification['document'][ind] == "ADP/PAYCOM" and excel_file.df_template_modification['entity'][ind] == "Carrier"):
                                            excel_file.df_template_modification['DataFactSourceId'][ind]=excel_file.df_template_modification['location'] + "_ADP_PAYCOM"
                                        else:    
                                            excel_file.df_template_modification['dataFactSourceId'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_modification['document'][ind].replace(' ', "_").replace('"', '').replace(',', '')
                                            
                                            #-- need to check if differencet id for same document
                                            n = 0
                                            while (excel_file.df_template_modification['dataFactSourceId'][ind] in excel_file.df_template_dataFactSources['id'].str.lower().values.tolist()):
                                                n = n + 1
                                                excel_file.df_template_modification['dataFactSourceId'][ind] = excel_file.df_template_modification['dataFactSourceId'][ind] + "_" + n
                                                if n == 6:
                                                    break
                                    else:
                                        #-- calculate test aspect, check fact_1, fact_a and calculation
                                        # fact_1
                                        where1 =  excel_file.df_template_dataFactSources['id'] == excel_file.df_template_modification['FactID_1'][ind]
                                        if ( len(excel_file.df_template_dataFactSources[where1]) > 0):
                                            df_1 = excel_file.df_template_dataFactSources[where1]
                                            df_1['name'] = excel_file.df_template_modification['FactName_1 (Later Date/Larger Number)'][ind]
                                            excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources[~where1], df_1], ignore_index=False) 
                                            #--excel_file.df_template_dataFactSources = excel_file.df_template_dataFactSources[~where1].append(df_1, ignore_index=False)
                                        else:
                                            # Stop - since calculation is changes
                                            sys.exit(0)

                                        excel_file.df_template_modification['dataFactSourceId'][ind] = excel_file.df_template_modification['location'][ind] + '_Calculated'
                                        excel_file.df_template_modification['document'][ind] = 'Calculated'

                                    #-- add this new id to datafactsource
                                    df_1 = excel_file.df_template_dataFactSources[excel_file.df_template_dataFactSources['unique_index']==1]
                                    df_1['id'] = excel_file.df_template_modification['dataFactSourceId'][ind]
                                    df_1['name'] =excel_file.df_template_modification['document'][ind]
                                    df_1['unique_index']=  unique_index
                                    excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources, df_1],ignore_index=True) 
                                    #-- excel_file.df_template_dataFactSources = excel_file.df_template_dataFactSources.append(df_1,ignore_index=True)
                                    excel_file.df_template_dataFactSources.drop_duplicates(subset=['id','name'],inplace=True)
                                
                                #-- FactName_1 (Later Date/Larger Number) change
                                if (excel_file.df_template_modification['FactName_1 (Later Date/Larger Number)'][ind] != ''):
                                    where1 = excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['FactID_1'][ind]
                                    if ( len(excel_file.df_template_dataFacts[where1]) > 0):
                                        df_1 = excel_file.df_template_dataFacts[where1]
                                        df_1['name'] = excel_file.df_template_modification['FactName_1 (Later Date/Larger Number)'][ind]
                                        df_1['type'] = excel_file.df_template_modification['type'][ind]
                                        df_1['displayInputUnit'] =excel_file.df_template_modification['displayInputUnit'][ind]
                                        df_1['dataFactSourceId'] =excel_file.df_template_modification['dataFactSourceId'][ind]
                                        df_1['entity'] = excel_file.df_template_modification['entity'][ind]
                                        df_1['expression'] = ''
                                        where1 = excel_file.df_template_dataFacts['id'].str.lower().isin( df_1['id'].str.lower().values.tolist())
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts[~where1], df_1], ignore_index=True) 
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts[~where1].append(df_1, ignore_index=False)
                                    else:
                                        #-- update datafacts with template value based on FactID_1
                                        where1 =  excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['FactID_1'][ind]
                                        where1 =  excel_file.df_template_dataFacts['entity'] == excel_file.df_template_modification['entity'][ind]
                                        df_1 = excel_file.df_template_dataFacts[where1 & where2]
                                        df_1['name'] = excel_file.df_template_modification['FactName_1 (Later Date/Larger Number)'][ind]
                                        df_1['type'] = excel_file.df_template_modification['type'][ind]
                                        df_1['displayInputUnit'] =excel_file.df_template_modification['displayInputUnit'][ind]
                                        df_1['dataFactSourceId'] =excel_file.df_template_modification['dataFactSourceId'][ind]
                                        df_1['entity'] = excel_file.df_template_modification['entity'][ind]
                                        df_1['expression'] = ''
                                        where1 = excel_file.df_template_dataFacts['id'].str.lower().isin( df_1['id'].str.lower().values.tolist())
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts[~where1], df_1], ignore_index=True) 
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts[~where1].append(df_1, ignore_index=False)
                                #-- FactName_2 (Earlier Date/Smaller Number) change
                                if (excel_file.df_template_modification['FactName_2 (Earlier Date/Smaller Number)'][ind] != ''):
                                    where1 =  excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['FactID_2'][ind]                        
                                    if ( len(excel_file.df_template_dataFacts[where1]) > 0):
                                        df_1 = excel_file.df_template_dataFacts[where1]
                                        df_1['name'] = excel_file.df_template_modification['FactName_2 (Earlier Date/Smaller Number)'][ind]
                                        df_1['type'] = excel_file.df_template_modification['type'][ind]
                                        df_1['displayInputUnit'] =excel_file.df_template_modification['displayInputUnit'][ind]
                                        df_1['dataFactSourceId'] =excel_file.df_template_modification['dataFactSourceId'][ind]
                                        df_1['entity'] = excel_file.df_template_modification['entity'][ind]
                                        df_1['expression'] = ''
                                        where1 = excel_file.df_template_dataFacts['id'].str.lower().isin( df_1['id'].str.lower().values.tolist())
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts[~where1], df_1], ignore_index=True) 
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts[~where1].append(df_1, ignore_index=False)
                                    else:
                                        #-- update datafacts with template value based on FactID_1
                                        where1 =  excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['FactID_2'][ind]
                                        where1 =  excel_file.df_template_dataFacts['entity'] == excel_file.df_template_modification['entity'][ind]
                                        df_1 = excel_file.df_template_dataFacts[where1 & where2]
                                        df_1['name'] = excel_file.df_template_modification['FactName_2 (Earlier Date/Smaller Number)'][ind]
                                        df_1['type'] = excel_file.df_template_modification['type'][ind]
                                        df_1['displayInputUnit'] =excel_file.df_template_modification['displayInputUnit'][ind]
                                        df_1['dataFactSourceId'] =excel_file.df_template_modification['dataFactSourceId'][ind]
                                        df_1['entity'] = excel_file.df_template_modification['entity'][ind]
                                        df_1['expression'] = ''
                                        where1 = excel_file.df_template_dataFacts['id'].str.lower().isin( df_1['id'].str.lower().values.tolist())
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts[~where1], df_1], ignore_index=True) 
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts[~where1].append(df_1, ignore_index=False)

                                #-- update expression, calculation, also template datafacts
                                if (excel_file.df_template_modification['FactID_1'][ind] != '' and excel_file.df_template_modification['FactID_2'][ind] != ''): 
                                    excel_file.df_template_modification['expression'][ind] = excel_file.df_template_modification['FactID_1'][ind] + "-" + excel_file.df_template_modification['FactID_2'][ind]
                                    where1= excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['calculation'][ind]
                                    df_1 = excel_file.df_template_dataFacts[where1]
                                    df_1['type'] = excel_file.df_template_modification['type'][ind]
                                    df_1['displayInputUnit'] =excel_file.df_template_modification['displayInputUnit'][ind]
                                    df_1['entity'] = excel_file.df_template_modification['entity'][ind]
                                    df_1['expression'] = excel_file.df_template_modification['expression'][ind]
                                    where1 = excel_file.df_template_dataFacts['id'].str.lower().isin( df_1['id'].str.lower().values.tolist())
                                    excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts[~where1], df_1], ignore_index=True) 
                                    #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts[~where1].append(df_1, ignore_index=False)

                                    excel_file.df_template_modification['dataFacts'][ind] = excel_file.df_template_modification['FactID_1'][ind] + "," + excel_file.df_template_modification['FactID_2'][ind] + "," + excel_file.df_template_modification['calculation'][ind]
                                        
                                #-- aspect change - non calculate
                                if (excel_file.df_template_modification['FactID_1'][ind] == '' and excel_file.df_template_modification['FactID_2'][ind] == ''): 
                                    #-- if this datafact has more than 1 aspect in template
                                    where1 = excel_file.df_template['dataFacts'] == excel_file.df_template_modification['dataFacts'][ind]
                                    where2 = excel_file.df_template['aspect'] == excel_file.df_template_modification['aspect'][ind]
                                    #--st.markdown(excel_file.df_template[where1 & ~where2].to_html(), unsafe_allow_html=True)
                                    if ( len(excel_file.df_template[where1 & ~where2]['aspect'].unique()) > 0):
                                        #-- this datafact has been used for another aspect, create a new datafact
                                        if (len(excel_file.df_template_modification['aspect'][ind]) > 30):
                                            excel_file.df_template_modification['dataFacts'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[:15] + "_" + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[30:15] + "_" + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[-15]
                                        else:
                                            excel_file.df_template_modification['dataFacts'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')
                                                                
                                        #-- need to check if differencet id for same name
                                        n = 0
                                        while (excel_file.df_template_modification['dataFacts'][ind].lower() in excel_file.df_template_dataFacts['id'].str.lower().values.tolist()):
                                            n = n + 1
                                            excel_file.df_template_modification['dataFacts'][ind] = excel_file.df_template_modification['dataFacts'][ind] + "_" + str(n)
                                            if n == 6:
                                                break     
                                        
                                        # remove extra space
                                        excel_file.df_template_modification['dataFacts'][ind] = excel_file.df_template_modification['dataFacts'][ind].strip()

                                        #-- add this new id to datafact
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_modification['dataFacts'][ind]], 'name': [excel_file.df_template_modification['aspect'][ind]], 'type': [excel_file.df_template_modification['inputComponent'][ind]], 'displayInputUnit': [excel_file.df_template_modification['displayInputUnit'][ind]], 'dataFactSourceId': [excel_file.df_template_modification['dataFactSourceId'][ind]], 'entity': [excel_file.df_template_modification['entity'][ind]], 'expression': [excel_file.df_template_modification['expression'][ind]], 'unique_index': [unique_index+1]})
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts, df_tmp], ignore_index=True)
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append({'id': excel_file.df_template_modification['dataFacts'][ind], 'name': excel_file.df_template_modification['aspect'][ind], 'type': excel_file.df_template_modification['inputComponent'][ind], 'displayInputUnit': excel_file.df_template_modification['displayInputUnit'][ind], 'dataFactSourceId': excel_file.df_template_modification['dataFactSourceId'][ind], 'entity': excel_file.df_template_modification['entity'][ind], 'expression': excel_file.df_template_modification['expression'][ind], 'unique_index': unique_index+1},ignore_index=True)
                                        #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append(df_1, ignore_index=False)
                                        excel_file.df_template_dataFacts.drop_duplicates()

                                        #-- update aspectId to reflect changes
                                        excel_file.df_template_modification['aspectId'][ind] = excel_file.df_template_modification['sectionId'][ind] + "." + excel_file.df_template_modification['topic'][ind] + "." + excel_file.df_template_modification['dataFacts'][ind] 
                                        excel_file.df_template_modification['id'][ind] = excel_file.df_template_modification['aspectId'][ind]
                                        #--st.markdown(excel_file.df_template_modification.to_html(), unsafe_allow_html=True)
                                    else:
                                        # this is the only datafact in template
                                        where1 =  excel_file.df_template_dataFacts['id'] == excel_file.df_template_modification['dataFacts'][ind]
                                        # -- remove this for US where2 = excel_file.df_template_dataFacts['entity'] == excel_file.df_template_modification['entity'][ind]
                                        if ( len(excel_file.df_template_dataFacts[where1]) > 0):
                                            excel_file.df_template_dataFacts =  excel_file.df_template_dataFacts[~where1]
                                            df_tmp = pd.DataFrame({'id': [excel_file.df_template_modification['dataFacts'][ind]], 'name': [excel_file.df_template_modification['aspect'][ind]], 'type':[excel_file.df_template_modification['inputComponent'][ind]], 'displayInputUnit': [excel_file.df_template_modification['displayInputUnit'][ind]], 'dataFactSourceId': [excel_file.df_template_modification['dataFactSourceId'][ind]], 'entity': [excel_file.df_template_modification['entity'][ind]], 'expression':[excel_file.df_template_modification['expression'][ind]], 'unique_index': [unique_index+1]})
                                            excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts, df_tmp], ignore_index=True)
                                            #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append({'id': excel_file.df_template_modification['dataFacts'][ind], 'name': excel_file.df_template_modification['aspect'][ind], 'type': excel_file.df_template_modification['inputComponent'][ind], 'displayInputUnit': excel_file.df_template_modification['displayInputUnit'][ind], 'dataFactSourceId': excel_file.df_template_modification['dataFactSourceId'][ind], 'entity': excel_file.df_template_modification['entity'][ind], 'expression': excel_file.df_template_modification['expression'][ind], 'unique_index': unique_index+1},ignore_index=True)
                                        else:
                                            #-- create new id  
                                            if (len(excel_file.df_template_modification['aspect'][ind]) > 30):
                                                excel_file.df_template_modification['dataFacts'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[:15] + "_" + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[30:15] + "_" + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')[-15]
                                            else:
                                                excel_file.df_template_modification['dataFacts'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_modification['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')
                                                                    
                                            #-- need to check if differencet id for same name
                                            n = 0
                                            while (excel_file.df_template_modification['dataFacts'][ind].lower() in excel_file.df_template_dataFacts['id'].str.lower().values.tolist()):
                                                n = n + 1
                                                excel_file.df_template_modification['dataFacts'][ind] = excel_file.df_template_modification['dataFacts'][ind] + "_" + str(n)
                                                if n == 6:
                                                    break  
                                                                        
                                            #-- add this new id to datafacts
                                            df_tmp = pd.DataFrame({'id': [excel_file.df_template_modification['dataFacts'][ind]], 'name': [excel_file.df_template_modification['aspect'][ind]], 'type': [excel_file.df_template_modification['inputComponent'][ind]], 'displayInputUnit': [excel_file.df_template_modification['displayInputUnit'][ind]], 'dataFactSourceId': [excel_file.df_template_modification['dataFactSourceId'][ind]], 'entity': [excel_file.df_template_modification['entity'][ind]], 'expression': [excel_file.df_template_modification['expression'][ind]], 'unique_index': [unique_index+1]})
                                            excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts, df_tmp], ignore_index=True)
                                            #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append({'id': excel_file.df_template_modification['dataFacts'][ind], 'name': excel_file.df_template_modification['aspect'][ind], 'type': excel_file.df_template_modification['inputComponent'][ind], 'displayInputUnit': excel_file.df_template_modification['displayInputUnit'][ind], 'dataFactSourceId': excel_file.df_template_modification['dataFactSourceId'][ind], 'entity': excel_file.df_template_modification['entity'][ind], 'expression': excel_file.df_template_modification['expression'][ind], 'unique_index': unique_index+1},ignore_index=True)
                                            #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append(df_1, ignore_index=False)
                                            excel_file.df_template_dataFacts.drop_duplicates()

                                            #-- update aspectId to reflect changes
                                            excel_file.df_template_modification['aspectId'][ind] = excel_file.df_template_modification['sectionId'][ind] + "." + excel_file.df_template_modification['topic'][ind] + "." + excel_file.df_template_modification['dataFacts'][ind] 
                                            excel_file.df_template_modification['id'][ind] = excel_file.df_template_modification['aspectId'][ind]

                                #-- update audit config details
                                where1 = excel_file.df_template_auditConfigurationDetails['aspectId'] == tmp_id
                                where2 = excel_file.df_template_auditConfigurationDetails['business'] == excel_file.df_template_modification['business'][ind]                     
                                excel_file.df_template_auditConfigurationDetails =  excel_file.df_template_auditConfigurationDetails[~(where1 & where2)]
                                
                                #--st.markdown(excel_file.df_template_modification.to_html(), unsafe_allow_html=True)
                                df_tmp = pd.DataFrame({'location': [excel_file.df_template_modification['location'][ind]], 'business': [excel_file.df_template_modification['business'][ind]], 
                                                        'auditType': [excel_file.df_template_modification['auditType'][ind]], 'riskPointsSection': [excel_file.df_template_modification['riskPointsSection'][ind]], 
                                                        'riskPointsTopic': [excel_file.df_template_modification['riskPointsTopic'][ind]],'riskPointsTest':[excel_file.df_template_modification['riskPointsTest'][ind]],
                                                        'capId': [excel_file.df_template_modification['capId'][ind]], 'riskProfileId': [excel_file.df_template_modification['riskProfileId'][ind]], 
                                                        'milestoneConfigurationProfileId': [excel_file.df_template_modification['milestoneConfigurationProfileId'][ind]],
                                                        'userRoleConfigurationProfileId': [excel_file.df_template_modification['userRoleConfigurationProfileId'][ind]],
                                                        'reviewErrorProfileId': [excel_file.df_template_modification['reviewErrorProfileId'][ind]],'aspectId': [excel_file.df_template_modification['aspectId'][ind]],
                                                        'displayOrder': [excel_file.df_template_modification['displayOrder'][ind]], 
                                                        'correctiveActionsSLAExclusionsProfileId': [excel_file.df_template_modification['correctiveActionsSLAExclusionsProfileId'][ind]], 
                                                        'breachOfContractMilestoneConfigurationProfileId': [excel_file.df_template_modification['breachOfContractMilestoneConfigurationProfileId'][ind]],
                                                        'scoringMethodologyId': [excel_file.df_template_modification['scoringMethodologyId'][ind]],
                                                        'displayOrder':["{:03d}".format(excel_file.df_template_modification['topic_displayOrder'][ind]) + "{:03d}".format(excel_file.df_template_modification['test_displayOrder'][ind]) + "{:03d}".format(excel_file.df_template_modification['aspect_displayOrder'][ind])], 
                                                        'unique_index': [unique_index+1]})     
                                df_tmp['displayOrder'] = df_tmp['displayOrder'].astype(int)                                  
                                excel_file.df_template_auditConfigurationDetails = pd.concat([excel_file.df_template_auditConfigurationDetails, df_tmp ], ignore_index=True)
                                #-- excel_file.df_template_auditConfigurationDetails = excel_file.df_template_auditConfigurationDetails.append(excel_file.df_template_modification.loc[ind][excel_file.auditConfigurationDetails_column_list], ignore_index=True)                    
                            
                                #-- update audit rules
                                where1 = excel_file.df_template_auditRules['id'] == tmp_id
                                
                                excel_file.df_template_auditRules = excel_file.df_template_auditRules[~where1]
                                df_tmp = pd.DataFrame({'sectionId': [excel_file.df_template_modification['sectionId'][ind]], 'section': [excel_file.df_template_modification['section'][ind]], 'controlId': [excel_file.df_template_modification['controlId'][ind]],
                                                        'control': [excel_file.df_template_modification['control'][ind]],'topic': [excel_file.df_template_modification['topic'][ind]],'testId': [excel_file.df_template_modification['testId'][ind]], 
                                                        'test': [excel_file.df_template_modification['test'][ind]],'id': [excel_file.df_template_modification['aspectId'][ind]],'aspect': [excel_file.df_template_modification['aspect'][ind]],'dataFacts': [excel_file.df_template_modification['dataFacts'][ind]],'calculation':[excel_file.df_template_modification['calculation'][ind]],'operator': [excel_file.df_template_modification['operator'][ind]],'value': [excel_file.df_template_modification['value'][ind]],'dateValueUnit': [excel_file.df_template_modification['dateValueUnit'][ind]],'inputComponent': [excel_file.df_template_modification['inputComponent'][ind]],'inputFormatValues': [excel_file.df_template_modification['inputFormatValues'][ind]],'valueforNotApplicable': [excel_file.df_template_modification['valueforNotApplicable'][ind]], 
                                                        'aspectStatusForTestNotApplicable': [excel_file.df_template_modification['aspectStatusForTestNotApplicable'][ind]], 
                                                        'parentAspectStatusforDisablingDependents': [excel_file.df_template_modification['parentAspectStatusforDisablingDependents'][ind]],
                                                        'aspectStatusForTestPass': [excel_file.df_template_modification['aspectStatusForTestPass'][ind]], 
                                                        #-- 'scoringMethodologyId':[excel_file.df_template_modification['scoringMethodologyId'][ind]], 
                                                        'auditFindingForPassTemplate':[excel_file.df_template_modification['auditFindingForPassTemplate'][ind]], 
                                                        'auditFindingTemplate':[excel_file.df_template_modification['auditFindingTemplate'][ind]], 
                                                        'correctiveActionTemplate':[excel_file.df_template_modification['correctiveActionTemplate'][ind]], 
                                                        'dependentTestAspects':[excel_file.df_template_modification['dependentTestAspects'][ind]], 
                                                        'unique_index': [excel_file.df_template_modification['unique_index'][ind]]})
                                
                                excel_file.df_template_auditRules = pd.concat([excel_file.df_template_auditRules, df_tmp ], ignore_index=True)


                    #-- add new if there any 
                    if len(excel_file.df_template_new) > 0:
                        castr_rule_definder.location = excel_file.df_template_new['location'].unique()
                        
                        #-- datafactsource
                        unique_index = 9999
                        # iterate through each row and select
                        for ind in excel_file.df_template_new.index:
                            unique_index = unique_index + 1
                            # -- exclude holiday list
                            if (excel_file.df_template_new['location'][ind] not in excel_file.holiday_location_list):
                                castr_rule_definder.rule_id_prefix(excel_file.df_template_new['business'][ind])

                                #-- datafact source id for datafact1
                                if (excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind].strip() != ''):
                                    #-- if excel_file.df_template_new['FactName_1_Document'][ind].lower() == 'paystub':
                                    #--     tem = "333"

                                    df_tmp = excel_file.FindDataFactSourceByName(excel_file.df_template_new['FactName_1_Document'][ind], "", excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['dataFactSourceId_1'][ind] = df_tmp['id'].values[0]
                                    else:
                                        excel_file.df_template_new['dataFactSourceId_1'][ind] =  excel_file.CreateDataFactSourceId(excel_file.df_template_new['FactName_1_Document'][ind], excel_file.df_template_dataFactSources)

                                        #-- add this new id to datafactsource
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['dataFactSourceId_1'][ind]], 'name': [excel_file.df_template_new['FactName_1_Document'][ind]], 'unique_index':[unique_index]})     
                                        excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources, df_tmp], ignore_index=True)
                                        excel_file.df_template_dataFactSources.drop_duplicates(subset=['id','name'],inplace=True)

                                #-- datafact source id for datafact2
                                if (excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind].strip() != ''):

                                    df_tmp = excel_file.FindDataFactSourceByName(excel_file.df_template_new['FactName_2_Document'][ind], "", excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['dataFactSourceId_2'][ind] = df_tmp['id'].values[0]
                                    else:
                                        excel_file.df_template_new['dataFactSourceId_2'][ind] =  excel_file.CreateDataFactSourceId(excel_file.df_template_new['FactName_2_Document'][ind], excel_file.df_template_dataFactSources)

                                        #-- add this new id to datafactsource
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['dataFactSourceId_2'][ind]], 'name': [excel_file.df_template_new['FactName_2_Document'][ind]], 'unique_index':[unique_index]})     
                                        excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources, df_tmp], ignore_index=True)
                                        excel_file.df_template_dataFactSources.drop_duplicates(subset=['id','name'],inplace=True)

                                #-- create datafact source id for calculation/expression besides source1 and source2
                                if (excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind].strip() != ''): 
                                    #-- create a datafactsource for calculate test aspect
                                    df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['location'][ind] + '_Calculated'], 'name': ['Calculated'], 'unique_index':[unique_index]})   
                                    excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources, df_tmp], ignore_index=True)                                            
                                    excel_file.df_template_dataFactSources.drop_duplicates(subset=['id','name'],inplace=True)
                                    excel_file.df_template_new['dataFactSourceId'][ind] = excel_file.df_template_new['location'][ind] + '_Calculated'

                                #-- create datafact source id for non calculate test aspect
                                if (excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind].strip() == '' and excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind].strip() == ''):
                                    
                                    df_tmp = excel_file.FindDataFactSourceByName(excel_file.df_template_new['document'][ind], "", excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['dataFactSourceId'][ind] = df_tmp['id'].values[0]
                                    else: 
                                        excel_file.df_template_new['dataFactSourceId'][ind] =  excel_file.CreateDataFactSourceId(excel_file.df_template_new['document'][ind], excel_file.df_template_dataFactSources)

                                        #-- add this new id to datafactsource
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['dataFactSourceId'][ind]], 'name': [excel_file.df_template_new['document'][ind]], 'unique_index':[unique_index]})     
                                        excel_file.df_template_dataFactSources = pd.concat([excel_file.df_template_dataFactSources, df_tmp], ignore_index=True)
                                        excel_file.df_template_dataFactSources.drop_duplicates(subset=['id','name'],inplace=True)

                                #-- datafact1
                                if (excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind].strip() != ''):
                                    df_tmp = excel_file.FindDataFactByNameTypeEntityDocument(excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind], excel_file.df_template_new['FactName_1_inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_new['FactName_1_Document'][ind], "", excel_file.df_template_dataFacts, excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['FactID_1'][ind] = df_tmp['id'].values[0]
                                    else :
                                        excel_file.df_template_new['FactID_1'][ind] = excel_file.CreateDataFactId(excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind], excel_file.df_template_new['FactName_1_inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_dataFacts)
                            
                                        #-- add datafacts with datafact1 
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['FactID_1'][ind]], 'name': [excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind]], 'type': [excel_file.df_template_new['FactName_1_inputComponent'][ind]], 'displayInputUnit':[excel_file.df_template_new['displayInputUnit'][ind]], 'dataFactSourceId':[excel_file.df_template_new['dataFactSourceId_1'][ind]],'entity':[excel_file.df_template_new['entity'][ind]], 'expression':[''],'unique_index': [unique_index]})
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts,df_tmp], ignore_index=True)
                                        excel_file.df_template_dataFacts.drop_duplicates()

                                #-- datafact2
                                if (excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind].strip() != ''):

                                    df_tmp = excel_file.FindDataFactByNameTypeEntityDocument(excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind], excel_file.df_template_new['FactName_2_inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_new['FactName_2_Document'][ind], "", excel_file.df_template_dataFacts,excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['FactID_2'][ind] = df_tmp['id'].values[0]
                                    else :
                                        excel_file.df_template_new['FactID_2'][ind] = excel_file.CreateDataFactId(excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind], excel_file.df_template_new['FactName_2_inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_dataFacts)
                            
                                        #-- add datafacts with datafact2 
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['FactID_2'][ind]], 'name': [excel_file.df_template_new['FactName_2 (Earlier Date/Smaller Number)'][ind]], 'type': [excel_file.df_template_new['FactName_2_inputComponent'][ind]], 'displayInputUnit':[excel_file.df_template_new['displayInputUnit'][ind]], 'dataFactSourceId':[excel_file.df_template_new['dataFactSourceId_2'][ind]],'entity':[excel_file.df_template_new['entity'][ind]], 'expression':[''],'unique_index': [unique_index]})
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts,df_tmp], ignore_index=True)
                                        excel_file.df_template_dataFacts.drop_duplicates()

                                #-- create datafact for calculation besides fact1 and fact2
                                if (excel_file.df_template_new['FactName_1 (Later Date/Larger Number)'][ind].strip() != ''):
                                    #-- expression
                                    excel_file.df_template_new['expression'][ind] = excel_file.df_template_new['FactID_1'][ind] + "-" + excel_file.df_template_new['FactID_2'][ind]
                                    
                                    # check if this expression exists
                                    where1 =  excel_file.df_template_dataFacts['expression'] == excel_file.df_template_new['expression'][ind]                                            
                                    if ( len(excel_file.df_template_dataFacts[where1]) > 0):
                                        #-- existing expression
                                        excel_file.df_template_new['calculation'][ind] = excel_file.df_template_dataFacts[where1]['id'].iloc[0]
                                        excel_file.df_template_new['dataFacts'][ind] = excel_file.df_template_new['FactID_1'][ind] + "," + excel_file.df_template_new['FactID_2'][ind] + "," + excel_file.df_template_new['calculation'][ind] 
                                        
                                    else:
                                        #-- create a new calculation for the expression  
                                        excel_file.df_template_new['calculation'][ind] = castr_rule_definder.ruleIdPrefix + excel_file.df_template_new['aspect'][ind].replace(' ', "_").replace('"', '').replace(',', '')
                                        if (len(excel_file.df_template_new['calculation'][ind]) > 30):
                                            excel_file.df_template_new['calculation'][ind] = excel_file.df_template_new['calculation'][ind][:15] + "_" + excel_file.df_template_new['calculation'][ind][20:15]

                                        #-- make sure this new id is unique
                                        n = 0
                                        tmp_id = excel_file.df_template_new['calculation'][ind]
                                        while (tmp_id.lower() in excel_file.df_template_dataFacts['id'].str.lower().values.tolist()):
                                            n = n + 1
                                            tmp_id = excel_file.df_template_new['calculation'][ind] + "_" + str(n)

                                        excel_file.df_template_new['calculation'][ind] = tmp_id
                                        excel_file.df_template_new['dataFactName'][ind] = excel_file.df_template_new['aspect'][ind]
                                        excel_file.df_template_new['dataFacts'][ind] = excel_file.df_template_new['FactID_1'][ind] + "," + excel_file.df_template_new['FactID_2'][ind] + "," + excel_file.df_template_new['calculation'][ind]                                   

                                        #-- add this new calculation id to datafacts
                                        df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['calculation'][ind]], 'name': [excel_file.df_template_new['dataFactName'][ind]], 'type':[excel_file.df_template_new['inputComponent'][ind]], 'displayInputUnit':[excel_file.df_template_new['dateValueUnit'][ind]], 'dataFactSourceId':[excel_file.df_template_new['location'][ind] + "_Calculated"],'entity':[excel_file.df_template_new['entity'][ind]], 'expression':[excel_file.df_template_new['expression'][ind]],'unique_index': [unique_index+1]})
                                        excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts, df_tmp],ignore_index=True)                                            
                                        excel_file.df_template_dataFacts.drop_duplicates(subset=['id','name','type'], inplace=True)

                                else:
                                    #-- non calculate test aspect    
                                    df_tmp = excel_file.FindDataFactByNameTypeEntityDocument(excel_file.df_template_new['aspect'][ind], excel_file.df_template_new['inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_new['document'][ind], "", excel_file.df_template_dataFacts,excel_file.df_template_dataFactSources)
                                    if len(df_tmp) > 0 :
                                        excel_file.df_template_new['dataFacts'][ind] = df_tmp['id'].values[0]
                                    else :
                                        excel_file.df_template_new['dataFacts'][ind] = excel_file.CreateDataFactId(excel_file.df_template_new['aspect'][ind], excel_file.df_template_new['inputComponent'][ind], excel_file.df_template_new['entity'][ind], excel_file.df_template_dataFacts)
                            
                                    # type
                                    excel_file.df_template_new['type'][ind] = excel_file.df_template_new['inputComponent'][ind]                                           

                                    excel_file.df_template_new['dataFactName'][ind] = excel_file.df_template_new['aspect'][ind]

                                    #-- displayInputUnit
                                    if excel_file.df_template_new['inputComponent'][ind] == "Number":
                                        excel_file.df_template_new['displayInputUnit'][ind] = excel_file.df_template_new['inputFormatValues'][ind]
                                    

                                    #-- add this new id to datafacts
                                    df_tmp = pd.DataFrame({'id': [excel_file.df_template_new['dataFacts'][ind]], 'name': [excel_file.df_template_new['dataFactName'][ind]], 'type':[excel_file.df_template_new['inputComponent'][ind]], 'displayInputUnit':[excel_file.df_template_new['displayInputUnit'][ind]], 'dataFactSourceId':[excel_file.df_template_new['dataFactSourceId'][ind]],'entity':[excel_file.df_template_new['entity'][ind]], 'expression':[''],'unique_index': [unique_index+1]})
                                    excel_file.df_template_dataFacts = pd.concat([excel_file.df_template_dataFacts, df_tmp], ignore_index=True)
                                    #-- excel_file.df_template_dataFacts = excel_file.df_template_dataFacts.append({'id': excel_file.df_template_new['dataFacts'][ind], 'name': excel_file.df_template_new['dataFactName'][ind], 'type':excel_file.df_template_new['inputComponent'][ind], 'displayInputUnit':excel_file.df_template_new['displayInputUnit'][ind], 'dataFactSourceId':excel_file.df_template_new['dataFactSourceId'][ind],'entity':excel_file.df_template_new['entity'][ind], 'expression':'','unique_index': unique_index+1},ignore_index=True)
                                    excel_file.df_template_dataFacts.drop_duplicates(subset=['id','name','type'], inplace=True)

                                #-- aspectId
                                excel_file.df_template_new['aspectId'][ind] = excel_file.df_template_new['sectionId'][ind] + "." + excel_file.df_template_new['topic'][ind].replace(' ', "_").replace('"', '').replace(',', '') + "." + excel_file.df_template_new['dataFacts'][ind]
                                excel_file.df_template_new['id'][ind] = excel_file.df_template_new['aspectId'][ind]

                                #-- need to check if differencet id for same document
                                n = 0
                                while (excel_file.df_template_new['aspectId'][ind] in excel_file.df_template_auditRules['id'].str.lower().values.tolist()):
                                    n = n + 1
                                    excel_file.df_template_new['aspectId'][ind] = excel_file.df_template_new['aspectId'][ind] + "_" + n


                                #-- add this new id to auditrules
                                df_tmp = pd.DataFrame({'sectionId': [excel_file.df_template_new['sectionId'][ind]], 'section': [excel_file.df_template_new['section'][ind]], 
                                                    'controlId': [excel_file.df_template_new['controlId'][ind]],'control': [excel_file.df_template_new['control'][ind]],
                                                    'topic': [excel_file.df_template_new['topic'][ind]],'testId': [excel_file.df_template_new['testId'][ind]],'test': [excel_file.df_template_new['test'][ind]],
                                                    'id': [excel_file.df_template_new['aspectId'][ind]],'aspect': [excel_file.df_template_new['aspect'][ind]],'dataFacts': [excel_file.df_template_new['dataFacts'][ind]],
                                                    'calculation':[excel_file.df_template_new['calculation'][ind]],'operator': [excel_file.df_template_new['operator'][ind]],
                                                    'value': [excel_file.df_template_new['value'][ind]],'dateValueUnit': [excel_file.df_template_new['dateValueUnit'][ind]],
                                                    'inputComponent': [excel_file.df_template_new['inputComponent'][ind]],'inputFormatValues': [excel_file.df_template_new['inputFormatValues'][ind]],
                                                    'valueforNotApplicable': [excel_file.df_template_new['valueforNotApplicable'][ind]],
                                                    'aspectStatusForTestNotApplicable': [excel_file.df_template_new['aspectStatusForTestNotApplicable'][ind]],
                                                    'parentAspectStatusforDisablingDependents': [excel_file.df_template_new['parentAspectStatusforDisablingDependents'][ind]],
                                                    'aspectStatusForTestPass': [excel_file.df_template_new['aspectStatusForTestPass'][ind]], 
                                                    'auditFindingForPassTemplate':[excel_file.df_template_new['auditFindingForPassTemplate'][ind]], 
                                                    'auditFindingTemplate':[excel_file.df_template_new['auditFindingTemplate'][ind]], 
                                                    'correctiveActionTemplate':[excel_file.df_template_new['correctiveActionTemplate'][ind]], 
                                                    'dependentTestAspects':[excel_file.df_template_new['dependentTestAspects'][ind]], 
                                                    'unique_index': [excel_file.df_template_new['unique_index'][ind]]})
                                excel_file.df_template_auditRules =  pd.concat([excel_file.df_template_auditRules, df_tmp], ignore_index=True)
                                excel_file.df_template_auditRules.drop_duplicates(subset=['id','topic','section'], inplace=True)

                                #--debugging
                                #-- excel_file.df_template_auditRules

                                #-- add this new id to audit configuration details
                                df_tmp = pd.DataFrame({'location': [excel_file.df_template_new['location'][ind]], 'business': [excel_file.df_template_new['business'][ind]], 'auditType': [excel_file.df_template_new['auditType'][ind]], 
                                                        'riskPointsSection': [excel_file.df_template_new['riskPointsSection'][ind]], 'riskPointsTopic': [excel_file.df_template_new['riskPointsTopic'][ind]],
                                                        'riskPointsTest':[excel_file.df_template_new['riskPointsTest'][ind]],'capId': [excel_file.df_template_new['capId'][ind]], 
                                                        'riskProfileId': [excel_file.df_template_new['riskProfileId'][ind]], 
                                                        'milestoneConfigurationProfileId': [excel_file.df_template_new['milestoneConfigurationProfileId'][ind]],
                                                        'userRoleConfigurationProfileId': [excel_file.df_template_new['userRoleConfigurationProfileId'][ind]],
                                                        'reviewErrorProfileId': [excel_file.df_template_new['reviewErrorProfileId'][ind]],'aspectId': [excel_file.df_template_new['aspectId'][ind]],
                                                        'displayOrder': [excel_file.df_template_new['displayOrder'][ind]], 
                                                        'correctiveActionsSLAExclusionsProfileId': [excel_file.df_template_new['correctiveActionsSLAExclusionsProfileId'][ind]], 
                                                        'breachOfContractMilestoneConfigurationProfileId': [excel_file.df_template_new['breachOfContractMilestoneConfigurationProfileId'][ind]], 
                                                        'tagConfigurationProfileId':[excel_file.df_template_new['tagConfigurationProfileId'][ind]], 
                                                        'scoringMethodologyId':[excel_file.df_template_new['scoringMethodologyId'][ind]], 
                                                        'displayOrder':["{:03d}".format(excel_file.df_template_new['topic_displayOrder'][ind]) + "{:03d}".format(excel_file.df_template_new['test_displayOrder'][ind]) + "{:03d}".format(excel_file.df_template_new['aspect_displayOrder'][ind])], 
                                                        'unique_index': [unique_index+1]})
                                
                                df_tmp['displayOrder'] = df_tmp['displayOrder'].astype(int)  
                                excel_file.df_template_auditConfigurationDetails = pd.concat([excel_file.df_template_auditConfigurationDetails, df_tmp], ignore_index=True)
                                excel_file.df_template_auditConfigurationDetails.drop_duplicates(subset=['aspectId','business'], inplace=True)
                                

                    #-------- this section does not needed if template file has topic order, test order and aspect order fixed            
                    
                    #-- df_topic_order = castr_rule_definder.createDisplayorder(excel_file.df_template_auditRules, 'topic',  excel_file.df_template_auditConfigurationDetails)                            
                    #-- df_test_order = castr_rule_definder.createDisplayorder(excel_file.df_template_auditRules, 'test',  excel_file.df_template_auditConfigurationDetails)                            
                    #-- df_aspect_order = castr_rule_definder.createDisplayorder(excel_file.df_template_auditRules, 'aspect',  excel_file.df_template_auditConfigurationDetails)
                
                    #-- tmp_auditRules = pd.merge( excel_file.df_template_auditRules, df_topic_order,how="left", left_on=['topic'], right_on='topic')
                    #-- tmp_auditRules.rename(columns={'displayOrder': 'topic_order'}, inplace=True)
                
                    #-- tmp_auditRules = pd.merge( tmp_auditRules, df_test_order,how="left", left_on=['test'], right_on='test')
                    #-- tmp_auditRules.rename(columns={'displayOrder': 'test_order'}, inplace=True)
                    #-- tmp_auditRules = pd.merge( tmp_auditRules, df_aspect_order,how="left", left_on=['aspect'], right_on='aspect')
                    #-- tmp_auditRules.rename(columns={'displayOrder': 'aspect_order'}, inplace=True)
                    #-- tmp_auditRules['order_created'] = tmp_auditRules['topic_order'] + tmp_auditRules['test_order'] + tmp_auditRules['aspect_order']
                    #-- tmp_auditRules['order_created'] = tmp_auditRules['order_created'].astype(int)                              
                    
                    #-- excel_file.df_template_auditConfigurationDetails = pd.merge( excel_file.df_template_auditConfigurationDetails, tmp_auditRules[['id','topic','test','aspect','order_created']] ,how="left", left_on=['aspectId'], right_on='id')
                    
                    #-- excel_file.df_template_auditConfigurationDetails['displayOrder'] = excel_file.df_template_auditConfigurationDetails['order_created']

                    #-- end of no need this section


                    # -- keep columns required by CASTR only
                    auditConfigDetails_column = [i for i in excel_file.df_SST_auditConfigurationDetails_Columns_list if i not in excel_file.auditConfigurationDetails_column_list]
                    excel_file.df_template_auditConfigurationDetails = excel_file.df_template_auditConfigurationDetails[excel_file.auditConfigurationDetails_column_list + auditConfigDetails_column]
                    
                    #-- debugging
                    #-- excel_file.auditConfigurationDetails_column_list

                    #merge new/modify/delete dataframe and build sheet template
                    df_merge = pd.concat([excel_file.df_template,excel_file.df_template_new ], ignore_index=False)
                    df_merge = pd.concat([df_merge,excel_file.df_template_modification ], ignore_index=False)
                    
                    #-- do a quality check before saving
                    #-- 1- required input data fields validation
                    bValid = False
                    if (template_data_error_checking(df_merge, 'business/aspect/displayOrder', NULL) == True):
                        if ( template_data_error_checking(df_merge,'inputFormatValues/inputComponent/value', NULL) == True):
                            if ( template_data_error_checking(df_merge,'dateValueUnit', NULL) == True):
                                if (template_data_error_checking(df_merge,'business/audittype/topic/test/testId', NULL) == True) :
                                    bValid = True
                    if ( bValid == True):
                        with st.spinner("Output configuration file is being built..."):  
                            #-- merge delete back to template
                            df_merge = pd.concat([df_merge,excel_file.df_template_delete ], ignore_index=False)
                            #-- df_merge = df_merge.append(excel_file.df_template_delete, ignore_index=False)
                            
                            gd_configuration_file =grid_builder(df_merge[excel_file.selfService_template_column_list], user_permit.permit, 500, fileCount) 

                            #-- if not os.path.isdir(root_folder.replace("[userid]", os.getlogin()) + "\\Configuration Files"):
                                #-- os.makedirs(root_folder.replace("[userid]", os.getlogin()) + "\\Configuration Files")

                            file_name = "Config_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"       
                            save_file_path_name = config_file_path + file_name
                            with st.spinner("WALLE is saving template file..."):                     
                                with pd.ExcelWriter(save_file_path_name) as writer:
                                        excel_file.df_template_auditRules.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "AuditRules", index = False)
                                        excel_file.df_template_dataFacts.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "DataFacts", index = False)
                                        excel_file.df_template_dataFactSources.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "DataFactSources", index = False)
                                        excel_file.df_template_auditConfigurationDetails.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)

                                        #merge new/modify/delete back to sheet template
                                        excel_file.df_template = pd.concat([excel_file.df_template, excel_file.df_template_new, excel_file.df_template_modification, excel_file.df_template_delete], ignore_index=False)
            
                                        excel_file.df_template.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "template", index = False)
                                        excel_file.df_template_new.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "template-new", index = False)
                                        excel_file.df_template_modification.drop(labels=['unique_index'], axis=1).to_excel(writer, sheet_name = "template-modify", index = False)
                                        worksheet = writer.sheets['template']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        worksheet = writer.sheets['template-new']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        worksheet = writer.sheets['template-modify']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        
                                        #-- build a checking summary report
                                        # datafactsources, x is new data while y is available in prod
                                        df_1 = pd.merge(excel_file.df_template_dataFactSources[['id', 'name']], excel_file.df_prod_dataFactSources[['id','name']], how="left", left_on=['id'], right_on=['id'])
                                        where1= df_1['name_x'] == df_1['name_y']
                                        df_check_dataFactSources = df_1[~where1]   
                                                                        
                                        # datafacts 
                                        df_1 = pd.merge(excel_file.df_template_dataFacts[excel_file.dataFacts_column_list], excel_file.df_prod_dataFacts[excel_file.dataFacts_column_list], how="left", left_on=['id'], right_on=['id'])  
                                        where1= df_1['name_x'] == df_1['name_y']                                     
                                        where2= df_1['type_x'] == df_1['type_y']
                                        where3= df_1['displayInputUnit_x'] == df_1['displayInputUnit_y']
                                        where4= df_1['dataFactSourceId_x'] == df_1['dataFactSourceId_y']
                                        where5= df_1['entity_x'] == df_1['entity_y']
                                        where6= df_1['expression_x'] == df_1['expression_y']
                                        df_check_dataFacts = df_1[~(where1 & where2 & where3 & where4 & where5 & where6)]
                                        # df_check_dataFacts = excel_file.df_template_dataFacts.drop(labels=['unique_index'], axis=1).sort_values(by=['id','name','type', 'entity']).reset_index(drop=True).compare(excel_file.df_prod_dataFacts.drop(labels=['unique_index'], axis=1).sort_values(by=['id','name','type', 'entity']).reset_index(drop=True)).reset_index(drop=True)
                                        # AuditRules
                                        df_1 = pd.merge(excel_file.df_template_auditRules.drop(labels=['unique_index'], axis=1), excel_file.df_prod_auditRules.drop(labels=['unique_index'], axis=1), how ="outer",indicator=True)  
                                        where1= df_1['_merge'] == 'both'  
                                        df_check_auditRules = df_1[~where1].sort_values(by=['id'])
                                        
                                        # auditConfigDetails
                                        df_1 = pd.merge(excel_file.df_template_auditConfigurationDetails.drop(labels=['unique_index'], axis=1), excel_file.df_prod_auditConfigurationDetails.drop(labels=['unique_index'], axis=1), how ="outer", left_on=['aspectId', 'business', 'auditType'], right_on=['aspectId', 'business', 'auditType'], indicator=True)  
                                        where1= df_1['_merge'] == 'both'  
                                        df_check_auditConfigDetails = df_1[~where1].sort_values(by=['aspectId', 'business', 'auditType'])


                                        # df_check_auditConfigDetails = excel_file.df_template_auditConfigurationDetails.drop(labels=['unique_index'], axis=1).sort_values(by=['aspectId', 'business', 'auditType']).reset_index(drop=True).compare(excel_file.df_prod_auditConfigurationDetails.drop(labels=['unique_index'], axis=1).sort_values(by=['aspectId', 'business', 'auditType']).reset_index(drop=True))

                                        df_check_auditRules.to_excel(writer, sheet_name = "Check_AuditRules")
                                        df_check_dataFacts.to_excel(writer, sheet_name = "Check_DataFacts")
                                        df_check_dataFactSources.to_excel(writer, sheet_name = "Check_DataFactSources")
                                        df_check_auditConfigDetails.to_excel(writer, sheet_name = "check_AuditConfigurationDetails")

                                        worksheet = writer.sheets['Check_AuditRules']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        worksheet = writer.sheets['Check_DataFacts']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        worksheet = writer.sheets['Check_DataFactSources']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()
                                        worksheet = writer.sheets['check_AuditConfigurationDetails']
                                        worksheet.set_column('A:A', 30)
                                        worksheet.hide()

                                        writer.close()

                                        info_widget("", "Configuration file " + save_file_path_name + " has been generated successfully from " + source_file,"success")
                                                                                        
                                        #-- with open(save_file_path_name, 'rb') as my_file:
                                            #-- download_button_str = st.download_button(label = 'Click me to download config file and save it to local computer', data = my_file, file_name = file_name, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      

            else:
                
                status_widget("", "WALLE Stopped - error found in source self service template file:  ","") 
                if  not st.session_state.gd_template:
                    info_widget("","tab " + self_service_template_file.template.value + " is missing from " + source_file, 'error')
                if not st.session_state.gd_template_dataFacts:
                    info_widget("","tab " + self_service_template_file.template_DataFacts.value + " is missing from " + source_file,'error')
                if not st.session_state.gd_template_dataFactSources:
                    info_widget("","tab " + self_service_template_file.template_DataFactSources.value + " is missing from " + source_file,'error')
                if not st.session_state.gd_template_auditRules:
                    info_widget("","tab " + self_service_template_file.template_AuditRules.value + " is missing from " + source_file,'error') 
    
    if fileCount == 0:
        info_widget("", "No file found in " + file_path_name,"success")

 #--  start to build conditiaonTests sheet       
elif user_selection_mode ==  selection_modes.add_conditional_test.value:

    fileCount = 0
    for each in os.listdir(config_file_path):
        fileCount = fileCount + 1
        status_widget("", "", str(fileCount) + ". Source input file: " + config_file_path + "\\" + each )
        resetUserSelection()
        
        source_file = config_file_path + "\\" + each
        if excel_file.load_file(source_file, create_configuration_file) == False:
            source_file = None
            
        bValid = False
        if source_file is not None:   
            #-- check if the Template/TAuditRules/DataFacts/DatafactSources/ConditionalTests are availalbe
            if st.session_state.gd_conditionalTests == False:
                info_widget("", "tab ConditionalTests is not found in Source input file: " + source_file , "error")
            if st.session_state.gd_dataFacts == False or st.session_state.gd_dataFactSources == False or st.session_state.gd_auditRules == False:
                info_widget("", "source input file: " + source_file + " is not in valid format", "error")
                            
            if st.session_state.gd_dataFacts and st.session_state.gd_dataFactSources and st.session_state.gd_auditRules and st.session_state.gd_conditionalTests:
                if ( len(excel_file.df_conditionTests)> 0):
                    #-- find id for child aspect
                    excel_file.df_conditionTests = pd.merge(excel_file.df_conditionTests, excel_file.df_auditRules[['id','test', 'aspect', ]], how="left", left_on=['dependentTest', 'dependentTestAspect'], right_on=['test','aspect'])
                    excel_file.df_conditionTests.drop(labels=['unique_index', 'dependentTestAspectId', 'aspect'], axis=1, inplace=True)
                    excel_file.df_conditionTests.rename(columns={'id': 'dependentTestAspectId'}, inplace=True)
                    excel_file.df_conditionTests['dependentTestAspectId'].fillna("", inplace=True)
                    
                    where1 = excel_file.df_conditionTests['dependentTestAspectId'] ==""
                                                
                    if len( excel_file.df_conditionTests[where1])  > 0 :
                        status_widget("", "WALLE Stopped - A dependentTest + dependentTestAspect from tab ConditionalTests is not found in tab AuditRules!","")
                        info_widget("", " ~~ " + error_fix_instr , "error")

                        gd_configuration_file =grid_builder(excel_file.df_conditionTests[where1], True, 500, fileCount) 

                        #-- save the file
                        with st.spinner("WALLE is saving the file..."):    
                            file_name = "error_" + each.replace(".xlsx", "") + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".xlsx"   
                            save_file_path_name = correction_file_path + file_name     
                            excel_file_save = excelFile()
                            excel_file_save.create_writer(save_file_path_name ) 
                            #-- excel_file.create_template_column_list()
                            
                            with excel_file_save.writer as writer:                      
                                (excel_file.df_conditionTests[where1]).to_excel(writer, sheet_name = "data", index = False)
                                
                                writer.close()
                                status_widget("","Above data has been saved in: " + save_file_path_name,"")

                    else: 
                        #find parent id
                        #--excel_file.df_conditionTests = pd.merge(excel_file.df_conditionTests, excel_file.df_auditRules[['id', 'topic', 'test', 'aspect', ]], how="left", left_on=['topic', 'test', 'parentTestAspect'], right_on=['topic', 'test','aspect'])
                        excel_file.df_conditionTests = pd.merge(excel_file.df_conditionTests, excel_file.df_auditRules[['id','test', 'aspect', ]], how="left", left_on=['parentTest', 'parentTestAspect'], right_on=['test', 'aspect'])

                        excel_file.df_conditionTests.drop(labels=['parentTestAspectId', 'aspect'], axis=1, inplace=True)
                        excel_file.df_conditionTests.rename(columns={'id': 'parentTestAspectId'}, inplace=True)

                        excel_file.df_conditionTests.fillna("", inplace=True)
                        where1 = excel_file.df_conditionTests['parentTestAspectId'] ==""
                        if len( excel_file.df_conditionTests[where1])  > 0 :
                            status_widget("", "WALLE Stopped - A parentTest + parentTestAspect from tab ConditionalTests is not found in tab AuditRules!","")
                            info_widget("", " ~~ " + error_fix_instr , "error")

                            gd_configuration_file =grid_builder(excel_file.df_conditionTests[where1], True, 500, fileCount) 
                        else:
                            # make a list of dependentTestAspectId
                            child_list = excel_file.df_conditionTests.groupby(['parentTestAspectId'])['dependentTestAspectId'].apply(lambda x: ', '.join(x))
                            
                            #update auditRules 
                            child_list = pd.merge(excel_file.df_auditRules, child_list, how="left", left_on=['id'], right_on=['parentTestAspectId'])
                            #-- child_list['dependentTestAspectId'].fillna('',inplace=True)
                            
                            child_list.drop(labels=['dependentTestAspects'], axis=1, inplace=True)
                            child_list.rename(columns={'dependentTestAspectId': 'dependentTestAspects'}, inplace=True)
                        
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
                                    (child_list.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditRules", index = False)
                                    #-- (excel_file.df_auditRules.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditRules", index = False)
                                    (excel_file.df_auditConfigurationDetails.drop(labels='unique_index', axis=1)).to_excel(writer, sheet_name = "AuditConfigurationDetails", index = False)
                                    excel_file.df_conditionTests.to_excel(writer, sheet_name = "ConditionalTests", index = False)
                                    writer.close()
                                    status_widget("","Above data has been saved in: " + save_file_path_name,"")
                else:     
                    info_widget("", "No condtion tests data found in " + config_file_path,"success")

    if fileCount == 0:
            info_widget("", "No file found in " + config_file_path,"success")
