import streamlit as st
from gmail_ingest import authenticate_gmail, fetch_recent_emails
from summarizer import summarize_email

st.set_page_config(page_title="Kaden AI Assistant", layout="centered")
st.title("📬 Kaden — Your AI Email Assistant")

st.markdown("Connect to your Gmail account, and Kaden will fetch and summarize your latest emails.")

# Input your unique label for each Gmail account
account_name = st.text_input("Enter a name for this Gmail account (e.g., personal, work):")

if st.button("Connect & Summarize Emails"):
    if not account_name:
        st.error("Please enter a name for this account.")
    else:
        with st.spinner("Authenticating and fetching emails..."):
            try:
                service = authenticate_gmail(account_name)
                emails = fetch_recent_emails(service)
                if emails:
                    for i, email in enumerate(emails):
                        st.subheader(f"Email #{i+1}: {email['subject']}")
                        st.markdown(f"**From:** {email['from']}")
                        summary = summarize_email(email['body'])
                        st.markdown(f"**Kaden's Summary:** {summary}")
                else:
                    st.warning("No emails found.")
            except Exception as e:
                st.error(f"Error: {e}")
