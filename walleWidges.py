def status_widget(header, sub_header, key):
    if (header !=""):
        st.header(header)
    if(sub_header !=""):
        st.subheader(sub_header)
    if(key !=""):
        st.markdown(key)

def link_widget(key, title):
    if (title !=""):
        st.subheader(title)
    st.markdown(key, unsafe_allow_html=True)

def info_widget(key, title, type, place = ''):
    if type == 'info':
        if(place == 'side bar'):
            st.sidebar.info(title)
        else: 
            st.info(title)
    elif type == 'error':
        st.error(title)
    elif type == 'success':
        st.success(title)

def input_widget(label, key):
    return st.text_input(label, value =  key)

def radio_widget(label, lists, indexSelected, key):
    return st.radio(label, lists, index=indexSelected, key=key)

def button_widget(key, title):
    if( title == 'Save'):
        return st.button(label=title, key=key)
    if( title == 'Download'):
        return st.download_button(label=title, key=key)