# Import Streamlit and ticket management functions
import streamlit as st
from app.data.db import connect_database
from datetime import datetime
from app.data.db import connect_database
from app.data.tickets import get_all_tickets, insert_ticket, update_ticket_status, delete_ticket



# Only allow access if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()

# Connect to the database for ticket operations
conn = connect_database('DATA/intelligence_platform.db')

# Page title
st.title("🎫 IT Tickets Dashboard")



# Get all tickets to display
tickets = get_all_tickets()
st.divider()
st.dataframe(tickets, use_container_width=True)


st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Tickets")
    with st.form("new_ticket"):
        id = st.text_input("Ticket ID")
        title = st.text_input("Title")
        priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
        status = st.selectbox("Status", ["open", "in progress", "resolved", "closed"])

        submitted = st.form_submit_button("Add Ticket")


        # Add a new ticket if the form is submitted
        if submitted:
            created_date = datetime.now().strftime("%Y-%m-%d")
            insert_ticket(id, title, priority, status, created_date) 
            st.success("✓ Ticket added successfully!")
            st.rerun()

with col2:
        # Updating ticket status
        st.markdown("Update Ticket")
        with st.form("update_ticket_status"):
                ticket_ids = tickets['id'].tolist()
                selected_id = st.selectbox("Select Ticket ID", ticket_ids)
                new_status = st.selectbox("New Status", ["open", "in progress", "resolved", "closed"])
                update_submitted = st.form_submit_button("Update Ticket Status")
                if update_submitted:
                        update_ticket_status(selected_id, new_status)
                        st.success(f"✓ Ticket {selected_id} status updated to '{new_status}'!")
                        st.rerun()

# Deleting a ticket 
st.markdown("Delete Tickets")
with st.form("delete_ticket_form"):
        ticket_ids = tickets['id'].tolist()
        del_id = st.selectbox("Select Ticket ID to Delete", ticket_ids)
        del_submitted = st.form_submit_button("Delete Ticket")
        if del_submitted:
                delete_ticket(del_id)
                st.success(f"✓ Ticket {del_id} deleted!")
                st.rerun()




st.divider()




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


