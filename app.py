# from flask import Flask, request, redirect, url_for, render_template, flash
# import sqlite3
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Needed for flashing messages
#
# # Initialize the database
# def init_db():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS user_info (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             firstname TEXT NOT NULL,
#             lastname TEXT NOT NULL,
#             gender TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# init_db()
#
# @app.route('/')
# def signup_form():
#     return render_template('signup.html')
#
# @app.route('/signup-success', methods=['POST'])
# def signup_success():
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     gender = request.form['gender']
#     email = request.form['email']
#     password = request.form['psw']
#     password_repeat = request.form['psw-repeat']
#
#     # Server-side validation
#     if password != password_repeat:
#         flash("Passwords do not match.")
#         return redirect(url_for('signup_form'))
#
#     if not firstname.isalpha() or not lastname.isalpha():
#         flash("First name and Last name should only contain letters.")
#         return redirect(url_for('signup_form'))
#
#     if len(password) < 8:
#         flash("Password must be at least 8 characters long.")
#         return redirect(url_for('signup_form'))
#
#     # Check if email already exists
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM user_info WHERE email = ?', (email,))
#     existing_user = cursor.fetchone()
#     if existing_user:
#         flash("This email is already registered.")
#         conn.close()
#         return redirect(url_for('signup_form'))
#
#     # Save data to database
#     cursor.execute('''
#         INSERT INTO user_info (firstname, lastname, gender, email, password)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (firstname, lastname, gender, email, password))
#     conn.commit()
#     conn.close()
#
#     return "Signup successful!"
#
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, redirect, url_for, render_template, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            gender TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def login_form():
    return render_template('login.html')

@app.route('/signup')
def signup_form():
    return render_template('signup.html')

@app.route('/signup-success', methods=['POST'])
def signup_success():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    gender = request.form['gender']
    email = request.form['email']
    password = request.form['psw']
    password_repeat = request.form['psw-repeat']

    # Server-side validation
    if password != password_repeat:
        flash("Passwords do not match.")
        return redirect(url_for('signup_form'))

    if not firstname.isalpha() or not lastname.isalpha():
        flash("First name and Last name should only contain letters.")
        return redirect(url_for('signup_form'))

    if len(password) < 8:
        flash("Password must be at least 8 characters long.")
        return redirect(url_for('signup_form'))

    # Check if email already exists
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_info WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        flash("This email is already registered.")
        conn.close()
        return redirect(url_for('signup_form'))

    # Save data to database
    cursor.execute('''
        INSERT INTO user_info (firstname, lastname, gender, email, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (firstname, lastname, gender, email, password))
    conn.commit()
    conn.close()

    return redirect(url_for('login_form'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['psw']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_info WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        flash("Login successful!")
        return "Login successful!"
    else:
        flash("Invalid email or password.")
        return redirect(url_for('login_form'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)
