# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.engine import URL
#
# #  ODBC connection string.
# odbc_connection_string = (
#     "Driver={ODBC Driver 18 for SQL Server};"
#     "Server=tcp:blockchain.database.windows.net,1433;"
#     "Database=BlockchainDB;"
#     "Uid=;"
#     "Pwd=;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )
#
# # URL for mssql+pyodbc
# connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": odbc_connection_string})
#
# # Create the engine
# engine = create_engine(connection_url)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#

# COULDNT DEPLOY WITH DB