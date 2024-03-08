#-- class to apply CASTR rules
class ruleDefiner():
    def _init_(self ):
        self.sectionId = ""
        self.location = ""
        self.mile = ""
        self.type = ""
        self.mileShort =""
        self.ruleIdPrefix = ""

    def rule_id_prefix(self, business):
        self.getBusinessMileType(business)
        tmp = self.location + "_" + self.mileShort + "_" + self.type + "_"
  
        self.ruleIdPrefix =  tmp[0].replace(" ", "_").replace('.', '')

    def rule_sectionId(self, section):
        self.sectionId =  + "_" + self.getFirstLetter(section)

    def getBusinessMileType(self, text_to_split):
        words = text_to_split.split("-")

        self.mile = words[0]
        if self.mile == "LastMile":
            self.mileShort = "LM"
        else:
            self.mileShort = "MM"

        if len(words) > 2:
            self.type = words[2]
        else:
            self.type = words[1]
    
    def getFirstLetter(self, text_to_split):    
        # Use split to break the string into words 
        words = text_to_split.split() 
        
        # Get the first letter of each word 
        first_letters = [word[0] for word in words] 
        return first_letters

    def createDisplayorder(self, df, field_name, df_detail):

        if df_detail is not None:
            where1 = df_detail['aspectId'] == ""
            df_chk = pd.merge( df_detail, df[[field_name, 'id']][~where1], how="left", left_on=['aspectId'], right_on='id')
        else:
            df_chk = df  

        df_chk.displayOrder = pd.to_numeric(df_chk.displayOrder, errors='coerce')
        df_chk = df_chk.sort_values('displayOrder')

        tmp_df_Order = pd.DataFrame()
        displayOrder = 0

        #-- st.write(df_chk,unsafe_allow_html=True)
        for ind in df_chk.index:
            if displayOrder == 0 :

                displayOrder = displayOrder + 1
                data = [[df_chk[field_name][ind], "{:03d}".format(displayOrder)]]

                tmp_df_Order = pd.DataFrame(data, columns=[field_name, 'displayOrder'])
            else:
                #-- st.write(df_chk[field_name][ind],unsafe_allow_html=True)
                where1 = df_chk[field_name][ind] == tmp_df_Order[field_name]
                df_1 = tmp_df_Order[where1]
                if len(df_1) == 0:    
                    displayOrder = displayOrder + 1
                    df_tmp = pd.DataFrame({field_name: [df_chk[field_name][ind]], 'displayOrder': ["{:03d}".format(displayOrder)]})               
                       
                    tmp_df_Order = pd.concat([tmp_df_Order, df_tmp], ignore_index=True)  
        return tmp_df_Order
