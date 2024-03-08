#---------------------------------------------------------------------------------#
#    purpose : 1> allow user either download a castr config file from workdoc     #
#              2> create a brand new self service template file                   #
#    source:                                                                      #
#    output : excel file with with a tab, tab name is Tempalte                    #
#---------------------------------------------------------------------------------#

#-- functions on Template builder web page
file_selection_mode = option_menu(
    menu_title= "",
    options= [selection_modes.instruction.value, selection_modes.download_latest_prod_config_file.value, selection_modes.build_brand_new_self_service_template.value],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

#--  instructions on what kind of template file to build
if file_selection_mode == selection_modes.instruction.value:
    status_widget("","", "If you are new onbard country and looking for a " + file_name_management.self_service_template_file.value + " to start then the steps below - :point_up: to continue. ")
    lst = ["1. Click **" + selection_modes.build_brand_new_self_service_template.value + "** :point_up:", '2. WALLE will create a brand new ' + file_name_management.self_service_template_file.value, ' 3. WALLE will save a brand new self service template in yoru laptop', '4. Once the process completes, you can work on the file off line']
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)
    
    status_widget("","", "If you are looking for a production config file for reference, click **Download " + file_name_management.castr_config_file.value + "** :point_up:  , then follow the steps below to continue")
    lst = ["1. Click **" + selection_modes.download_latest_prod_config_file.value + "** :point_up: to open WorkDocs folder named Latest Config Files", '2. Select a region config file from WorkDocs Latest Config Files folder', '3. On WorkDocs window, click Download under Actions dropdown. This step saves the selected file to your laptop', '4. Once download completes, you can work on the file off line']
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    status_widget("","", "If you are going to update a couple of small changes and familiar with CASTR config file format click **" + selection_modes.download_latest_prod_config_file.value + "** :point_up: to continue")
    st.markdown(s)

    status_widget("","", "If you are going to add or delete row(s) in a config file then follow the steps below -  :point_down: to continue")
    lst = ["1. Click **" + selection_modes.download_latest_prod_config_file.value + "** :point_up: to open WorkDocs folder named Latest Config Files", '2. Select a region config file from WorkDocs Latest Config Files folder', 
            '3. On WorkDocs window, click Download under Actions dropdown. This step saves the selected file to your laptop', 
            '4. Once download completes, copy and paste just downloaded config file to CASTR config folder. Example C:\\Users\\your alias\\Documents\\CASTR Configs\\Configuration Files\\', 
            '5. Once you completes the above steps, On WALLE window under **Main Menu** :point_left: , click **' + selection_modes.build_self_service_template.value + "**.  WALLE creates a self service template file under C:\\Users\\your alias\\Documents\\CASTR Configs\\Tempaletes\\",
            '6. Work on self service template file off line']
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)
#-- start to build a brand new self service template from scrach    
elif file_selection_mode == selection_modes.build_brand_new_self_service_template.value:
    #load model file
    excel_file.load_file(file_location_management.modelFilePath.value.replace("[userid]", os.getlogin()), "")
    with st.expander("See explanation"):
        st.write("The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
        business = st.selectbox('Business Program', excel_file.business_list)
        auditType = st.multiselect('Audit Type', excel_file.audit_type_list)
        capId = st.selectbox('capId', set(excel_file.df_correctiveActionItemProfile[excel_file.df_correctiveActionItemProfile['id'] != '']['id'].values.tolist()), index=0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        location = st.selectbox('Location',excel_file.location_list) 
    with col2:
        riskProfileId = st.selectbox('riskProfileId', set(excel_file.df_riskProfiles['id'].values.tolist()), index=0)
        milestoneConfigurationProfileId = st.selectbox('milestoneConfigurationProfileId', set(excel_file.df_milestoneConfigurationProfile['id'].values.tolist()))
        userRoleConfigurationProfileId =st.selectbox('userRoleConfigurationProfileId', set(excel_file.df_userRoleConfigurationProfile['id'].values.tolist()))
        reviewErrorProfileId = st.selectbox('reviewErrorProfileId', set(excel_file.df_reviewErrorProfile['id'].values.tolist()))
    with col3:
        tagConfigurationProfileId =st.selectbox('tagConfigurationProfileId', ['', set(excel_file.df_tagConfigurationProfiles['id'].values.tolist())])
        scoringMethodologyId = st.selectbox('tagConfigurationProfileId', ['bottom_up_weights'])
        breachOfContractMilestoneConfigurationProfileId =st.selectbox('breachOfContractMilestoneConfigurationProfileId',['','BOC_Apr_2022'])

    if len(auditType) == 0 :
        #stop here
        info_widget(""," You must provide values to above CASTR fields in order to create a brand new self service ",'error')
    else:

        with st.spinner("WALLE is building template file..."):
            
            excel_file.create_template_column_list()

            rows, cols = (len(excel_file.selfService_template_column_list), len(excel_file.selfService_template_column_list))
            lst = [[""]*cols] * rows
            df_new_template_1 = pd.DataFrame(lst, columns =excel_file.selfService_template_column_list)
            df_new_template_1.drop_duplicates(subset=['location','ModifyDeleteNew'],inplace=True)
            df_new_template_1['ModifyDeleteNew'][0] = "N"
            df_new_template_1['location'][0] = location
            df_new_template_1['business'][0] = business
            tmp_type = ""
            for i in range(len(auditType)) :
                tmp_type = tmp_type + auditType[i] + ","
            df_new_template_1['auditType'][0] = tmp_type[0:len(tmp_type) -1]

            df_new_template_1['capId'][0] = capId
            df_new_template_1['riskProfileId'][0] = riskProfileId
            df_new_template_1['milestoneConfigurationProfileId'][0] = milestoneConfigurationProfileId
            df_new_template_1['userRoleConfigurationProfileId'][0] = userRoleConfigurationProfileId
            df_new_template_1['reviewErrorProfileId'][0] = reviewErrorProfileId
            df_new_template_1['tagConfigurationProfileId'][0] = tagConfigurationProfileId
            df_new_template_1['scoringMethodologyId'][0] = scoringMethodologyId
            df_new_template_1['breachOfContractMilestoneConfigurationProfileId'][0] = breachOfContractMilestoneConfigurationProfileId


            file_name = "Template_Config_Data" + "_" + datetime.datetime.now().strftime('%Y_%m_%d') + ".xlsx"        
            save_file_path_name = file_location_management.self_service_template_file_folder.value.replace("[userid]", os.getlogin()) + "\\" + file_name
            excel_file_save = excelFile()
            excel_file_save.create_writer(save_file_path_name ) 
            with excel_file_save.writer as writer:
                df_new_template_1.to_excel(writer, sheet_name = "Template", index = False)
                worksheet = writer.sheets['Template']
                workbook = writer.book

                # read only column Green fill with dark green text.
                green_format = workbook.add_format({'bg_color':   '#C6EFCE',
                                            'font_color': '#006100'})

                # Create a cell format with protection properties.
                unlocked = workbook.add_format({'locked': False})
                
                cols = df_new_template_1.columns.values.tolist()
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
                writer.close()

                ## with open(file_path_name, 'rb') as my_file:
                ##s download_button_str = st.download_button(label = 'Click me to download the file and save it to your local computer', data = my_file, file_name = file_name, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      
                info_widget("","A self service tempalte has been created successful. The file is saved in: " + save_file_path_name,"success")

#-- start to open a workdoc in a new browser        
elif file_selection_mode == selection_modes.download_latest_prod_config_file.value:
    webbrowser.open_new_tab('https://amazon.awsapps.com/workdocs/index.html#/folder/db6510fe04c3cb550b382a99ee9ec623c02bd4bc22e5e9402d0535f6df68ad76')
    st.markdown("WorkDoc folder Latest Config Files has been opened in a new tab. ")
