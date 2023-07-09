import os

# Define the base directory of your Flask application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # MySQL configuration
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'db_f_wbs_revit'

    # Other configuration options
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False