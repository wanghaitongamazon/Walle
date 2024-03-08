document_selected = option_menu(
    menu_title= "",
    options= ['Intruduction', 'User Guide', 'Update WALLE Tool to the Latest Version', 'CASTR Configuration File Rules', 'WALLE Input Template Data Quality Checking'],
    menu_icon="cast",
    default_index=0,
    icons=['', 'file-earmark-text','cloud-download','file-earmark-text'],
    orientation="horizontal"
)

if document_selected == 'Intruduction':
    status_widget("","", "**If you want to update WALLE tool to the lastest verion then follow the steps below** - :point_down: to continue. ")
    lst = ["1. Click **Update WALLE Tool to the Latest Version** :point_up:, it opens WorkDocs folder named Python in a new browser tab", '2. On WorkDocs browser tab, select all files and sub folders from WorkDocs folder Python', '3. On WorkDocs browser tab, click Download under Actions dropdown. This step saves the selected file to your laptop', '4. Once download completes, copy and paste just downloaded config file to your lap top CASTR config folder. Example C:\\Users\\your alias\\Documents\\CASTR Configs\\', '5. Once you complete the above steps,  close this browser.',  '6. Double click C:\\Users\\your alias\\Documents\\CASTR Configs\\walle.bat to lauch WALLE tool']
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    status_widget("","", "**If you are looking for a document on how to setup WALLE tool on a laptop, how to fix issues during WALLE setup, and how to use WALLE to create self service template or CASTR configuration file**, click **User Guide** - :point_up: to continue. ")

    status_widget("","", "**If you are looking for a config rules document which are being implemented in CASTR or WALLE tool**, click **CASTR Configuration File Rules** - :point_up: to continue. ")
    
    status_widget("","", "**If you are looking for a what data quality is being checked in WALLE tool** , click **WALLE Input Template Data Quality Checking** - :point_up: to continue. ")

elif document_selected == 'Update WALLE Tool to the Latest Version':
    webbrowser.open_new_tab("https://amazon.awsapps.com/workdocs/index.html#/folder/425b350f47a9235503b525174cb911faca76da5864f5ea0a0039bde7041f502c")
    st.markdown("Quip file WALLE User Guide has been opened in a new tab. ")

elif document_selected == 'User Guide':
    webbrowser.open_new_tab("https://quip-amazon.com/hGRnADESQoMF/WALLE")
    st.markdown("Quip file WALLE User Guide has been opened in a new tab. ")

elif document_selected == 'CASTR Configuration File Rules':
    webbrowser.open_new_tab("https://quip-amazon.com/YYhBAmfEbaE9/Config-Rules#temp:C:INbda68ed839a614f76a9fc0067a")
    st.markdown("Quip file Config Rules has been opened in a new tab. ")

elif document_selected == 'WALLE Input Template Data Quality Checking':
    webbrowser.open_new_tab("https://quip-amazon.com/EKwTAF6XDY9b/WALLE-Input-Template-Data-Quality-Checking")
    st.markdown("Quip file Config Rules has been opened in a new tab. ")
          