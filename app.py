import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "very_secret_key"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        email = request.form.get('email')
        cursor.execute('SELECT * FROM Users WHERE Email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            password = request.form.get('password')
            if password == user[3]:
                session['user_id'] = user[0]
                return redirect(url_for('home'))
            
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        job_title = request.form['job_title']
        company = request.form['company']
        deadline = request.form['deadline']
        status = request.form['status']
        cursor.execute('INSERT INTO Applications (User_ID, job_title, company, deadline, status) VALUES (?, ?, ?, ?, ?)', (1, job_title, company, deadline, status))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Applications')
        apps = cursor.fetchall()
        conn.close()

        total = len(apps)
        return render_template('dashboard.html', applications=apps, total_apps=total)

@app.route('/delete/<int:id>')
def delete_job(id):
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Applications WHERE App_ID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)