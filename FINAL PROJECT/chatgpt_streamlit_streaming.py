import streamlit as st
from openai import OpenAI

def run_ai_chat(domain, model="gpt-4o", temperature=1.0):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def get_system_prompt(domain):
        if domain == "Cyber Incidents":
            return {
                "role": "system",
                "content": "You are a cybersecurity expert. Analyze incidents, threats, and vulnerabilities. Provide technical guidance using MITRE ATT&CK, CVE references. Prioritize actionable recommendations."
            }
        elif domain == "IT Tickets":
            return {
                "role": "system",
                "content": "You are an IT operations expert. Help troubleshoot issues, optimize systems, manage tickets, and provide infrastructure guidance. Focus on practical solutions."
            }
        else:
            return {
                "role": "system",
                "content": "You are a data science expert. Help with data analysis, visualization, statistical methods, and machine learning. Explain concepts clearly and suggest appropriate techniques."
            }

    if 'messages' not in st.session_state or not st.session_state.messages or st.session_state.get('ai_domain') != domain:
        st.session_state.messages = [get_system_prompt(domain)]
        st.session_state.ai_domain = domain

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Say something...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True
            )
        with st.chat_message("assistant"):
            container = st.empty()
            full_reply = ""
            for chunk in completion:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_reply += delta.content
                    container.markdown(full_reply + "▌")
            container.markdown(full_reply)
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_reply
        })
    with st.sidebar:
        st.subheader("Chat Controls")
        # Display message count
        message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
        st.metric("Messages", message_count)
        # Clear chat button
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        # Model selection
        model = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4o-mini"],
            index=0
        )
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Higher values make output more random"
        )
