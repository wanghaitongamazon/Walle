castr_rule_input_component_format =  " CASTR Rule - 1> when InputComponent is Boolean, inputFormatValues must be 'Yes, No'; 2> when InputComponent is Categorical, inputFormatValues must have more than one item and seperated by comma. "

castr_rule_input_component_rule =  " CASTR Rule - 1> Must have a value, can not be blank; 2> must be one of String, Boolean, Categorical, Number or Percentage; "

castr_rule_modifyDeleteNew = " CASTR Rule - 1> Mark 'D' or 'd' to delete a row;  2> Mark 'N' or 'n' to add a new row ; 3> Mark 'M' or 'm' to  update a row; 4> Leave blank if no change; 5> 'S' is a reserved row in CASTR- do not change or delete."

castr_rule_sectionID = " CASTR Rule - 1> Must be upper case; 2> Format must be location_business_section, example, location = US, business = middle mile, section =Carrier Licensing,  sectionID = US_MM_CL; 3> Each section must has a unique section ID under same business and audit type; 4> Contains no whitespace. "
castr_rule_section = " CASTR Rule - 1> Must have a value; 2> For existing section, value must be case propered; 3> If this is a new sction, it must get CMC approval first. "

castr_rule_topic = " CASTR Rule - 1> Must have a value; 2> For existing topic, value must be case propered; 3> If this is a new sction, it must get CMC approval first. "
castr_rule_controlID = " CASTR Rule - 1>Must have a value; 2> Must be uppercase; 3> Contains no whitespace; 4> Each topic must has a unique control ID under same business and audit type."

castr_rule_test = " CASTR Rule - 1> Must have a value, can not be blank "
castr_rule_testID = " CASTR Rule - 1>Must have a value; 2> Must be uppercase; 3> Contains no whitespace; 4> Each topic must has a unique test ID under same business, audit type and topic."

castr_rule_calculate_test_aspect = " CASTR Rule - 1> FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number) either both of them are blank or both of them have value at same time."

castr_rule_document = " CASTR Rule - 1> Must have a value, can not be blank; 2> must less than 250 characters; 3> must be 'Calculated' only when both FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number) have non blank value."

castr_rule_fact_operator = " CASTR Rule - 1> Must be blank when both FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number) are blank; 2> Must be '-' when both FactName_1 (Later Date/Larger Number) and FactName_2 (Earlier Date/Smaller Number) are blank."

castr_rule_value = " CASTR Rule - 1> Must have a value, can not be blank. 2> must be a numeric value when inputComponent is Number or Percentage. "

castr_rule_operator = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be one of  '=', '<', '>', '<=' or '>=' when inputComponent is Number or Percentage."

walle_rule_calculate = "WALLE does not support converting an existing calculate test aspect to an non calculate test aspect or convert non calculate test aspect to a calculate test aspect.  1> Must mark D or d on column ModifyDeleteNew for existing test aspect; 2> Insert a new row and fill in new values in each column; 3> Must mark N or n on column ModifyDeleteNew for the new inserted test aspect "

castr_rule_scoringMethodology = " CASTR Rule - 1> scoringMethodologyId must be bottom_up_weights, can not be blank; 2> riskPointsTest must be a numeric value, can not be blank. "

castr_rule_aspectId = " CASTR Rule - 1> aspectId must have a valid value for row(s) where ModifyDeleteNew equal to  D/d or M/m; 2> aspectId must have a blank value for row(s) where ModifyDeleteNew equal to 'N'; 3> aspectId must be unique for same business and audit type; 4> same aspectId can not be used in more than one row where ModiyDeleteNew equals to M/m or D/d.  "

castr_rule_displayOrder = " CASTR Rule - 1> displayOrder fields must be valid numeric characters; 2> topic_displayOrder and test_displayOrder value must be a 2 digits numeric characters and between 01 and 99; 3> aspect_displayOrder must be a 3 numeric characters and between 001 and 999; 4> displayOrder must be unique under same business. "

castr_rule_capId = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be a valid value from global file. "

castr_rule_business = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must in the format, example LastMile-DSP-1.0  or LastMile-DSP-WagonWheel.  "

castr_rule_entity = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be one of Employee or Carrier. "

castr_rule_riskProfileId = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be a valid value from global file. If you need help, please contact TAP team."

castr_rule_milestoneConfigurationProfileId = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be a valid value from global file. If you need help, please contact TAP team."

castr_rule_reviewErrorProfileId = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be a valid value from global file. If you need help, please contact TAP team."

castr_rule_userRoleConfigurationProfileId = " CASTR Rule - 1> Must have a value, can not be blank; 2> Must be a valid value from global file. If you need help, please contact TAP team."

castr_rule_tagConfigurationProfileId = " CASTR Rule - If this feature is enabled in a region, column tagProfileId can not be blank and must have a valid id from CASTR global file. If you need help with tagConfigurationProfileId value, please contact TAP team."

castr_rule_fact_document = " CASTR Rule - 1> Must have a value, can not be blank; 2> must less than 250 characters. "

castr_rule_scoringMethodologyId = " CASTR Rule - 1> If this feature is enabled in a region, this field can not be blank and must be a value from global file. If you need help with scoringMethodologyId value, please contact TAP team. 2> If this feature is not enabled in a region, this filed must be blank. "

castr_rule_correctiveActionsSLAExclusionsProfileId = " CASTR Rule - 1> If this feature is enabled in a region, this filed can not be blank and must be a value from global file. If you need help with correctiveActionsSLAExclusionsProfileId value, please contact TAP team. 2> If this feature is not enabled in a region, this filed must be blank. "