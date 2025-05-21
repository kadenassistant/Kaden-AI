import os
import pickle
import base64
import email
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail read-only permission
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail(account_name):
    token_path = f'tokens/{account_name}.pickle'

    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_recent_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')

        parts = payload.get('parts', [])
        body = ""
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body_data = part['body']['data']
                    body += base64.urlsafe_b64decode(body_data.encode('ASCII')).decode('utf-8', errors='ignore')
        else:
            body_data = payload.get('body', {}).get('data')
            if body_data:
                body += base64.urlsafe_b64decode(body_data.encode('ASCII')).decode('utf-8', errors='ignore')

        emails.append({
            'subject': subject,
            'from': sender,
            'body': body
        })

    return emails
