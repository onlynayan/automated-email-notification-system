import oracledb
import os
from dotenv import load_dotenv

# Path of your Oracle Instant Client
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_9")

load_dotenv()

USER = os.getenv("ORACLE_USER")
PASS = os.getenv("ORACLE_PASSWORD")
DSN  = os.getenv("ORACLE_DSN")

pool = oracledb.create_pool(
    user=USER,
    password=PASS,
    dsn=DSN,
    min=1,
    max=5,
    increment=1
)
