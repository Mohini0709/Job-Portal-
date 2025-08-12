# db_connection.py
from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    # app should have config keys set before calling init_db
    mysql.init_app(app)
    return mysql