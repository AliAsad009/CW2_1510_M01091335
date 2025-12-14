
# Import Streamlit and Week 8 functions
import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident
from datetime import datetime
from app.data.incidents import update_incident_status

import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets, insert_ticket
from chatgpt_streamlit_streaming import run_ai_chat
import altair as alt
import plotly.express as px


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="Incidents", page_icon="📊", layout="wide")
conn = connect_database('DATA/intelligence_platform.db')


# Section: Cybersecurity Dashboard
st.markdown("#### 🛡️ Cybersecurity Dashboard")
incidents = get_all_incidents()  
incidents = incidents[~incidents['severity'].isin(['Low', 'High'])]
# Remove rows where status is exactly 'Open' (capital O)
incidents = incidents[incidents['status'] != 'Open']

# Calculate metrics
total_incidents = len(incidents)
critical = (incidents['severity'] == 'critical').sum()
high = (incidents['severity'] == 'high').sum()
open = (incidents['status'] == 'open').sum()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Incidents", total_incidents)
with col2:
    st.metric("Critical", critical)
with col3:
    st.metric("High", high)
with col4:
    st.metric("Open", open)

# Section: Incidents by Severity and Status
col_sev, col_stat = st.columns(2)
with col_sev:
    st.markdown("#### Incidents by Severity")
    st.bar_chart(incidents['severity'].value_counts())

with col_stat:
    st.markdown("#### Incidents by Status (Pie Chart)")
    status_counts = incidents['status'].value_counts()
    fig = px.pie(
        names=status_counts.index,
        values=status_counts.values,
        color=status_counts.index,
        color_discrete_map={
            "open": "#636EFA",
            "in-progress": "#EF553B",
            "resolved": "#00CC96",
            "closed": "#AB63FA"
        }
    )
    st.plotly_chart(fig, use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    with st.form("new_incident"):
        st.markdown("#### Add New Incident")
        title = st.text_input("Incident Title")
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        status = st.selectbox("Status", ["open", "in progress", "resolved"])
        submitted = st.form_submit_button("Add Incident")
    if submitted and title:
        insert_incident(conn, title, severity, status)
        st.success("✓ Incident added successfully!")
        st.experimental_rerun()
with col2:
    with st.form("update_incident_status"):
        st.markdown("#### Update Incident Status")
        incident_ids = incidents['id'].tolist()
        selected_id = st.selectbox("Select Incident ID", incident_ids)
        new_status = st.selectbox("New Status", ["open", "in-progress", "resolved", "closed"])
        update_submitted = st.form_submit_button("Update Status")
    if update_submitted:
        from app.data.incidents import update_incident_status
        update_incident_status(selected_id, new_status)
        st.success(f"✓ Incident ID {selected_id} status updated to {new_status}!")
        st.experimental_rerun()

    if update_submitted:
        update_incident_status(selected_id, new_status)
        st.success(f"✓ Incident ID {selected_id} status updated to {new_status}!")
        st.experimental_rerun()  # Refresh to show updated status

# DELETE: Delete incident
st.markdown("---")
st.subheader("Delete Incident")
incident_ids = incidents['id'].tolist() if 'id' in incidents.columns else []
if incident_ids:
    with st.form("delete_incident_form"):
        delete_id = st.selectbox("Select Incident ID to Delete", incident_ids, key="delete_incident_id")
        delete_submitted = st.form_submit_button("Delete Incident")
    if delete_submitted:
        from app.data.incidents import delete_incident
        delete_incident(delete_id)
        st.success(f"Incident {delete_id} deleted!")
        st.experimental_rerun()

st.dataframe(incidents, use_container_width=True) # ← Streamlit creates UI


st.header("Security Analysis")
    # Get incidents data from database
incidents_df = get_all_incidents()




st.markdown("""
    <style>
    .wide-btn .stButton > button {
        width: 100%;
        min-width: 160px;
        font-size: 1.1em;
        padding: 0.6em 0;
    }
    </style>
    """, unsafe_allow_html=True)
btn_col1, btn_col2, _ = st.columns([2,2,6])
chart_type = "bar"
with btn_col1:
        if st.button("Show Bar Chart", key="bar_btn", help="Show bar chart", use_container_width=True):
            chart_type = "bar"
with btn_col2:
        if st.button("Show Line Chart", key="line_btn", help="Show line chart", use_container_width=True):
            chart_type = "line"

threat_counts = incidents_df['incident_type'].value_counts()
chart_data = threat_counts.reset_index()
chart_data.columns = ['Type', 'Count']
chart_col, chart_spacer = st.columns([2, 5])
with chart_col:
        st.markdown("### Incidents by type")
        if chart_type == "bar":
            bar_chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('Type:N', axis=alt.Axis(labelAngle=45)),
                y='Count:Q'
            ).properties(width=500, height=400)
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            line = alt.Chart(chart_data).mark_line().encode(
                x=alt.X('Type:N', axis=alt.Axis(labelAngle=45)),
                y='Count:Q'
            ).properties(width=500, height=400)
            points = alt.Chart(chart_data).mark_point(filled=True, size=100, color='orange').encode(
                x=alt.X('Type:N'),
                y='Count:Q'
            ).properties(width=500, height=400)
            st.altair_chart(line + points, use_container_width=True)


st.divider()




st.title("Cyber Incidents AI Chat")
run_ai_chat("Cyber Incidents")


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