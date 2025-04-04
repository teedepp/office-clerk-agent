import streamlit as st
import requests

st.title("Leave & Certificate Request System with Multi-Agent AI")

st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose a Page",
    ["Submit Leave Request", "View Leave Requests", "Request Certificate", "Download Certificate", "AI Assistant", "Agent Status"]
)


user_query = st.text_input("Ask me anything related to leaves or certificates:")

if st.button("Ask"):
    if user_query:
        response = requests.post("http://127.0.0.1:8000/generate-response/", json={"query": user_query})
        if response.status_code == 200:
            st.write(f"**AI Response:** {response.json()['response']}")
        else:
            st.error("Error getting response from AI model")


# Submit Leave Request
if page == "Submit Leave Request":
    st.header("Submit a Leave Request")
    employee_id = st.text_input("Employee ID")
    leave_type = st.selectbox("Leave Type", ["Casual", "Sick", "Annual"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    reason = st.text_area("Reason")

    if st.button("Submit"):
        response = requests.post("http://127.0.0.1:8000/request_leave/", json={
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "reason": reason
        })
        if response.status_code == 200:
            st.success("Leave request submitted successfully!")
        else:
            st.error("Error submitting leave request")

# View Leave Requests
elif page == "View Leave Requests":
    st.header("Leave Requests")
    response = requests.get("http://127.0.0.1:8000/leave_requests/")
    if response.status_code == 200:
        data = response.json()["data"]
        for leave in data:
            st.write(f"**Employee ID:** {leave['employee_id']}")
            st.write(f"**Leave Type:** {leave['leave_type']}")
            st.write(f"**Start Date:** {leave['start_date']}")
            st.write(f"**End Date:** {leave['end_date']}")
            st.write(f"**Reason:** {leave['reason']}")
            st.write("---")
    else:
        st.error("Error fetching leave requests.")

# Request Certificate
elif page == "Request Certificate":
    st.header("Request a Certificate")
    student_id = st.text_input("Student ID")
    certificate_type = st.selectbox("Certificate Type", ["Bonafide", "NOC"])

    if st.button("Request Certificate"):
        response = requests.post("http://127.0.0.1:8000/generate_certificate/", json={
            "student_id": student_id,
            "certificate_type": certificate_type
        })
        if response.status_code == 200:
            st.success("Certificate request submitted successfully!")
        else:
            st.error("Error submitting certificate request")

# Download Certificate
elif page == "Download Certificate":
    st.header("Download Certificate")
    certificate_id = st.number_input("Enter Certificate ID", min_value=1, step=1)

    if st.button("Download"):
        response = requests.get(f"http://127.0.0.1:8000/download_certificate/{certificate_id}")
        if response.status_code == 200:
            st.success("Certificate downloaded successfully!")
        else:
            st.error("Error downloading certificate")

# AI Assistant with Multi-Agent Support
elif page == "AI Assistant":
    st.header("AI Assistant - Multi-Agent Query System")

    user_prompt = st.text_area("Enter your query:")
    selected_agent = st.selectbox("Select Agent", ["General AI", "Leave Request Agent", "Certificate Agent"])

    agent_map = {
        "General AI": "general_ai",
        "Leave Request Agent": "leave_agent",
        "Certificate Agent": "certificate_agent"
    }

    if st.button("Get Response"):
        response = requests.post("http://127.0.0.1:8000/generate-response/", json={
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": 150,
            "agent": agent_map[selected_agent]
        })
        
        if response.status_code == 200:
            st.write("AI Response:", response.json().get("response", "No response received"))
        else:
            st.error(f"Error getting response from AI model: {response.text}")

# Agent Status Page
elif page == "Agent Status":
    st.header("Agent Status")
    
    response = requests.get("http://127.0.0.1:8000/agents-status")
    if response.status_code == 200:
        agent_status = response.json()
        st.write("### Registered Agents:")
        for agent, status in agent_status.items():
            st.write(f"**{agent}**: {'✅ Running' if status else '❌ Not Running'}")
    else:
        st.error("Error fetching agent status.")
