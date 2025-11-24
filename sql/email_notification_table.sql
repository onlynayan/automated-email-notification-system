CREATE TABLE EMAIL_NOTIFICATION (
    ID               NUMBER,
    EMAIL            VARCHAR2(320),
    CC               VARCHAR2(1000),
    BCC              VARCHAR2(1000),
    MESSAGE          VARCHAR2(4000),
    SUBJECT          VARCHAR2(500),
    ATTACHMENT_PATH  VARCHAR2(500),
    USER_ID          VARCHAR2(100),
    ENTER_DATE       DATE,
    LAST_UPDATE      DATE
);
