import oracledb
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize Oracle client (adjust path as needed)
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_xx_x")

DB_USER = "ADMIN"
DB_PASSWORD = "write_your_db_password_here"
DB_DSN = "host:port/service_name"


def fetch_all_emails():
    """
    Fetches all records from EMAIL_NOTIFICATION table.
    """
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


def send_email_via_gmail(data):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    smtp_user = "write_your_gmail_here"
    smtp_pass = "write_your_gmail_app_password_here"

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = data["email"]
    msg["Subject"] = data["subject"]

    msg.attach(MIMEText(data["message"] or "", "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {data['email']}")
    except Exception as e:
        print("EMAIL ERROR:", e)


if __name__ == "__main__":
    rows = fetch_all_emails()

    if not rows:
        print("No rows found.")
    else:
        print("Total rows fetched:", len(rows))
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

            print(f"Sending to: {email_data['email']} (ID={email_data['id']})")
            send_email_via_gmail(email_data)
