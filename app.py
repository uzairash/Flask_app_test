from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape
import os
from DB.db import get_db, close_db, init_db_command

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.instance_path, 'flaskr.sqlite')
app.secret_key = 'your_secret_key'  # Required for flashing messages and CSRF protection

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

app.cli.add_command(init_db_command)

@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user = db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?);',
            (username, password)
        ).fetchone()
        db.commit()
        # Replace this section with actual user registration logic
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            return "incorrect username"
        elif user['password'] == password:
            return f"Welcome, {escape(username)}!"
        else:
            return "Invalid password!"
        
    return render_template('login.html')
