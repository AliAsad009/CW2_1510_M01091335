import streamlit as st
import os
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets, insert_ticket
from app.data.users import get_all_users

from auth import register_user, login_user, user_exists, validate_password, validate_username


# Set up Streamlit page configuration
st.set_page_config(page_title="Login / Register", page_icon="🔑 ", layout="centered")

# Initialize session state variables if not already set
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.logged_in:
    with st.sidebar:
        username = st.session_state.get("username", "")
        role = st.session_state.get("role", "")
        st.markdown(f"**Logged in as:** {username}")
        st.markdown(f"**Role:** {role}")

        if st.button("Log out"):
            # Clear session state on logout
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.info("You have been logged out")
            st.switch_page("Home.py")
    # Fetch data for dashboard metrics
    incidents = get_all_incidents()
    tickets = get_all_tickets()
    users = get_all_users()
    total_users = len(users)
    incidents = len(incidents)
    it_tickets = len(tickets)
    users_delta = "+50"
    incidents_delta = "-12"
    tickets_delta = "+18"

    st.markdown("## Multi-Domain Intelligence Platform")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", total_users, users_delta)
    with col2:
        st.metric("Incidents", incidents, incidents_delta)
    with col3:
        st.metric("IT Tickets", it_tickets, tickets_delta)

    st.markdown("---")
    st.markdown("### Pages Navigation")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.page_link("pages/1_Dashboard.py", label="Dashboard")
    with col_b:
        st.page_link("pages/2_Analytics.py", label="Analytics")
    with col_c:
        st.page_link("pages/3_Settings.py", label="Settings")
    st.stop() # Don’t show login/register

st.title("Login / Register")
# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])
# ----- LOGIN TAB -----

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log in", type="primary"):
        if not login_username or not login_password:
            st.warning("Please fill in all fields.")
        elif login_user(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            # Find user role from users.txt after successful login
            users_txt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "users.txt"))
            role = ""
            try:
                with open(users_txt_path, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = [p.strip().strip("'\"") for p in line.strip().split(",")]
                        # Only assign role if username matches and role is valid
                        if len(parts) >= 3 and parts[0] == login_username:
                            role_candidate = parts[2]
                            if role_candidate.lower() in ["user", "admin", "analyst", "manager"]:
                                role = role_candidate
                                break
            except Exception:
                pass
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid username or password.")



# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    role = st.selectbox("Select role", ["user", "admin", "analyst", "manager"], key="register_role")

    if st.button("Create account"):
        if not new_username or not new_password or not confirm_password or not role:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            valid_user, user_msg = validate_username(new_username)
            valid_pass, pass_msg = validate_password(new_password)
            if not valid_user:
                st.error(user_msg)
            elif not valid_pass:
                st.error(pass_msg)
            elif user_exists(new_username):
                st.error("Username already exists. Choose another one.")
            else:
                # Register the new user with the selected role
                registered = register_user(new_username, new_password, role)
                if registered:
                    st.success("Account created! You can now log in from the Login tab.")
                    st.info("Tip: go to the Login tab and sign in with your new account.")
                else:
                    st.error("Registration failed. Please try again.")



