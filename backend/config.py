# Edit values for your environment (or better: use environment variables)

import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'job_portal')

# Email (Gmail example) - prefer App Password
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@gmail.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_app_password')

RESET_TOKEN_EXP_MINUTES = int(os.getenv('RESET_TOKEN_EXP_MINUTES', 15))
FRONTEND_BASE = os.getenv('FRONTEND_BASE', 'http://127.0.0.1:5500/frontend')