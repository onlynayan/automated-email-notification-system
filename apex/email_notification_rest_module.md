# 📡 Oracle APEX – Email Notification REST API Module

This module exposes the **EMAIL_NOTIFICATION** Oracle table as a REST API endpoint using Oracle ORDS.
The endpoint is used by the Python automation script to fetch pending emails and send them via SMTP or Zoho Mail API.

---

## ✅ Module Name

`email_notification_api`

## ✅ Base Path

```
/email/
```

## ✅ Endpoint

### **GET /getAll**

Returns all records from the `EMAIL_NOTIFICATION` table.

### **Example URL**

```
https://<your-domain>:8443/ords/<schema>/email/getAll
```

---

## ✅ SQL Used in the GET Handler

```sql
SELECT 
    id,
    email,
    cc,
    bcc,
    message,
    subject,
    attachment_path,
    user_id,
    enter_date,
    last_update
FROM email_notification;
```

---

## 📄 JSON Response Structure

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "email": "example@gmail.com",
      "cc": null,
      "bcc": null,
      "message": "<h2>This is a test</h2>",
      "subject": "Test Subject",
      "attachment_path": null,
      "user_id": "ADMIN",
      "enter_date": "2025-11-24T04:27:15Z",
      "last_update": null
    }
  ],
  "count": 1,
  "hasMore": false
}
```

---
