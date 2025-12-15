import streamlit as st
from app.data.tickets import get_all_tickets

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()

# Page title
st.title("🎫 IT Tickets Analytics")

# Get tickets data
tickets = get_all_tickets()  # Should return a pandas DataFrame

# Calculate metrics
total_tickets = len(tickets)
open_count = (tickets['status'] == 'open').sum()
in_progress_count = (tickets['status'] == 'in-progress').sum()
closed_count = (tickets['status'] == 'closed').sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
        st.metric("Total Tickets", total_tickets)
with col2:
        st.metric("Open", open_count)
with col3:
        st.metric("In Progress", in_progress_count)
with col4:
        st.metric("Closed", closed_count)

st.markdown("---")
# Section: Tickets by Priority and Status
col_pri, col_stat = st.columns(2)
with col_pri:
        st.markdown("#### Tickets by Priority")
        desired_priorities = ["low", "medium", "high", "urgent"]  # Only show these
        priority_counts = tickets['priority'].value_counts()
        priority_counts = priority_counts[priority_counts.index.isin(desired_priorities)]
        st.bar_chart(priority_counts)

with col_stat:
        st.markdown("#### Tickets by Status")
        # Drop rows where status is exactly 'Open' (capital O)
        tickets_filtered = tickets[tickets['status'] != 'Open']
        st.bar_chart(tickets_filtered['status'].value_counts())


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
