# auth_routes.py
from flask import Blueprint, request, jsonify
import bcrypt
import uuid
import datetime
from db.db_connection import mysql
from utils.email_service import send_reset_email
import config
from flask_mail import Mail

auth_bp = Blueprint('auth', __name__)
mail = Mail()

@auth_bp.record_once
def on_load(state):
    # initialize Mail with the app when blueprint registers
    mail.init_app(state.app)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
                    (name, email, hashed, role))
        mysql.connection.commit()
        return jsonify({'message': 'Account created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password, role FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    user_id, hashed_pw, role = user
    if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
        return jsonify({'message': 'Login successful', 'user_id': user_id, 'role': role})
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if not user:
        cur.close()
        return jsonify({'error': 'Email not found'}), 404
    user_id = user[0]
    token = str(uuid.uuid4())
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=config.RESET_TOKEN_EXP_MINUTES)
    cur.execute("INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s,%s,%s)",
                (user_id, token, expires_at))
    mysql.connection.commit()
    cur.close()
    reset_link = f"{config.FRONTEND_BASE}/reset_password.html?token={token}"
    send_reset_email(mail, email, reset_link, config.MAIL_USERNAME)
    return jsonify({'message': 'Password reset email sent'})

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    token = data.get('token')
    new_password = data.get('new_password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, expires_at FROM password_reset_tokens WHERE token = %s", (token,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({'error': 'Invalid token'}), 400
    user_id, expires_at = row
    if datetime.datetime.now() > expires_at:
        cur.close()
        return jsonify({'error': 'Token expired'}), 400
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
    cur.execute("DELETE FROM password_reset_tokens WHERE token = %s", (token,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Password updated successfully'})