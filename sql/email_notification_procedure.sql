CREATE OR REPLACE PROCEDURE SEND_EMAIL_REQUEST(p_id NUMBER)
AS
    req   UTL_HTTP.req;
    resp  UTL_HTTP.resp;
    url   VARCHAR2(500);
BEGIN
    url := 'http://YOUR_FASTAPI_IP:8000/send-email';

    req := UTL_HTTP.begin_request(url, 'POST', 'HTTP/1.1');
    UTL_HTTP.set_header(req, 'Content-Type', 'application/json');

    UTL_HTTP.write_text(req,
        '{"email_id": ' || p_id || '}'
    );

    resp := UTL_HTTP.get_response(req);
    UTL_HTTP.end_response(resp);

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error calling FastAPI: ' || SQLERRM);
END;
/
