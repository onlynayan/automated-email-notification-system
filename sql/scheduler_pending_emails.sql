---------------------------------------------------------
-- PROCEDURE : SEND_ALL_PENDING_EMAILS
-- Retries all emails that are NOT marked as SENT
---------------------------------------------------------

CREATE OR REPLACE PROCEDURE NTS.SEND_ALL_PENDING_EMAILS AS
    CURSOR c_pending IS
        SELECT ID
        FROM   NTS.EMAIL_NOTIFICATION
        WHERE  NVL(LAST_UPDATE, 'NONE') <> 'SENT';
BEGIN
    FOR r IN c_pending LOOP

        -- Mark as processing
        UPDATE NTS.EMAIL_NOTIFICATION
        SET LAST_UPDATE = 'PROCESSING',
            LAST_UPDATE_DATE = SYSDATE
        WHERE ID = r.ID;

        COMMIT;

        -- Call FastAPI service
        NTS.SEND_EMAIL_REQUEST(r.ID);

        -- Mark as sent
        UPDATE NTS.EMAIL_NOTIFICATION
        SET LAST_UPDATE = 'SENT',
            LAST_UPDATE_DATE = SYSDATE
        WHERE ID = r.ID;

        COMMIT;

    END LOOP;
END;
/
---------------------------------------------------------
-- SCHEDULER JOB : SEND_PENDING_EMAILS_JOB
-- Runs every 5 minutes and processes unsent emails
---------------------------------------------------------

BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
        job_name        => 'SEND_PENDING_EMAILS_JOB',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'NTS.SEND_ALL_PENDING_EMAILS',
        repeat_interval => 'FREQ=MINUTELY; INTERVAL=5',
        enabled         => TRUE
    );
END;
/
---------------------------------------------------------
-- SEE JOB STATUS
---------------------------------------------------------
-- SELECT job_name, state, last_start_date, next_run_date
-- FROM user_scheduler_jobs;
