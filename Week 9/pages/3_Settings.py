import streamlit as st
from auth import change_password

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()

st.title("Settings")

st.header("Change Password")

if "username" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("You must be logged in to change your password.")
    st.stop()

with st.form("change_password_form"):
    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    submitted = st.form_submit_button("Change Password")

if submitted:
    if not old_password or not new_password or not confirm_password:
        st.warning("Please fill in all fields.")
    elif new_password != confirm_password:
        st.error("New passwords do not match.")
    else:
        username = st.session_state.get("username", "")
        success, msg = change_password(username, old_password, new_password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

if st.session_state.logged_in:
    with st.sidebar:
        username = st.session_state.get("username", "")
        role = st.session_state.get("role", "")
       
        st.markdown(f"**Logged in as:** {username}")
        st.markdown(f"**Role:** {role}")

        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.info("You have been logged out")
            st.switch_page("Home.py")