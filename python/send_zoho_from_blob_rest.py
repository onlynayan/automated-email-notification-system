import requests
import urllib3
import base64
import tempfile
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------
# APEX REST API Endpoints
# -----------------------------
API_LIST_URL = "https://your_apex_server/ords/schema/email_blob/getAll"
API_FILE_URL = "https://your_apex_server/ords/schema/email_blob/getAttachment/"

# -----------------------------
# ZOHO MAIL CONFIG
# -----------------------------
ZOHO_CLIENT_ID = "write_your_zoho_client_id_here"
ZOHO_CLIENT_SECRET = "write_your_zoho_client_secret_here"
ZOHO_REFRESH_TOKEN = "write_your_zoho_refresh_token_here"
ZOHO_ACCOUNT_ID = "write_your_zoho_account_id_here"
ZOHO_FROM_ADDRESS = "your_mailbox@zohomail.com"


# -----------------------------
# Get Zoho Access Token
# -----------------------------
def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    resp = requests.post(url, data=data)
    return resp.json().get("access_token")


# -----------------------------
# Fetch Metadata
# -----------------------------
def fetch_emails():
    resp = requests.get(API_LIST_URL, verify=False)
    return resp.json().get("items", [])


# -----------------------------
# Fetch BLOB File
# -----------------------------
def fetch_attachment(id_value):
    resp = requests.get(API_FILE_URL + str(id_value), verify=False)
    data = resp.json()

    if not data:
        return None, None, None

    # ORDS returns BLOB as base64
    base64_data = data.get("attachment_blob")
    mime_type = data.get("attachment_mimetype")
    filename = data.get("attachment_filename")

    if not base64_data:
        return None, None, None

    file_bytes = base64.b64decode(base64_data)
    return filename, mime_type, file_bytes


# -----------------------------
# Send Email with Attachment
# -----------------------------
def send_email_with_attachment(access_token, item):
    url = f"https://mail.zoho.com/api/accounts/{ZOHO_ACCOUNT_ID}/messages"

    # Fetch attachment bytes
    filename, mimetype, file_bytes = fetch_attachment(item["id"])

    # Build email body
    body = {
        "fromAddress": ZOHO_FROM_ADDRESS,
        "toAddress": item["email"],
        "ccAddress": item.get("cc") or "",
        "bccAddress": item.get("bcc") or "",
        "subject": item.get("subject") or "",
        "content": item.get("message") or "",
        "mailFormat": "html",
    }

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    # If no attachment, send normal email
    if not file_bytes:
        resp = requests.post(url, headers=headers, data=body)
        print(resp.status_code, resp.text)
        return

    # Write file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(file_bytes)
        temp_path = tmpfile.name

    # Prepare multipart files
    files = {
        "attachments": (filename, open(temp_path, "rb"), mimetype)
    }

    resp = requests.post(url, headers=headers, data=body, files=files)

    print(resp.status_code, resp.text)

    # Clean up temp file
    os.remove(temp_path)


# -----------------------------
# MAIN EXECUTION
# -----------------------------
def main():
    access_token = get_access_token()
    emails = fetch_emails()

    if not emails:
        print("No rows found.")
        return

    for item in emails:
        send_email_with_attachment(access_token, item)


if __name__ == "__main__":
    main()
