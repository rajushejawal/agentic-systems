import streamlit as st
import requests

# Configure page layout and visual anchors
st.set_page_config(page_title="Cred Support Portal", page_icon="🏦", layout="centered")
st.title("🏦 Cred Operations & Support Agent")

# Sidebar - Made completely generic with no default record ID
st.sidebar.header("Account Parameters")
record_id = st.sidebar.text_input(
    "Target Loan Record ID", 
    value="", 
    placeholder="e.g., CRED-LN-1001"
).strip()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past chat conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle live multi-turn user query submission
if user_query := st.chat_input("Ask a policy question..."):
    # 1. Enforce validation checkpoint right at the UI layer
    if not record_id:
        st.error("❌ Action Required: Please enter a valid Target Loan Record ID in the sidebar before asking your question.")
    else:
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        backend_url = "http://127.0.0.1:8090/ask"  # Ensure this matches the FastAPI endpoint
        payload = {"query": user_query, "record_id": record_id}

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = requests.post(backend_url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        result_text = f"**Policy Response:** {data['policy_response']}"
                        st.write(result_text)
                        st.session_state.messages.append({"role": "assistant", "content": result_text})
                    
                    elif response.status_code == 404:
                        error_msg = f"❌ Record Not Found: The ID `{record_id}` does not exist in the ledger database."
                        st.error(error_msg)
                    
                    else:
                        st.error(f"Backend Server Error: Received Status Code {response.status_code}")
                
                except Exception as e:
                    st.error(f"Unable to connect to the FastAPI gateway: {str(e)}")
