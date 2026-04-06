import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Load backend/.env if exists
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Also load azure/.env to fetch the deployed database credentials
load_dotenv(os.path.join(BASE_DIR, '..', 'azure', '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mnh-hospital-secret-key-2024')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mnh-jwt-secret-key-2024')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours

    # Database - Azure SQL/MySQL or SQLite fallback
    AZURE_SQL_CONNECTION = os.getenv('AZURE_SQL_CONNECTION', '')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    
    if AZURE_SQL_CONNECTION:
        SQLALCHEMY_DATABASE_URI = AZURE_SQL_CONNECTION
    elif MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE:
        # Require PyMySQL to be installed (`pip install pymysql`)
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'mnh_hospital.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Azure OpenAI
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY', '')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')

    # Azure ML
    AZURE_ML_ENDPOINT = os.getenv('AZURE_ML_ENDPOINT', '')
    AZURE_ML_KEY = os.getenv('AZURE_ML_KEY', '')

    # Azure Storage
    AZURE_STORAGE_CONNECTION = os.getenv('AZURE_STORAGE_CONNECTION', '')
