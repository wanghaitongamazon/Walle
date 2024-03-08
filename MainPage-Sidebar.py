with st.sidebar.container():
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'sidebar')
    
# ---- side bar ----
st.sidebar.image(imag_icon, use_column_width=True)
with st.sidebar:        
    selected = option_menu(
        menu_title= "Main Menu",
        options= user_permit.actions,
        menu_icon="cast",
        default_index=0,
        icons=['emoji-smile','cloud-download','filetype-xlsx','filetype-xlsx','cloud-upload','stack','link','link','link','activity','link']
    )