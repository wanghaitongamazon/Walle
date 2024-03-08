dashboard_selection_mode = option_menu(
    menu_title= "",
    options= ['CASTR Audits', 'Test Score Impact Analysis', 'CASTR Metrics' ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if dashboard_selection_mode == 'CASTR Audits':

    lst = ["1. **" + quickSightAllCastrAuditslink + "** - view CASTR audits by country, owner, carrier, audit type, business or milestone.", "2. **" + quickSightPTOPlannerlink + "** - view CASTR audits by country, owner, carrier, audit type, business, milestone, cap remediator, level 1 reviewer, level 2 reviewer done date, preparer and executor.", "3. **" + quickSightAllCASTRCAPslink + "** - view CASTR audits by country, owner, audit type, business, milestone and CAP status", 
            "4. **" + quickSightCASTRAdoptionlink + "** - view CASTR audit metrics and test level metrics", "5. **" + quickSightMyAuditslink + "** - view CASTR audit by owner, cap remediator, executor or milestone"]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)
    
elif dashboard_selection_mode == 'Test Score Impact Analysis':
    
    st.subheader("Introduction")
    st.markdown("The purpose of the document is to provide notes on SOP to use QuickSight dashboard to perform audit score impact analysis which is used during change management process. The impact analysis uses three key values, ")
    lst = ["1) CASTR tests," ,"2) CASTR test existing weightage scale,", "3) New test weightage scale (change in value). The new test weightage scale is used on the historic test audit results (Pass / Fail / Not applicable) to know the new audit score based on the new test weightage scale provided."]
    s =''
    for i in lst:
        s += "- " + i + "\n"

    st.markdown(s)

    st.markdown("This new audit score is then compared with the CASTR previous (old) audit score to know the change in audit score. This will provide the impact of the changes proposed.")

    st.markdown("**SOP, Wiki and Dashboard link**")
    lst = ["1. **" + testImpactAnalysisSOPlink + "** :point_left:", "2. **" + testImpactAnalysisWikilink + "** :point_left:", "3. **" + quickSightTestScoreImpactAnalysisInputFilePrerequisitelink + "** :point_left:", "4. **" + quickSightTestScoreImpactAnalysislink + "** :point_left:"]
    s ='' 
    for i in lst:
        s += "- " + i + "\n"
    st.markdown(s)

elif dashboard_selection_mode == 'CASTR Metrics':
    lst = ["1. **" + quickSightCASTRTestAspectlink + "** - view how many test aspects, tests by country, business, audit type and entity in most recent config file or since CASTR inception. ", 
            "2. **" + quickSightCASTRTestAspectDetaillink + "** - view test and test aspects by by country, business, audit type, section, topic in most recent config file or since CASTR inception.", 
            "3. **" + quickSightCastrWWMetricslink + "** -- view CASTR WW(adopted) metrics for WBR including total completed audits, total counties, total country program, total country program audittype, total new audits, total use in roles"]
    s =''
    for i in lst:
        s += "- " + i + "\n" 

    st.markdown(s)