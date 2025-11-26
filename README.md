# 🚀 Automated Email Notification System

A fully automated, production-ready email notification system integrating:

- **Oracle Database (Triggers, Procedures, Scheduler Jobs)**
- **Python FastAPI Microservice**
- **Zoho Mail API (OAuth2)**
- **Oracle REST + Automation**
- **End‑to‑End Email Delivery Workflow**

This system automatically sends emails whenever a new row is inserted into the Oracle table.  
If any email fails, a scheduler job retries it every 5 minutes.

---

# 📌 Features

### ✅ Real-time email sending
Triggered immediately after an INSERT in Oracle.

### ✅ Automated retry mechanism
Scheduler job checks all pending/failed emails and resends them.

### ✅ FastAPI microservice
Handles sending emails using Zoho Mail API with OAuth tokens.

### ✅ Secure & modular
Environment variables, packaged SQL scripts, and production-safe configuration.

### ✅ Supports:
- HTML emails  
- CC/BCC  
- File attachments (path-based)  
- Zoho Mail API (OAuth Refresh Token → Access Token)  
- Oracle connection pooling  
- Logging email status  

---

# 📂 Project Structure

```
automated-email-notification-system/
│
├── fastapi/
│   ├── app.py               # Main FastAPI service
│   ├── db.py                # Oracle DB pool
│   ├── email_sender.py      # Zoho email logic
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
│
├── sql/
│   ├── email_notification.sql
│   ├── email_notificaion_seq.sql
│   ├── email_notification_trigger.sql
│   ├── email_notification_procedure.sql
│   ├── scheduler_pending_emails.sql
│   └── README.md
│
├── apex/
│   └── (APEX-related documentation if any)
│
├── .env.example
├── .gitignore
└── README.md   <--- this file
```

---

# 🧩 System Architecture

```mermaid
flowchart TD
    A[Insert into EMAIL_NOTIFICATION] --> B[Oracle BEFORE INSERT Trigger]
    B --> C[Sequence Assigns ID]
    C --> D[AFTER INSERT Trigger]
    D --> E[Procedure SEND_EMAIL_REQUEST]
    E --> F[FastAPI POST /send-email]
    F --> G[Fetch row from Oracle DB]
    G --> H[Zoho Mail API]
    H --> I[Email Sent]
    I --> J[Update LAST_UPDATE='SENT']

    subgraph Scheduler (Every 5 min)
       K[Check pending emails]
       K --> E
    end
```

---

# 📬 Email Flow (Step-by-Step)

### 1️⃣ User inserts a record into Oracle table
```
INSERT INTO INTERN.EMAIL_NOTIFICATION (EMAIL, SUBJECT, MESSAGE)
VALUES ('user@example.com', 'Hello', '<h2>Welcome</h2>');
```

### 2️⃣ BEFORE trigger assigns auto sequence ID  
### 3️⃣ AFTER trigger calls:
```
SEND_EMAIL_REQUEST(:NEW.ID);
```

### 4️⃣ FastAPI receives:
```json
{
  "email_id": 12
}
```

### 5️⃣ FastAPI fetches row → sends email via Zoho Mail API  
### 6️⃣ Updates:
```
LAST_UPDATE = 'SENT'
LAST_UPDATE_DATE = SYSDATE
```

If sending fails:
```
LAST_UPDATE = 'FAILED'
```

### 7️⃣ Scheduler job retries FAILED emails every 5 minutes.

---

# 🛠 Oracle Components

### ✔ Table  
`sql/email_notification.sql`

### ✔ Sequence  
`sql/email_notificaion_seq.sql`

### ✔ Triggers  
- BEFORE INSERT (assign ID)
- AFTER INSERT (call FastAPI)

`sql/email_notification_trigger.sql`

### ✔ Procedure  
Calls FastAPI using UTL_HTTP

`sql/email_notification_procedure.sql`

### ✔ Scheduler Job  
Retries pending emails every 5 minutes

`sql/scheduler_pending_emails.sql`

---

# 🔧 FastAPI Microservice

### Start service:
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Endpoints

| Method | Endpoint       | Description |
|--------|----------------|-------------|
| GET    | `/`            | Health check |
| POST   | `/send-email` | Sends an email using email_id |

---

# 📦 Environment Variables

### Global `.env.example`
```
ORACLE_USER=
ORACLE_PASSWORD=
ORACLE_DSN=

ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_REFRESH_TOKEN=
ZOHO_ACCOUNT_ID=
ZOHO_FROM_ADDRESS=
```

⚠️ Never upload your real `.env`.

---

# 🚀 Deployment Options

- Windows or Linux FastAPI deployment
- Oracle DB local/remote
- Docker-ready (optional)
- Supports internal networks (192.168.x.x)

---

# 🧑‍💻 Author

Developed by **Nayan Das**  
A production-grade example of Oracle + Python FastAPI + Zoho automation.

---

# ⭐ Contribution

Feel free to fork the repo, submit issues, or open pull requests.

---

# 📜 License

MIT License (Recommended to add)
