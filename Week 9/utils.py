import streamlit as st
# Initialize data storage
if "records" not in st.session_state:
    st.session_state.records = []

# Create form
with st.form("add_record"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["User", "Admin"])

if st.form_submit_button("Add Record"):
    record = {"name": name, "email": email, "role": role}
    st.session_state.records.append(record)
    st.success("Record added!")

# Display all records
if st.session_state.records:
    st.subheader("All Records")

    # Convert to DataFrame
    import pandas as pd
    df = pd.DataFrame(st.session_state.records)

    # Display interactive table
    st.dataframe(df, use_container_width=True)

    # Or use static table
    # st.table(df)
else:
    st.info("No records found")


# Select record to update
if st.session_state.records:
    names = [r["name"] for r in st.session_state.records]
    selected = st.selectbox("Select record", names)

    # Find index
    idx = names.index(selected)
    record = st.session_state.records[idx]

# Update form
with st.form("update_form"):
    new_email = st.text_input("Email", record["email"])
    new_role = st.selectbox("Role", ["User", "Admin"],
    index=0 if record["role"]=="User"else 1)

if st.form_submit_button("Update"):
    st.session_state.records[idx]["email"] = new_email
    st.session_state.records[idx]["role"] = new_role
    st.success("Record updated!")


# Select record to delete
if st.session_state.records:
    names = [r["name"] for r in st.session_state.records]
    to_delete = st.selectbox("Select record to delete", names
)

    # Confirmation and delete
    col1, col2 = st.columns([3, 1])

with col1:
    st.warning(f"Delete {to_delete}?")

with col2:
    if st.button("Delete", type="primary"):
        idx = names.index(to_delete)
        st.session_state.records.pop(idx)
        st.success("Record deleted!")
        st.rerun()
