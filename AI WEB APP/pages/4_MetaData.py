import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets, insert_ticket
from chatgpt_streamlit_streaming import run_ai_chat
import pandas as pd
import plotly.express as px

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Home.py")
    st.stop()

st.markdown("#### 📊 Data Science Dashboard")


ds = pd.read_csv("DATA/datasets_metadata.csv")  

total_datasets = len(ds)
size_count = (ds['size']).sum()  

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Datasets", total_datasets)
with col2:
    average_size = size_count / total_datasets if total_datasets > 0 else 0
    st.metric("Average Size", average_size)
with col3:
    analytics_count = 0
    if 'category' in ds.columns:
        analytics_count = (ds['category'].str.lower() == 'analytics').sum()
    st.metric("Analytics", analytics_count)
with col4:
    security_count = 0
    if 'category' in ds.columns:
        security_count = (ds['category'].str.lower() == 'security').sum()
    st.metric("Security", security_count)

st.markdown("---")

left_col, right_col = st.columns([2, 2])
with left_col:
    st.markdown("#### Datasets by Source")
    if 'source' in ds.columns:
        st.bar_chart(ds['source'].value_counts())
    else:
        st.info("No 'source' column in dataset.")

with right_col:
    if 'category' in ds.columns:
        import plotly.express as px
        category_counts = ds['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        fig = px.pie(
            category_counts,
            names='Category',
            values='Count',
            title='Datasets by Category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No 'category' column in dataset.")

col1, col2 = st.columns(2)
st.markdown("#### Metadata")
with st.form("add_metadata_form"):
        meta_name = st.text_input("Metadata Name", key="meta_name")
        meta_type = st.selectbox("Type", ["Image", "Text", "Tabular", "Audio"], key="meta_type")
        meta_status = st.selectbox("Status", ["Active", "Archived"], key="meta_status")
        meta_records = st.number_input("Records", min_value=0, key="meta_records")
        meta_submit = st.form_submit_button("Add Metadata")
if meta_submit and meta_name:
        st.success("Metadata added! (Implement insert_metadata in your backend)")
        st.experimental_rerun()

try:
        ds = pd.read_csv("DATA/datasets_metadata.csv")
        meta_names = ds["dataset"].tolist() if "dataset" in ds.columns else ds.index.astype(str).tolist()
        meta_to_delete = st.selectbox("Delete Metadata", meta_names, key="delete_metadata")
        if st.button("Delete Metadata", key="delete_metadata_btn"):
            st.success("Metadata deleted! (Implement delete_metadata in your backend)")
            st.experimental_rerun()
except Exception:
        st.info("No metadata to delete or file not found.")

st.divider()
st.dataframe(ds, use_container_width=True)
st.divider()
st.title("Data Science AI Chat")
run_ai_chat("Data Science")
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