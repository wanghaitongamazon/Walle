#-- WALLE page title
st.set_page_config(
    page_title="WALLE",
    page_icon=imag_icon,
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'About': "WALLE Configuration Tool version 4.0"
    }
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)