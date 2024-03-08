import enum
#-- file types constants
class file_name_management(enum.Enum):
    self_service_template_file = "Self Service Template File"
    castr_config_file = "CASTR Configuration File"

#-- castr config file sheets constatns
class castr_config_file(enum.Enum):
    dataFacts = "DataFacts"   
    dataFactSources = "DataFactSources"
    auditRules = "AuditRules"
    auditConfigurationDetails = "AuditConfigurationDetails"
    conditionalTests ="ConditionalTests"

#-- castr config file sheets constatns
class self_service_template_file(enum.Enum):
    template_dataFacts = "Template_DataFacts"   
    template_dataFactSources = "Template_DataFactSources"
    template_auditRules = "Template_AuditRules"
    auditConfigurationDetails = "AuditConfigurationDetails"
    conditionalTests ="ConditionalTests"
    template = "Template"

#-- WALLE web page functions constants
class selection_modes(enum.Enum):
    instruction = "Instruction"
    build_self_service_template = "Start to Build " + file_name_management.self_service_template_file.value
    build_castr_config_file = "Start to Build " + file_name_management.castr_config_file.value
    add_conditional_test = "Add sheet " + castr_config_file.conditionalTests.value + " to " + file_name_management.castr_config_file.value
    download_latest_prod_config_file = 'Download ' + file_name_management.castr_config_file.value
    build_brand_new_self_service_template = "Download Brand New " + file_name_management.self_service_template_file.value
    stack_self_service_template = "Start to Stack " + file_name_management.self_service_template_file.value
    stack_castr_config_file = "Start to Stack " + file_name_management.castr_config_file.value
    correct_display_order_self_service_template= 'Correct displyOrder in ' + file_name_management.self_service_template_file.value
    correct_display_order_castr_config_file = 'Correct displyOrder in ' + file_name_management.castr_config_file.value

#-- WALLE file location management constants
class file_location_management(enum.Enum):
    root_folder = r"C:\Users\[userid]\Documents\CASTR Configs"
    modelFilePath = r"C:\Users\[userid]\Documents\CASTR Configs\Model 20220314.xlsx"
    globalFilePath = r"C:\Users\[userid]\Documents\CASTR Configs\Global_CASTR_Data_Jan_4.2.xlsx"
    castr_config_file_folder = r"C:\Users\[userid]\Documents\CASTR Configs\Configuration Files"
    self_service_template_file_folder = r"C:\Users\[userid]\Documents\CASTR Configs\Templates"
    file_correction_folder =  r"C:\Users\[userid]\Documents\CASTR Configs\Correction"
    #-- WALLE file documents management constants
    walle_UserGuide = r'[WALLE user guide](https://quip-amazon.com/hGRnADESQoMF/CASTR-Configuration-Tool-Python-Version)'
    walle_PythonCode = r'[WALLE latest version](https://amazon.awsapps.com/workdocs/index.html#/folder/425b350f47a9235503b525174cb911faca76da5864f5ea0a0039bde7041f502c)'



#-- ticket management constants
class ticket_management(enum.Enum):
    sim_link_castr = r'[Open a SIM ticket for CASTR](https://sim.amazon.com/issues/create?assignedFolder=c5049c4b-f31f-4e5a-9f10-feec7a86d25c)'
    sim_link_walle = r'[Open a SIM ticket for WALLE](https://issues.amazon.com/issues/create?assignedFolder=c5049c4b-f31f-4e5a-9f10-feec7a86d25c)'


