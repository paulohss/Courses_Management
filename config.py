import os

class Config:        
     
    SQLALCHEMY_DATABASE_URI =  os.getenv('MSSQL_PYODBC')
    SQLALCHEMY_TRACK_MODIFICATIONS = False