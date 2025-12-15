# Import Streamlit and Week 8 functions
import streamlit as st
from app.data.db import connect_database
from datetime import datetime
from openai	import OpenAI
import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_tickets, insert_ticket, update_ticket_status, delete_ticket
from chatgpt_streamlit_streaming import run_ai_chat


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()



# Connect to database (Week 8 function)
conn = connect_database('DATA/intelligence_platform.db')

# Page title
st.title("🎫 IT Tickets Dashboard")


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


        if submitted:
            created_date = datetime.now().strftime("%Y-%m-%d")
            insert_ticket(id,title,priority,status,created_date) 
            st.success("✓ Ticket added successfully!")
            st.rerun()

with col2:
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

st.markdown("Delete Tickets")
with st.form("delete_ticket_form"):
        ticket_ids = tickets['id'].tolist()
        del_id = st.selectbox("Select Ticket ID to Delete", ticket_ids)
        del_submitted = st.form_submit_button("Delete Ticket")
        if del_submitted:
                delete_ticket(del_id)
                st.success(f"✓ Ticket {del_id} deleted!")
                st.rerun()



st.title("IT Tickets AI Chat")
run_ai_chat("IT Tickets")
st.divider()


#Initialize OpenAI client
client	= OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#Page configuration
st.set_page_config(
        page_title="ChatGPT Assistant",
        page_icon="💬",
        layout="wide"
)

# Store chat messages in session state
if 'messages' not in st.session_state:
        st.session_state.messages = []

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


