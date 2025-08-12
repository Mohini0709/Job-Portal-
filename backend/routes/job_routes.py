from flask import Blueprint, request, jsonify
from db.db_connection import mysql

job_bp = Blueprint('job', __name__)

@job_bp.route('/post_job', methods=['POST'])
def post_job():
    data = request.get_json() or {}
    employer_id = data.get('employer_id')
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    salary = data.get('salary')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jobs (employer_id, title, description, location, salary) VALUES (%s,%s,%s,%s,%s)",
                (employer_id, title, description, location, salary))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Job posted successfully'})

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT jobs.id, title, description, location, salary, users.name FROM jobs JOIN users ON jobs.employer_id = users.id")
    rows = cur.fetchall()
    cur.close()
    jobs = []
    for r in rows:
        jobs.append({
            'id': r[0],
            'title': r[1],
            'description': r[2],
            'location': r[3],
            'salary': float(r[4]) if r[4] is not None else None,
            'employer_name': r[5]
        })
    return jsonify(jobs)