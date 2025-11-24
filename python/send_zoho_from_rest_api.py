import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# APEX REST API endpoint
API_URL = os.getenv("APEX_EMAIL_API_URL", "https://your_apex_server/ords/schema/email/getAll")

# Zoho config
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID", "write_your_zoho_client_id_here")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET", "write_your_zoho_client_secret_here")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN", "write_your_zoho_refresh_token_here")
ZOHO_ACCOUNT_ID = os.getenv("ZOHO_ACCOUNT_ID", "write_your_zoho_account_id_here")
ZOHO_FROM_ADDRESS = os.getenv("ZOHO_FROM_ADDRESS", "your_mailbox@zohomail.com")


def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"

    data = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        print("❌ Failed to generate access token:", token_data)
        raise RuntimeError("Cannot get Zoho access token")

    return token_data["access_token"]


def fetch_emails():
    response = requests.get(API_URL, verify=False)  # internal SSL may be self-signed
    data = response.json()
    return data.get("items", [])


def send_email(access_token, item):
    url = f"https://mail.zoho.com/api/accounts/{ZOHO_ACCOUNT_ID}/messages"

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
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=body)

    print(f"Sending to {item['email']} → Status {response.status_code}")
    print(response.text)


def main():
    print("Fetching new emails from APEX REST API...")
    emails = fetch_emails()

    if not emails:
        print("No data found.")
        return

    print(f"Total rows fetched: {len(emails)}")

    access_token = get_access_token()

    for e in emails:
        send_email(access_token, e)


if __name__ == "__main__":
    main()
