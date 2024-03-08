st.subheader('Introduction')
st.markdown ("WALLE- CASTR Self Service SSA Tool is a python application. It helps a POC preparing high quality configuration data in a self-service way. The final file meets CASTR file uploader requirments and will be digested by CASTR. With WALLE you also can - ")

lst = ['Allow a user download the most recent production config file', 
        'Creat a self-service template base off a CASTR config file and continue to work on the data in the file off line',
        'Create a brand new self-service template for new onboard region', 
        'Create a CASTR configuration file base off a finalized self-service template.',  
        'Improve CASTR config input data quality', 
        'Submit a SIM for trouble shooting (all users)',
        'Upload a CASTR config to UAT, QA and Beta environment (TAP team only)',
        'Stack files, either CASTR configuration files or self service template',
        'View CASTR QuickSight dashboards - CASTR Audits, audit-score Impact Analysis and CASTR Metrics']

s =''
for i in lst:
    s += "- " + i + "\n"

st.markdown(s)



status_widget("","","In order to continue, please click an action under Main Menu on left side window :point_left:")