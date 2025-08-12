# app.py (entrypoint)
from flask import Flask, send_from_directory
from config import *
from db.db_connection import init_db
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp
from routes.application_routes import app_bp
from flask_mail import Mail
from flask_cors import CORS
import os

# Set paths for frontend
FRONTEND_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

app = Flask(
    __name__,
    template_folder=FRONTEND_FOLDER,
    static_folder=FRONTEND_FOLDER
)
CORS(app)

# configure app from config module
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

# init extensions
mysql = init_db(app)
mail = Mail(app)

# register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(job_bp)
app.register_blueprint(app_bp)

# serve frontend index.html for root URL
@app.route('/')
def serve_home():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

# serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
