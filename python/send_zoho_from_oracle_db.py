import oracledb
import requests

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_xx_x")

DB_USER = "ADMIN"
DB_PASSWORD = "write_your_db_password_here"
DB_DSN = "host:port/service_name"

ZOHO_DC = "com"
ZOHO_CLIENT_ID = "write_your_zoho_client_id_here"
ZOHO_CLIENT_SECRET = "write_your_zoho_client_secret_here"
ZOHO_REFRESH_TOKEN = "write_your_zoho_refresh_token_here"

ZOHO_ACCOUNT_ID = "write_your_zoho_account_id_here"
ZOHO_FROM_ADDRESS = "your_mailbox@zohomail.com"


def fetch_all_emails():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT ID, EMAIL, CC, BCC, MESSAGE, SUBJECT, ATTACHMENT_PATH
                  FROM EMAIL_NOTIFICATION
            """)
            return cursor.fetchall()
    except Exception as e:
        print("DB ERROR:", e)
        return []


def get_zoho_access_token():
    token_url = f"https://accounts.zoho.{ZOHO_DC}/oauth/v2/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
    }

    resp = requests.post(token_url, data=data, timeout=30)
    resp.raise_for_status()
    json_data = resp.json()
    access_token = json_data.get("access_token")

    if not access_token:
        raise RuntimeError(f"Failed to get access_token: {json_data}")

    return access_token


def send_email_via_zoho(email_data, access_token):
    url = f"https://mail.zoho.{ZOHO_DC}/api/accounts/{ZOHO_ACCOUNT_ID}/messages"

    body = {
        "fromAddress": ZOHO_FROM_ADDRESS,
        "toAddress": email_data["email"],
        "subject": email_data["subject"] or "",
        "content": email_data["message"] or "",
        "mailFormat": "html",
    }

    if email_data.get("cc"):
        body["ccAddress"] = email_data["cc"]
    if email_data.get("bcc"):
        body["bccAddress"] = email_data["bcc"]

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(url, json=body, headers=headers, timeout=30)

    if 200 <= resp.status_code < 300:
        print(f"[OK] Zoho mail sent to {email_data['email']} (ID={email_data['id']})")
    else:
        print(f"[FAIL] Zoho mail error for {email_data['email']} (ID={email_data['id']}):")
        print(resp.status_code, resp.text)


if __name__ == "__main__":
    rows = fetch_all_emails()

    if not rows:
        print("No rows found in EMAIL_NOTIFICATION.")
    else:
        print("Total rows fetched:", len(rows))

        token = get_zoho_access_token()

        for row in rows:
            email_data = {
                "id": row[0],
                "email": row[1],
                "cc": row[2],
                "bcc": row[3],
                "message": row[4],
                "subject": row[5],
                "attachment": row[6],
            }

            print(f"Sending via Zoho to: {email_data['email']} (ID={email_data['id']})")
            send_email_via_zoho(email_data, token)
