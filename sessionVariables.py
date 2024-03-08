def resetUserSelection():
    # -- reset session variables
    st.session_state.gd_template = False
    st.session_state.gd_dataFactSources = False
    st.session_state.gd_template_dataFactSources = False
    st.session_state.gd_dataFacts = False
    st.session_state.gd_template_dataFacts = False
    st.session_state.gd_auditRules = False
    st.session_state.gd_template_auditRules = False
    st.session_state.gd_configurationDetails = False
    st.session_state.gd_check_datafacts = False
    st.session_state.gd_check_dataFactSources = False
    st.session_state.gd_check_auditRules = False
    st.session_state.gd_check_auditConfigurationDetails = False
    st.session_state.gd_conditionalTests = False
    st.session_state.gd_mr_auditTypes = False
    st.session_state.gd_mr_milestones = False

if "gd_template_dataFacts" not in st.session_state:
    st.session_state.gd_template_dataFacts = False
if "gd_dataFacts" not in st.session_state:
    st.session_state.gd_dataFacts = False
if "gd_template_dataFactSources" not in st.session_state:
    st.session_state.gd_template_dataFactSources = False
if "gd_dataFactSources" not in st.session_state:
    st.session_state.gd_dataFactSources = False
if "gd_template_auditRules" not in st.session_state:
    st.session_state.gd_template_auditRules = False
if "gd_auditRules" not in st.session_state:
    st.session_state.gd_auditRules = False
if "gd_template_configuationDetails" not in st.session_state:
    st.session_state.gd_template_configuationDetails = False
if "gd_configuationDetails" not in st.session_state:
    st.session_state.gd_configurationDetails = False
if "gd_template" not in st.session_state:
    st.session_state.gd_template = False
if "gd_check_datafacts" not in st.session_state:
    st.session_state.gd_check_datafacts = False
if "gd_check_dataFactSources" not in st.session_state:
    st.session_state.gd_check_dataFactSources = False
if "gd_check_auditRules" not in st.session_state:
    st.session_state.gd_check_auditRules = False
if "gd_check_auditConfigurationDetails" not in st.session_state:
    st.session_state.gd_check_auditConfigurationDetails = False
if "gd_conditionTests" not in st.session_state:
    st.session_state.gd_conditionalTests = False
if "gd_mr_auditTypes" not in st.session_state:
    st.session_state.gd_mr_auditTypes = False
if "gd_mr_milestones" not in st.session_state:
    st.session_state.gd_mr_milestones = True