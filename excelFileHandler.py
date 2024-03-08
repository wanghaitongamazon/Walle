class excelFile():
    def _init_(self ):
        self.df_template = pd.DataFrame()
        self.df_template_display = pd.DataFrame()
        self.df_auditConfigurationDetails = pd.DataFrame()
        self.df_template_auditRules= pd.DataFrame()
        self.df_template_dataFacts= pd.DataFrame()
        self.df_template_dataFactSources =pd.DataFrame()
        self.df_auditRules = pd.DataFrame()
        self.df_dataFactSources = pd.DataFrame()
        self.df_dataFacts = pd.DataFrame()
        #-- new rows in template
        self.df_template_new = pd.DataFrame()
        #-- modified rows in template
        self.df_template_modification = pd.DataFrame() 
        #-- delete rows in template
        self.df_template_delete = pd.DataFrame()
        
        #-- prod configs for checking summary
        self.df_prod_auditConfigurationDetails = pd.DataFrame()
        self.df_prod_auditRules= pd.DataFrame()
        self.df_prod_dataFacts= pd.DataFrame()
        self.df_prod_dataFactSources =pd.DataFrame()

        self.dataFacts_column_list = []

    def load_file(self, filename, from_which_menu):
        xls = pd.ExcelFile(filename)
        bValid = True
        for sheet_name in xls.sheet_names:
            df = df_GetSheet(filename, sheet_name)
            df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
            if sheet_name.strip() == "Template":
                if from_which_menu == create_configuration_file:
                    df['document'] = df['document'].str.replace('\n', "").str.replace('\r', "")                               
                    self.df_template = self.columnNameCorrection(df)
                    #-- validate section/sectionId unique
                    with st.spinner("WALLE is validing input template data.."):    
                        bValid = template_data_error_checking(self.df_template, 'business/audittype/section/sectionId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'business/audittype/topic/topicId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'business/audittype/topic/test/testId', NULL)   
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'business/aspect/displayOrder', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'document', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'calculate/noncalculate', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'FactName_1 (Later Date/Larger Number)/FactName_2 (Earlier Date/Smaller Number)', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'inputFormatValues/inputComponent/value', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'ModifyDeleteNew', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'business/displayOrder', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'riskPointsTest/scoringMethodologyId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'operator', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'capId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'business', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'entity', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'riskProfileId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'milestoneConfigurationProfileId', NULL)
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'reviewErrorProfileId', NULL)   
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'userRoleConfigurationProfileId', NULL)    
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'tagConfigurationProfileId', NULL)  
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'scoringMethodologyId', NULL) 
                        if bValid == True:
                            bValid = template_data_error_checking(self.df_template, 'correctiveActionsSLAExclusionsProfileId', NULL) 
                            

                    if bValid == True:
                        where1 =  self.df_template['ModifyDeleteNew'].str.lower() == 'm'
                        self.df_template_modification = self.df_template[where1]
                        where1 =  self.df_template['ModifyDeleteNew'].str.lower() == 'n'
                        self.df_template_new= self.df_template[where1]
                        where1 =  self.df_template['ModifyDeleteNew'].str.lower() == 'd'
                        self.df_template_delete= self.df_template[where1]
                        where1 =  self.df_template['ModifyDeleteNew'].str.lower() == ''
                        where2 =  self.df_template['ModifyDeleteNew'].str.lower() == 's'
                        self.df_template= self.df_template[where1 | where2]
                        st.session_state.gd_template = True
                        self.selfService_template_column_list =df.columns.values.tolist()
                else:
                    self.df_template = df
                    #-- add file name
                    #-- self.df_template['SouceFileName'] = filename
                    self.selfService_template_column_list =df.columns.values.tolist()
                    st.session_state.gd_template = True
            elif sheet_name == "AuditRules":
                self.df_auditRules = self.columnNameCorrection(df)
                self.auditRules_column_list = df.columns.values.tolist()
                st.session_state.gd_auditRules = True
            elif sheet_name == "DataFacts":
                self.df_dataFacts = df
                self.dataFacts_column_list = df.columns.values.tolist()
                st.session_state.gd_dataFacts = True
            elif sheet_name == "DataFactSources":
                self.df_dataFactSources = df
                st.session_state.gd_dataFactSources = True
            elif sheet_name == "AuditConfigurationDetails":
                self.df_auditConfigurationDetails =df
                #-- add file name
                #-- self.df_auditConfigurationDetails['SouceFileName'] = filename
                self.auditConfigurationDetails_column_list = df.columns.values.tolist()
                st.session_state.gd_configurationDetails = True
            elif sheet_name == "Template_AuditRules":
                self.df_template_auditRules= df
                self.df_prod_auditRules= df
                self.auditRules_column_list = df.columns.values.tolist()
                st.session_state.gd_template_auditRules = True
            elif sheet_name == "Template_DataFacts":
                self.df_template_dataFacts= df
                self.df_prod_dataFacts= df
                self.dataFacts_column_list = df.columns.values.tolist()
                st.session_state.gd_template_dataFacts = True
            elif sheet_name == "Template_DataFactSources":
                self.df_template_dataFactSources= df
                self.df_prod_dataFactSources= df
                st.session_state.gd_template_dataFactSources = True
            elif sheet_name == "Temp_AuditConfigurationDetails":
                self.df_template_auditConfigurationDetails =df
                self.df_prod_auditConfigurationDetails = df
                self.auditConfigurationDetails_column_list = df.columns.values.tolist()
                st.session_state.gd_template_configurationDetails = True
            elif sheet_name == "HolidayLocation":
                self.holiday_location_list = df['location'].values.tolist()
            elif sheet_name == "LocationSectionCap":
                self.df_SlaProfile = df
            elif sheet_name == "Location":
                self.location_list = df['location'].values.tolist()
            elif sheet_name == "Business Program":
                self.business_list = df['id'].values.tolist()
            elif sheet_name == "Audit Type":
                self.audit_type_list = df['id'].values.tolist()
            elif sheet_name == "MR_AuditTypes":
                self.df_mr_auditTypes = df
                st.session_state.gd_mr_auditTypes = True
            elif sheet_name == "MR_Milestones":
                self.df_mr_milestones = df
                st.session_state.gd_mr_milestones = True
            elif sheet_name == "ReviewErrorProfiles":
                self.df_reviewErrorProfile = df
            elif sheet_name == "UserRoleConfigurationProfiles":
                self.df_userRoleConfigurationProfile = df
            elif sheet_name == "MilestoneConfigurationProfiles":
                self.df_milestoneConfigurationProfile = df
            elif sheet_name == "CorrectiveActionItemProfiles":
                self.df_correctiveActionItemProfile = df
            elif sheet_name == "RiskProfiles":
                self.df_riskProfiles = df
            elif sheet_name == "TagConfigurationProfiles":
                self.df_tagConfigurationProfiles = df
            elif sheet_name == "ConditionalTests":
                self.df_conditionTests = df
                st.session_state.gd_conditionalTests = True
            elif sheet_name == "SST-Columns":
                self.df_SST_template_DisplayColumns_list = df['TemplateColumnDisplay'].values.tolist()
                self.df_SST_template_DisplayColumns_list  = [i for i in self.df_SST_template_DisplayColumns_list if i]
                
                self.df_SST_template_ReadOnlyColumns_list = df['TemplateColumnReadOnly'].values.tolist()
                self.df_SST_template_ReadOnlyColumns_list  = [i for i in self.df_SST_template_ReadOnlyColumns_list if i]

                self.df_SST_auditRules_Columns_list = df['AuditRules'].values.tolist()
                self.df_SST_auditRules_Columns_list  = [i for i in self.df_SST_auditRules_Columns_list if i]

                self.df_SST_dataFacts_Columns_list = df['DataFacts'].values.tolist()
                self.df_SST_dataFacts_Columns_list  = [i for i in self.df_SST_dataFacts_Columns_list if i]

                self.df_SST_dataFactSources_Columns_list = df['DataFactSources'].values.tolist()
                self.df_SST_dataFactSources_Columns_list  = [i for i in self.df_SST_dataFactSources_Columns_list if i]

                self.df_SST_auditConfigurationDetails_Columns_list = df['AuditConfigurationDetails'].values.tolist()
                self.df_SST_auditConfigurationDetails_Columns_list  = [i for i in self.df_SST_auditConfigurationDetails_Columns_list if i]
                
                self.df_SST_conditionalTesting_Columns_list = df['ConditionalTesting'].values.tolist()
                self.df_SST_conditionalTesting_Columns_list  = [i for i in self.df_SST_conditionalTesting_Columns_list if i]

        return bValid
    
    def columnNameCorrection(self, df):
        cols = df.columns
          
        for col in range(len(cols)):
            if cols[col] == 'Control':
                df.rename(columns={'Control':'control'}, inplace=True)  
            if cols[col] == 'ControlId':
                df.rename(columns={'ControlId':'controlId'}, inplace=True)  
        return df

    def display_template_required_column(self, df_template):
        disply_column = [i for i in self.selfService_template_column_list if i not in self.df_SST_template_ReadOnlyColumns_list]
        self.df_template_display= df_template[disply_column]
    
    #-- make sure self service template columns match the list in model
    def create_template_column_list(self):
        tmp_list = []
        #-- datafacts
        if st.session_state.gd_dataFacts:
            tmp_list = ['dataFacts' if item == 'id' else item for item in self.dataFacts_column_list]
            tmp_list = ['dataFactName' if item == 'name' else item for item in tmp_list]
            tmp_list.remove('unique_index')
       
        #-- datafact + auditrules
        if st.session_state.gd_auditRules:
            tmp_list = tmp_list + self.auditRules_column_list
            tmp_list.remove('unique_index')

        #-- need to make sure model has the update to date columns
        #-- check if country file has all columns in model, not all country file has same columns
        for column in self.df_SST_auditRules_Columns_list:
            if column not in (tmp_list):
                tmp_list.append(column)

        #-- datafact + configuration details
        if st.session_state.gd_configurationDetails:
            tmp_list = tmp_list + self.auditConfigurationDetails_column_list
        
        #-- check if country file has all columns in model, not all country file has same columns 
        for column in self.df_SST_auditConfigurationDetails_Columns_list:
            if column not in (tmp_list):
                tmp_list.append(column)

        full_list = self.df_SST_template_DisplayColumns_list + tmp_list + self.df_SST_template_ReadOnlyColumns_list
    
        #-- full_list = set(self.df_SST_template_DisplayColumns_list + tmp_list + self.df_SST_template_ReadOnlyColumns_list)

        dictionary = dict.fromkeys(full_list)
        self.selfService_template_column_list = list(dictionary)
    
    def create_writer(self, filename):
        pandas.io.formats.excel.ExcelFormatter.header_style = None
        self.writer = pd.ExcelWriter(filename)

    def createMilestonesTab(self, df):
        self.df_mr_milestones = pd.DataFrame()
        df_tmp = df
        df_tmp = df_tmp.fillna('')

        where1 = df_tmp['milestoneConfigurationProfileId'] == ""
        df_1 = df_tmp[~where1]
        self.df_mr_milestones = pd.concat([df_1[['location','business', 'milestoneConfigurationProfileId']], self.df_mr_milestones], ignore_index=True)
        self.df_mr_milestones.drop_duplicates(subset=['location', 'business', 'milestoneConfigurationProfileId'],inplace=True)
        st.session_state.gd_mr_milestones = True

    def createAuditTypesTab(self, df):
        self.df_mr_auditTypes = pd.DataFrame()
        df_tmp = df
        df_tmp = df_tmp.fillna('')

        where1 = df_tmp['auditType'] == ""
        df_1 = df_tmp[~where1]
        # iterate through each row and select
       
        for ind in df_1.index:
            children = df_1["auditType"][ind].split(",")
            children_business = df_1["business"][ind].split(",")
            if ( len(children)> 0):           
                for child in children:
                    child_auditType = child.strip() 
                    # loop business
                    if ( len(children_business)> 0):    
                         for child_business in children_business:
                            tmp_business = child_business.strip()      
                            tmp_df_auditType = pd.DataFrame({'auditType': [child_auditType], 'location':[df_1["location"][ind]],'business':[tmp_business]}) 

                            # add to the list
                            self.df_mr_auditTypes = pd.concat([tmp_df_auditType, self.df_mr_auditTypes], ignore_index=True)
                            self.df_mr_auditTypes.drop_duplicates(subset=['auditType','location','business'],inplace=True)
                            st.session_state.gd_mr_auditTypes = True

    def createConditionalTestsTab(self, df):
        self.df_conditionTests = pd.DataFrame()
        df_tmp = df
        df_tmp = df_tmp.fillna('')

        where1 = df_tmp['dependentTestAspects'] == ""
        df_1 = df_tmp[~where1]
        
        # iterate through each row and select
       
        for ind in df_1.index:

            children = df_1["dependentTestAspects"][ind].split(",")
           
            if ( len(children)> 0):           
                for child in children:
                    child_aspect_id = child.strip()     

                    # get child test, aspect
                    where2 = df['id'] == child_aspect_id
                    df_child = df[where2] 

                    tmp_df_conditionTests = pd.DataFrame({'topic': df_1['topic'][ind], 'parentTestAspectId': df_1['id'][ind], 'parentTest': df_1['test'][ind], 'parentTestAspect': df_1['aspect'][ind], 
                                                        'dependentTest': df_child['test'], 'dependentTestAspect':df_child['aspect'],'dependentTestAspectId': child_aspect_id}) 

                    # add to the list
                    self.df_conditionTests = pd.concat([tmp_df_conditionTests, self.df_conditionTests], ignore_index=True)

    def FindDataFactSourceByName(self, name, dataFactSourceID, df):
        where1 =  df['name'].str.lower() == name.lower()
        return df[where1]
    
    def CreateDataFactSourceId(self, name, df):
        tmp_id = castr_rule_definder.ruleIdPrefix + name.replace(' ', "_").replace('"', '').replace(',', '')
        # id lengh should be exceed 50 charactors long
        if len(tmp_id) > 50:
            tmp_id = tmp_id[0:50]

        #-- need to check if differencet id for same document
        n = 0
        while (tmp_id.lower() in df['id'].str.lower().values.tolist()):
            n = n + 1
            tmp_id = tmp_id[0:len(tmp_id)-3] + "_" + str(n)
        
        return tmp_id
    
    def FindDataFactByNameTypeEntityDocument(self, name, dataFactType, entity, document, dataFactID, df, df_datafactsource):
        where1 = df_datafactsource['name'].str.lower() == document.lower()
        df_temp = df_datafactsource[where1]

        where1 =  df['name'].str.lower() == name.lower()
        where2 =  df['type'].str.lower() == dataFactType.lower()
        where3 =  df['entity'].str.lower() == entity.lower()
        where4 =  df['dataFactSourceId'] == df_temp['id'].values[0]
        return df[where1 & where2 & where3 & where4]
        
    
    def CreateDataFactId(self, name, dataFactType, entity, df):
        tmp_id = castr_rule_definder.ruleIdPrefix  + name.replace(' ', "_").replace('"', '').replace(',', '')
        #-- create a new datafact Id_1
        if (len(name) > 30):
            tmp_id = castr_rule_definder.ruleIdPrefix + name.replace(' ', "_").replace('"', '').replace(',', '')[:15] + "_" + name.replace(' ', "_").replace('"', '').replace(',', '')[30:15] + "_" + name.replace(' ', "_").replace('"', '').replace(',', '')[-15]

        #-- make sure this new id is unique
        n= 0
        while (tmp_id.lower() in df['id'].str.lower().values.tolist()):
            n = n + 1
            tmp_id = tmp_id[0:len(tmp_id)-3] + "_" + str(n)

        return tmp_id
    