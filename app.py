import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        job_title = request.form['job_title']
        company = request.form['company']
        deadline = request.form['deadline']
        status = request.form['status']
        cursor.execute('INSERT INTO Applications (job_title, company, deadline, status) VALUES (? , ?, ?, ?)', (job_title, company, deadline, status))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Applications')
        apps = cursor.fetchall()
        conn.close()
        return render_template('dashboard.html', applications=apps)

@app.route('/delete/<int:id>')
def delete_job(id):
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Applications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

