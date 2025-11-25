import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# ZOHO CONFIG
# -----------------------------
ZOHO_DC = os.getenv("ZOHO_DC", "com")
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ACCOUNT_ID = os.getenv("ZOHO_ACCOUNT_ID")
ZOHO_FROM_ADDRESS = os.getenv("ZOHO_FROM_ADDRESS")

# -----------------------------
# GET ACCESS TOKEN
# -----------------------------
def get_access_token():
    token_url = f"https://accounts.zoho.{ZOHO_DC}/oauth/v2/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET
    }

    resp = requests.post(token_url, data=data)
    if resp.status_code != 200:
        raise Exception("Zoho Access Token Error: " + resp.text)

    return resp.json().get("access_token")


# -----------------------------
# SEND EMAIL
# -----------------------------
def send_mail(to_email, cc, bcc, subject, body, attachment_path=None):
    access_token = get_access_token()

    url = f"https://mail.zoho.{ZOHO_DC}/api/accounts/{ZOHO_ACCOUNT_ID}/messages"

    payload = {
        "fromAddress": ZOHO_FROM_ADDRESS,
        "toAddress": to_email,
        "subject": subject or "",
        "content": body or "",
        "mailFormat": "html"
    }

    if cc:
        payload["ccAddress"] = cc

    if bcc:
        payload["bccAddress"] = bcc

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code not in (200, 201):
        raise Exception("Zoho SendMail Error: " + resp.text)

    return True
