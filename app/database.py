from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL file as the database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app/database.sql"
# SQLALCHEMY_DATABASE_URL = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:blockchain.database.windows.net,1433;Database=BlockchainDB;Uid=useradmin;Pwd=BlockChain123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# from sqlalchemy.engine import URL
# connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=dagger;DATABASE=test;UID=user;PWD=password"
# connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
#
# from sqlalchemy import create_engine
# engine = create_engine(connection_url)
# Login: useradmin
# pass: BlockChain123

# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# Define your ODBC connection string.
odbc_connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:blockchain.database.windows.net,1433;"
    "Database=BlockchainDB;"
    "Uid=useradmin;"
    "Pwd=BlockChain123;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Create a proper URL for mssql+pyodbc
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": odbc_connection_string})

# Create the engine without sqlite-specific arguments.
engine = create_engine(connection_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
