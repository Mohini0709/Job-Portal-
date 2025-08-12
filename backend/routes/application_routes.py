from flask import Blueprint, request, jsonify
from db.db_connection import mysql

app_bp = Blueprint('application', __name__)

@app_bp.route('/apply_job', methods=['POST'])
def apply_job():
    data = request.get_json() or {}
    job_id = data.get('job_id')
    applicant_id = data.get('applicant_id')
    cover_letter = data.get('cover_letter')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO applications (job_id, applicant_id, cover_letter) VALUES (%s,%s,%s)",
                (job_id, applicant_id, cover_letter))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Applied successfully'})

@app_bp.route('/applications/<int:employer_id>', methods=['GET'])
def view_applications(employer_id):
    # Return applications for jobs posted by this employer
    cur = mysql.connection.cursor()
    cur.execute("SELECT a.id, a.job_id, a.applicant_id, a.cover_letter, a.applied_at, j.title FROM applications a JOIN jobs j ON a.job_id = j.id WHERE j.employer_id = %s",
                (employer_id,))
    rows = cur.fetchall()
    cur.close()
    apps = []
    for r in rows:
        apps.append({'id': r[0], 'job_id': r[1], 'applicant_id': r[2], 'cover_letter': r[3], 'applied_at': str(r[4]), 'job_title': r[5]})
    return jsonify(apps)