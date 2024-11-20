import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://server_name/database_name?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False