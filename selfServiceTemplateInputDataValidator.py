def template_data_error_checking(df, items, compare_df):
    where_holiday = df['location'].isin(excel_file.holiday_location_list)
    where1 = df['ModifyDeleteNew'].str.lower() == 's'
    where2 = df['ModifyDeleteNew'].str.lower() == 'd'

    df_chk = df[~where_holiday][~where1 & ~where2]
       
    if  (items == 'AuditRulesChecking'):
        # section
        where1 = compare_df['section'].str.lower().isin(df_chk['section'].str.lower().values.tolist())
        df_2 = compare_df[~where1]
        if (len(df_2) > 0 ):
            status_widget("", "WALLE Stopped - Column section has new value which is not found in production file","")
            status_widget("", "", "If this is a wording issue, fix the error in source input file offline before using this tool.")
            return False
        # topic
        where1 = compare_df['topic'].str.lower().isin(df_chk['topic'].str.lower().values.tolist())
        df_2 = compare_df[~where1]
        if (len(df_2) > 0 ):
            status_widget("", "WALLE Stopped - Column topic has new value which is not found in production file","")
            status_widget("", "", "If this is a wording issue, fix the error in source input file offline before using this tool.")
            return False

        # control
        #-- where1 = compare_df['control'].str.lower().isin(df_chk['control'].str.lower().values.tolist())
        #-- df_2 = compare_df[~where1]
        #-- if (len(df_2) > 0 ):
        #--     status_widget("", "WALLE Stopped - New control is found","")
        #--     status_widget("", "", "If this is a wording issue, fix the error in source input file offline before using this tool.")
        #--     return False

        # aspect
        #-- where1 = compare_df['aspect'].str.lower().isin(df_chk['aspect'].str.lower().values.tolist())
        #-- df_2 = compare_df[~where1]
        #-- if (len(df_2) > 0 ):
        #--     status_widget("", "Data validation - - some aspect(s) are not match between existing Production config file and Template file, we need a confirmation","")
        #--     status_widget("", "", "If this is a wording issue, fix the error in source input file offline before using this tool.")
        #--     return False

    #-- elif (items == 'dateValueUnit'):

    #--     where1 = df_chk['FactName_1 (Later Date/Larger Number)'].str.contains('date|month|hour')
    #--     where2= df_chk['FactName_2 (Earlier Date/Smaller Number)'].str.contains('date|month|hour')
    #--     where3= df_chk['dateValueUnit'].isin(['months', 'days','hours', 'years'])
    #--     df_2 = df_chk[where1 & where2 & ~where3]
    #--     if (len(df_2)) > 0:
    #--         status_widget("", "WALLE Stopped - dateValueUnit value is missing in calculated row","")
    #--         status_widget("", "", "dateValueUnit should be 'months', 'days', 'hours. Fix the error in source input file offline before using this tool.")
    #--         return False
    
    elif items == "riskPointsTest/scoringMethodologyId":
        where1 = df_chk['scoringMethodologyId'].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column scoringMethodologyId has blank value", "") 
            info_widget("", " ~~ " + castr_rule_scoringMethodology  +  "  " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False
        where1 = df_chk['riskPointsTest'].astype(str).str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column riskPointsTest has blank value", "") 
            info_widget("", " ~~ " + castr_rule_scoringMethodology  +  "  " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False

    elif items == "operator":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_operator  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False  
        
    elif items == "entity":
        where1 = df_chk[items].str.strip() == ""
        where2 = df_chk[items].str.strip() == "Employee"
        where3 = df_chk[items].str.strip() == "Carrier"
        df_1 = df_chk[where1 |(~where2 & ~where3) ]

        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has either blank or invalid value", "") 
            info_widget("", " ~~ " + castr_rule_entity  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False  
            
    elif items == "capId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_capId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False  
    elif items == "riskProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_riskProfileId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            yesno = st.radio("Please answer the question to continue. Do you have this feature enabled in your region?", YesNo_actions, 0)
            if yesno == yes_action:            
                id = st.text_input('riskProfileId', 'type your id here')
                if id.strip() == 'type your id here' or id.strip() == "":
                    status_widget("", "WALLE Stopped - you must provide a valid riskProfileId", "") 
                    return False
                else:
                    #update template with this riskProfileId
                    excel_file.df_template['riskProfileId'] = id
                    excel_file.df_template                      
                    return True
            else:
                return True 
    elif items == "milestoneConfigurationProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_milestoneConfigurationProfileId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False 
    elif items == "reviewErrorProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_reviewErrorProfileId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            yesno = st.radio("Please answer the question to continue. Do you have this feature enabled in your region?", YesNo_actions, 0)
            if yesno == yes_action:            
                id = st.text_input('reviewErrorProfileId', 'type your id here')
                if id.strip() == 'type your id here' or id.strip() == "":
                    status_widget("", "WALLE Stopped - you must provide a valid reviewErrorProfileId", "") 
                    return False
                else:
                    #update template with this reviewErrorProfileId
                    excel_file.df_template['reviewErrorProfileId'] = id
                    excel_file.df_template                      
                    return True
            else:
                return True 
            
    elif items == "userRoleConfigurationProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_userRoleConfigurationProfileId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False
    elif items == "tagConfigurationProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):                    
            gd_configuration_tagConfigurationProfileId_chk =grid_builder(df_1, user_permit.permit, 400,"gd_configuration_tagConfigurationProfileId_chk")    
            
            status_widget("", "WALLE Paused - feature Tag Profile is found in this file but they have blank value. Please click a radio button below to continue.", "") 
            info_widget("", " ~~ " + castr_rule_tagConfigurationProfileId,  "error") 

            yesno = st.radio("Please select a radio button to continue", YesNo_actions, 0)
            if yesno == yes_action:            
                id = st.text_input('tagConfigurationProfileId', 'type your id here')
                if id.strip() == 'type your id here' or id.strip() == "":
                    status_widget("", "WALLE Stopped - you must provide a valid tagConfigurationProfileId if your selection is yes above", "") 
                    return False
                else:
                    #update template with this tagConfigurationProfileId
                    excel_file.df_template['tagConfigurationProfileId'] = id
                    #--excel_file.df_template                      
                    return True
            elif yesno == no_action: 
                excel_file.df_template['tagConfigurationProfileId'] = ""
                return True
            else:
                return True
    elif items == "correctiveActionsSLAExclusionsProfileId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_correctiveActionsSLAExclusionsProfileId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_correctiveActionsSLAExclusionsProfileId_chk =grid_builder(df_1, user_permit.permit, 400, "gd_configuration_correctiveActionsSLAExclusionsProfileId_chk")    

            yesno_gd_configuration_correctiveActionsSLAExclusionsProfileId_chk = st.radio("Please answer the question to continue. Do you have this feature enabled in your region?", YesNo_actions, 0, key="esno_gd_configuration_correctiveActionsSLAExclusionsProfileId_chk")
            if yesno_gd_configuration_correctiveActionsSLAExclusionsProfileId_chk == yes_action:            
                tmpCorrectiveActionsSLAExclusionsProfileId = st.text_input('correctiveActionsSLAExclusionsProfileId', 'type your id here')
                if tmpCorrectiveActionsSLAExclusionsProfileId.strip() == 'type your id here' or tmpCorrectiveActionsSLAExclusionsProfileId.strip() == "":
                    status_widget("", "WALLE Stopped - you must provide a valid correctiveActionsSLAExclusionsProfileId if your selection is yes above", "") 
                    return False
                else:
                    #update template with this correctiveActionsSLAExclusionsProfileId
                    excel_file.df_template['correctiveActionsSLAExclusionsProfileId'] = tmpCorrectiveActionsSLAExclusionsProfileId
                    #--excel_file.df_template                      
                    return True
            elif yesno_gd_configuration_correctiveActionsSLAExclusionsProfileId_chk == no_action: 
                excel_file.df_template['correctiveActionsSLAExclusionsProfileId'] = ""
                return True
            else:
                return True
    elif items == "scoringMethodologyId":
        where1 = df_chk[items].str.strip() == ""
        df_1 = df_chk[where1]
        if ( len(df_1) > 0 ):
            status_widget("", "WALLE Stopped - Column " + items + " has blank value", "") 
            info_widget("", " ~~ " + castr_rule_scoringMethodologyId  +  "  " + items + " " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    

            yesno = st.radio("Please answer the question to continue. Do you have this feature enabled in your region?", YesNo_actions, 0)
            if yesno == yes_action:            
                id = st.text_input(items, 'type your id here')
                if id.strip() == 'type your id here' or id.strip() == "":
                    status_widget("", "WALLE Stopped - you must provide a valid " + items, "") 
                    return False
                else:
                    #update template with this scoringMethodologyId
                    excel_file.df_template[items] = id
                    #--excel_file.df_template                      
                    return True
            else:
                return True
            
    elif(items == "calculate/noncalculate"): #-- valid checking 
        where1 = df_chk['ModifyDeleteNew'].str.lower() == "m"
        where2 = df_chk['dataFacts'].str.count(',') >= 2
        where3 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where4 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == "" 
        where5 = df_chk['id'].str.strip()  == ''

        #--  calculate to non calculate change
        df_1 = df_chk[where1 & where2 & (where3 | where4)]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - A calculate test aspect is updated to a non calculate aspect!","")
            info_widget("", " ~~ " + walle_rule_calculate + "  " + error_fix_instr , "error") 
            
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400) 
            return False
        
        #--  non calculate to calculate change
        df_1 = df_chk[where1 & ~where2 & (~where3 | ~where4)]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - A non calculate test aspect is updated to a calculate test aspect!","")
            info_widget("", " ~~ " + walle_rule_calculate + "  " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400) 
            return False
        
    elif( items == "ModifyDeleteNew"):  #-- valid checking
        where1 = df_chk['ModifyDeleteNew'].str.lower()  == 'm'
        where2 = df_chk['ModifyDeleteNew'].str.lower()  == ''
        where3 = df_chk['ModifyDeleteNew'].str.lower()  =='n'
        
        df_1 = df_chk[~where1 & ~where2 & ~where3]
        df_2 = df_1.drop_duplicates()
        if ( len(df_2) > 1 ):
            status_widget("", "WALLE Stopped - Column ModifyDeleteNew has invalid value","") 
            info_widget("", " ~~ " + castr_rule_modifyDeleteNew + "  ModifyDeleteNew(s) " + error_fix_instr , "error") 
        
            gd_configuration_chk =grid_builder(df_2, user_permit.permit, 400)    
            return False
        
        #-- audit id must exist for m and d
        where4 = df_chk['id'].str.strip()  == ''
        df_1 = df_chk[where4 & where1]
        
        if ( len(df_1) > 1 ):
            status_widget("", "WALLE Stopped - Column ModifyDeleteNew has invalid value for existing test aspect", "") 
            info_widget("", " ~~ " + castr_rule_modifyDeleteNew + "  ModifyDeleteNew(s) " + error_fix_instr , "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False
        
        #-- audit id must be blank for n
        where4 = df_chk['id'].str.strip()  == ''
        df_1 = df_chk[~where4 & where3]
        if ( len(df_1) > 1 ):
            status_widget("", "WALLE Stopped - Column id must be blank when ModifyDeleteNew value is N or n", "") 
            info_widget("", " ~~ " + castr_rule_modifyDeleteNew + "  ModifyDeleteNew(s) " + error_fix_instr , "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False
        
        #-- only one row aspectId business auditType combination
        df_1 = pd.DataFrame(df[~where_holiday],columns=['aspectId','business', 'auditType'])
        df_1["is_duplicate"]= df_1.duplicated()
        where1 = df_1["is_duplicate"] == True
        where2 = df_1["aspectId"] == ""
        df_2 = df_1[where1 & ~where2]['aspectId']
        if (len(df_2) > 0):
            status_widget("", "WALLE Stopped - Column aspectId is not unique under same business and audit type", "") 
            info_widget("", " ~~ " + castr_rule_aspectId,  "error") 
            info_widget("", error_fix_instr , "info") 

            gd_configuration_chk =grid_builder(df_4, user_permit.permit, 400)    
            return False

    elif (items == 'business/displayOrder'): #-- valid checking 
        #topic/test/aspect display order can not be blank
        where1 = df_chk['topic_displayOrder'].astype(str).str.strip() == ""
        where2 = df_chk['test_displayOrder'].astype(str).str.strip() == ""
        where3 = df_chk['aspect_displayOrder'].astype(str).str.strip() == ""
        df_1 = df_chk[where1 | where2 | where3]
        if ( len(df_1) > 1 ):
            status_widget("", "WALLE Stopped - Column topic_displayOrder, test_displayOrder or aspect_displayOrder has blank value for topic/test/sspect", "") 
            info_widget("", " ~~ " + castr_rule_displayOrder  +  "  topic_displayOrder, test_displayOrder or aspect_displayOrder " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False

        #-- unique display order numbers by business type.  
        df_1 = df_chk[['business', 'topic_displayOrder','test_displayOrder','aspect_displayOrder']]
        df_2 = df_1.drop_duplicates() 
        
        if ( len(df_1)-len(df_2) > 0):
            status_widget("", "WALLE Stopped - same displayOrder for different business and aspect ", "") 
            info_widget("", " ~~ " + castr_rule_displayOrder  + "  topic_displayOrder, test_displayOrder or aspect_displayOrder " + error_fix_instr, "error") 
        
            gd_configuration_chk =grid_builder(df_2, user_permit.permit, 400)    
            return False
        
    elif (items == 'document'): #-- valid checking
        #-- document is required and length < 500.  
        where1 = df_chk['document'].str.strip() == ""
        df_1 = df_chk[where1]
        if (len(df_1) > 0):
            status_widget("", "WALLE Stopped - Column document has blank value","") 
            info_widget("", "   ~~ " + castr_rule_document + "document(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)    
            return False        
        else:
            df_1['document_len'] = df_chk['document'].apply(len)
            if (len(df_1[df_1['document_len'] > 250]) > 0):
                status_widget("", "WALLE Stopped - Column document value has more than 250 characters","") 
                info_widget("", "   ~~ " + castr_rule_document + "document(s) " + error_fix_instr , "error") 
                gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)  
                return False
            
    elif (items == 'inputFormatValues/inputComponent/value'): #-- valid checking
        df_1 = df_chk[['inputFormatValues','inputComponent','value','location','document', 'dateValueUnit']]
        df_2 = df_1.drop_duplicates()

        #-- Input inputComponent should never be blank.
        where1 = df_2['inputComponent'] == ""
        where2 = df_2['inputComponent'] == "Categorical"
        where3 = df_2['inputComponent'] == "Boolean"
        where4 = df_2['inputComponent'] == "Number"
        where5 = df_2['inputComponent'] == "Percentage"
        where6 = df_2['inputComponent'] == "String"

        df_3 = df_2[where1 | ( ~where2 & ~where3 & ~where4 & ~where5  & ~where6)]
        if (len(df_3)) > 0:
            status_widget("", "WALLE Stopped - Column inputComponent has invalid value","") 
            info_widget("", "   ~~ " + castr_rule_input_component_rule + " inputComponent(s) " + error_fix_instr , "error") 
            
            gd_configuration_chk =grid_builder(df_3, user_permit.permit, 400)  
            return False
        
        #-- Input inputFormatValues should never be blank.
        #-- where1 = df_2['inputFormatValues'] == ""
        #-- df_3 = df_2[where1]
        #-- if (len(df_3)) > 0:
        #--     status_widget("", "WALLE Stopped - Column inputFormatValues has blank value","") 
        #--     info_widget("", " ~~ " + castr_rule_input_component_format +  " inputFormatValues(s) " + error_fix_instr ,"error") 
        #--     gd_configuration_chk =grid_builder(df_3, user_permit.permit)  
        #--     return False
        
        #-- Input inputComponent should never be blank.
        where1 = df_2['value'] == ""
        where2 = df_2['document'] == "No-Show"
        df_3 = df_2[where1 & ~where2]
        if (len(df_3)) > 0:
            status_widget("", "WALLE Stopped - Column value has blank value","") 
            info_widget("", " ~~ " + castr_rule_value + " value(s) " + error_fix_instr ,"error") 
            gd_configuration_chk =grid_builder(df_3, user_permit.permit, 400)  
            return False
        
        #-- When the type is Boolean --> Yes, No and value=Yes
        where1 = df_2['inputComponent'].str.strip() == "Boolean"
        where2= df_2['inputFormatValues'].str.strip() == "Yes, No"
        df_3 = df_2[where1 &  ~where2]
        if (len(df_3)) > 0:
            status_widget("", "WALLE Stopped - Column inputFormatValues has invalid value when inputComponent is Boolean ","") 
            info_widget("", " ~~ " + castr_rule_input_component_format +  " inputFormatValues(s) and inputFormatValue(s) " + error_fix_instr  ,"error") 
            gd_configuration_chk =grid_builder(df_3, user_permit.permit, 400)  
            return False
        
        #-- When the type is Categorical --> Yes, No, N/A
        where1 = df_2['inputComponent'].str.strip() == "Categorical"
        where2= df_2['inputFormatValues'].str.strip() == ""
        df_3 = df_2[where1 & where2]
        if (len(df_3)) > 0:
            status_widget("", "WALLE Stopped - Column inputFormatValues has invalid value when inputComponent is Categorical ","") 
            info_widget("", " ~~ " + castr_rule_input_component_format +  " inputFormatValues(s) and inputFormatValue(s) " + error_fix_instr   ,"error") 
            gd_configuration_chk =grid_builder(df_3, user_permit.permit, 400)  
            return False

        #-- When the type is Number --> must provide a numeric value 
        where1 = df_2['inputComponent'].str.lower() == "number"
        df_3 = df_2[where1]
        if (len(df_3) > 0):  
                df_3['value'] = pd.to_numeric(df_3['value'], errors='coerce')  
                df_3.fillna('',inplace=True) 
                where1 = df_3['value'] == ""                        
                if (len(df_3[where1]) >0):
                    status_widget("", "Error - Column value has invalid value when inputComponent is Number","") 
                    info_widget("", " ~~ " + castr_rule_value + " inputComponent(s) and value(s) " + error_fix_instr ,"error") 
                    gd_configuration_chk =grid_builder(df_3, user_permit.permit)  
                    return False
                
        #-- When the type is Percentage --> must provide a numeric value 
        where1 = df_2['inputComponent'].str.lower() == "percentage"
        df_3 = df_2[where1]
        if (len(df_3) > 0):  
                df_3['value'] = pd.to_numeric(df_3['value'], errors='coerce')  
                df_3.fillna('',inplace=True) 
                where1 = df_3['value'] == ""                        
                if (len(df_3[where1]) >0):
                    status_widget("", "Error - Column value has invalid value when inputComponent is Percentage","") 
                    info_widget("", " ~~ " + castr_rule_input_component_format + " inputComponent(s) and value(s) " + error_fix_instr ,"error") 
                    gd_configuration_chk =grid_builder(df_3, user_permit.permit)  
                    return False
                               
                #-- when calculated test, the type is Number --> must be numeric number
                where3= df_2['inputFormatValues'] == ""
                where4= df_2['dateValueUnit'] == ""

                df_4 = df_3[~where3 | ~where4]
                if (len(df_4)) > 0:
                    status_widget("", "WALLE Stopped - Column inputFormatValues and/or dateValueUnit has non blank value when inputComponent is Percentage","") 
                    info_widget("", " ~~ CASTR Rule - inputFormatValues must be blank when inputComponent is Number for a calculate test aspect. document/inputFormatValues/dateValueUnit "+ error_fix_instr ,"error") 
                    gd_configuration_chk =grid_builder(df_4, user_permit.permit)  
                    return False
                
    elif (items == 'business/audittype/section/sectionId'):  #-- template valid checking
        #-- 1st no blank section
        where1 = df_chk['section'].str.strip() == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column Section has blank value  ","")
            info_widget("", " ~~ " + castr_rule_section + " Section(s) " + error_fix_instr  ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False

        #-- 2nd no blank sectionId
        where1 = df_chk['sectionId'].str.strip() == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column sectionId has blank value  ","")
            info_widget("", " ~~ " + castr_rule_sectionID + " Section(s) " + error_fix_instr  ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        #-- 2nd no whitespace inside sectionId
        where1 = df_chk['sectionId'].str.contains(' ')== True
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column sectionId contians whitespace  ","")
            info_widget("", " ~~ " + castr_rule_sectionID + " Section(s) " + error_fix_instr  ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
            
        #-- 3rd no duplicate
        df_1 = df_chk[['business', 'auditType', 'section', 'sectionId']]
        df_2 = df_1.drop_duplicates()
        df_3 = (df_2.groupby(['business','auditType','section'])['sectionId'].agg(["unique","nunique"]).reset_index())
        where1 = df_3['nunique'] > 1
        if ( len(df_3[where1]) > 1 ):
            status_widget("", "WALLE Stopped - Column sectionId has different value for same business, audit type and section ", "") 
            info_widget("", " ~~ " + castr_rule_sectionID + " Section(s) " + error_fix_instr  ,"error") 
        
            gd_configuration_chk =grid_builder(df_2, user_permit.permit)    
            return False
    
    elif (items == 'business/audittype/topic/topicId'): #-- valid checking
        #-- 1st no blank test
        where1 = df_chk['topic'] == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column topic has blank value  ","")
            info_widget("", " ~~ " + castr_rule_topic + " Topic(s) " + error_fix_instr ,"error") 
            return False

        #-- 2nd no blank testId
        where1 = df_chk['controlId'] == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column controlId has blank value:  ","")
            info_widget("", " ~~ " + castr_rule_controlID + " Control(s) " + error_fix_instr  ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)   
            return False
        
        #-- 3rd no duplicate
        df_1 = df_chk[['business', 'auditType', 'topic', 'controlId']]
        df_2 = df_1.drop_duplicates()
        df_3 = (df_2.groupby(['business','auditType','topic'])['controlId'].agg(["unique","nunique"]).reset_index())
        where1 = df_3['nunique'] > 1
        if ( len(df_3[where1]) > 1 ):
            status_widget("", "WALLE Stopped - Column controlId has different value for same business, audit type and topic ", "") 
            info_widget("", " ~~ " + castr_rule_controlID + " Control(s) " + error_fix_instr  ,"error") 
        
            gd_configuration_chk =grid_builder(df_3[where1], user_permit.permit, 400)    
            return False

    elif (items == 'business/audittype/topic/test/testId'):  #-- valid checking
        #-- 1st no blank test
        where1 = df_chk['test'] == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column test has blank value  ","")
            info_widget("", " ~~ " + castr_rule_test + " Test(s) " + error_fix_instr ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False

        #-- 2nd no blank testId
        where1 = df_chk['testId'] == ""
        df_1 = df_chk[where1]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column testId has blank value  ","")
            info_widget("", " ~~ " + castr_rule_testID + " Test(s) " + error_fix_instr ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400) 
            return False

        #-- 3rd no multiple testId for test
        df_1 = df_chk[['business','auditType','topic', 'test', 'testId']]
        df_2 = df_1.drop_duplicates()
        df_3 = (df_2.groupby(['business','auditType','topic','test'])['testId'].agg(["unique","nunique"]).reset_index())
        where1 = df_3['nunique'] > 1
        if ( len(df_3[where1]) > 1 ):
            status_widget("", "WALLE Stopped - Column test has different value for same business, audit type, topic and testId", "") 
            info_widget("", " ~~ " + castr_rule_testID + " Test(s) " + error_fix_instr ,"error") 
        
            gd_configuration_chk =grid_builder(df_3[where1], user_permit.permit, 400)    
            return False
        
        #-- 4th no multiple test for same test
        df_1 = df_chk[['business','auditType','topic', 'test', 'testId']]
        df_2 = df_1.drop_duplicates()
        df_3 = (df_2.groupby(['business','auditType','topic','testId'])['test'].agg(["unique","nunique"]).reset_index())
        where1 = df_3['nunique'] > 1
        if ( len(df_3[where1]) > 1 ):
            status_widget("", "WALLE Stopped - Column testId has different value for same business, audit type, topic and test", "") 
            info_widget("", " ~~ " + castr_rule_testID + " Test(s) " + error_fix_instr ,"error") 

            gd_configuration_chk =grid_builder(df_2, user_permit.permit, 400)    
            return False
        
    elif (items == "FactName_1 (Later Date/Larger Number)/FactName_2 (Earlier Date/Smaller Number)"):

        #-- calculated rows must have FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number)
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        df_1 = df_chk[(~where1 & where2) | (where1 & ~where2)]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - either column FactName_1 (Later Date/Larger Number) or FactName_2 (Earlier Date/Smaller Number) is blank  ","")
            info_widget("", " ~~ " + castr_rule_calculate_test_aspect + "  " + error_fix_instr ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        #-- calculated row must has document for fact_1
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_1_Document'] == ""
        df_1 = df_chk[~where1 & where2]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column FactName_1_Document is blank when FactName_1 (Later Date/Larger Number) have value  ","")
            info_widget("", "   ~~ " + castr_rule_fact_document + " FactName_1_Document(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_1_inputComponent'] == ""
        df_1 = df_chk[~where1 & where2]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column FactName_1_inputComponent is blank when FactName_1 (Later Date/Larger Number) have value  ","")
            info_widget("", "   ~~ " + castr_rule_input_component_rule + " FactName_1_inputComponent(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        

        #-- calculated row must has document for fact_2
        where1 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where2 = df_chk['FactName_2_Document'] == ""
        df_1 = df_chk[~where1 & where2]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column FactName_2_Document is blank when FactName_2 (Earlier Date/Smaller Number) have value  ","")
            info_widget("", "   ~~ " + castr_rule_fact_document + " FactName_2_Document(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        where1 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where2 = df_chk['FactName_2_inputComponent'] == ""
        df_1 = df_chk[~where1 & where2]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column FactName_2_inputComponent is blank when FactName_2 (Earlier Date/Smaller Number) have value  ","")
            info_widget("", "   ~~ " + castr_rule_input_component_rule + " FactName_2_inputComponent(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        #-- calculated row document must be Calculated
        #-- where3 = df_chk['document'].str.strip() == "Calculated"
        #-- df_1 = df_chk[~where1 & ~where2 & ~where3]
        #-- if (len(df_1)) > 0:
        #--    status_widget("", "WALLE Stopped - Column document has invalid value for a calculate test aspect  ","")
        #--     info_widget("", "   ~~ " + castr_rule_document + " document(s) " + error_fix_instr , "error") 
        #--     gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
        #--    return False
        
        #-- calculated row must has fact_operator
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where3 = df_chk['operator'] == ""
        df_1 = df_chk[(~where1 & ~where2) & where3]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column Fact_Operator(s) is blank when both FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number) have value  ","")
            info_widget("", "   ~~ " + castr_rule_fact_operator + " Fact_Operator(s) " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        #-- calculated row must has value
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where3 = df_chk['value'] == ""
        df_1 = df_chk[(~where1 & ~where2) & where3]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column value has blank value  ","")
            info_widget("", "   ~~ " + castr_rule_value + " value " + error_fix_instr , "error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit, 400)
            return False
        
        #-- calculated row must has inputComponent
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where3 = df_chk['inputComponent'] == "Number"
        df_1 = df_chk[(~where1 & ~where2) & ~where3]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - inputComponent(s) is not correct:  ","")
            info_widget("", " ~~ Calculated rows inputComponent must be number. Fix the error in source input file offline before using this tool." ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit)
            return False
        
        #-- calculated row must has blank inputFormatValues
        where1 = df_chk['FactName_1 (Later Date/Larger Number)'] == ""
        where2 = df_chk['FactName_2 (Earlier Date/Smaller Number)'] == ""
        where3 = df_chk['inputFormatValues'] == ""
        df_1 = df_chk[(~where1 & ~where2) & ~where3]
        if (len(df_1)) > 0:
            status_widget("", "WALLE Stopped - Column inputFormatValues(s) is not blank for calculate test aspect:  ","")
            info_widget("", " ~~ Calculated rows inputFormatValues must be blank. Fix the error in source input file offline before using this tool." ,"error") 
            gd_configuration_chk =grid_builder(df_1, user_permit.permit)
            return False

    elif items == "business" :
        if df_chk['business'].str.contains("-").any() == False:
            status_widget("", "WALLE Stopped - Column business has invalid value format", "") 
            info_widget("", " ~~ " + castr_rule_business + " business(s) " + error_fix_instr ,"error") 
            
            return False
        
    return True
