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
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    

    if request.method == 'POST':
        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        job_title = request.form['job_title']
        company = request.form['company']
        deadline = request.form['deadline']
        status = request.form['status']
        cursor.execute('INSERT INTO Applications (User_ID, job_title, company, deadline, status) VALUES (?, ?, ?, ?, ?)', (user_id, job_title, company, deadline, status))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        sort_selection = request.args.get('sort', 'deadline')
        allowed_columns = {
            'company': 'company',
            'status': 'status',
            'deadline': 'deadline'
        }
        column = allowed_columns.get(sort_selection, 'deadline')
        query = f'SELECT * FROM Applications WHERE User_ID = ? ORDER BY {column} ASC'

        conn = sqlite3.connect('job_tracker.db')
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))

        apps = cursor.fetchall()
        conn.close()

        total = len(apps)
        return render_template('dashboard.html', applications=apps, total_apps=total)

@app.route('/delete/<int:id>')
def delete_job(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('job_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Applications WHERE App_ID = ? AND User_ID = ?', (id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)