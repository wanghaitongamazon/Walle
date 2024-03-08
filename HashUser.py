import streamlit_authenticator as stauth
import streamlit as st

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

st.write(hashed_passwords)
