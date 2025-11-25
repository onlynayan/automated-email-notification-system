from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import pool
from email_sender import send_mail

app = FastAPI()


class EmailJob(BaseModel):
    email_id: int


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Email notification service is running"}


@app.post("/send-email")
async def send_email(job: EmailJob):
    email_id = job.email_id

    try:
        # DB connection from pool
        with pool.acquire() as conn:
            cur = conn.cursor()

            # Fetch email data
            cur.execute("""
                SELECT EMAIL, CC, BCC, SUBJECT, MESSAGE, ATTACHMENT_PATH
                FROM INTERN.EMAIL_NOTIFICATION
                WHERE ID = :id
            """, id=email_id)

            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail=f"Email ID {email_id} not found")

            email, cc, bcc, subject, message, attachment_path = row

            # Send mail using Zoho API
            send_mail(
                to_email=email,
                cc=cc,
                bcc=bcc,
                subject=subject,
                body=message,
                attachment_path=attachment_path
            )

            # Update status
            cur.execute("""
                UPDATE INTERN.EMAIL_NOTIFICATION
                SET LAST_UPDATE = 'SENT',
                    LAST_UPDATE_DATE = SYSDATE
                WHERE ID = :id
            """, id=email_id)

            conn.commit()

        return {"status": "sent", "email_id": email_id}

    except HTTPException:
        raise

    except Exception as e:
        # Mark as failed
        try:
            with pool.acquire() as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE INTERN.EMAIL_NOTIFICATION
                    SET LAST_UPDATE = 'FAILED',
                        LAST_UPDATE_DATE = SYSDATE
                    WHERE ID = :id
                """, id=email_id)
                conn.commit()
        except:
            pass

        raise HTTPException(status_code=500, detail=f"Error while sending email: {str(e)}")
