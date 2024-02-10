from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'P@ssword@!967'

# MySQL Connector setup
try:
    db = mysql.connector.connect(
        host="localhost",
        user="Tomorrow",
        password="P@ssword@!967",
        database="Tomorrow" 
    )
    print("Database connection successful")
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Helper function to execute SQL queries
def execute_query(query, values=None):
    cursor = db.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    db.commit()
    cursor.close()

# Root page
@app.route('/')
def index():
    return render_template('create_account_names.html')
@app.route('/create_account_names', methods=['GET', 'POST'])
def create_account_names():
    print("Executing create_account_names route")
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        email = request.form['email']

        # Check if the email already exists in the database
        query_check_email = "SELECT id FROM users WHERE email = %s"
        values_check_email = (email,)
        cursor = db.cursor()
        cursor.execute(query_check_email, values_check_email)
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            # Email already exists
            flash("User with this email already exists. Please log in.", 'error')
            return render_template('login-account.html')  # Redirect to login page or handle accordingly

        # Email doesn't exist, proceed with the insertion
        query = "INSERT INTO users (first_name, last_name, username, email) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, username, email)

        cursor = db.cursor()  # Define cursor here
        cursor.execute(query, values)

        # Get the last inserted ID (user ID)
        user_id = cursor.lastrowid
        cursor.close()  # Close cursor after use

        # Store user ID in the session
        session['user_id'] = user_id

        # Store user input in the session for later use
        session['first_name'] = first_name
        session['last_name'] = last_name
        session['username'] = username
        session['email'] = email

        # Redirect to the next page
        return redirect(url_for('create_account_dob'))

    return render_template('create_account_names.html')





@app.route('/create_account_dob', methods=['GET', 'POST'])
def create_account_dob():
    if request.method == 'POST':
        dob = request.form['dob']

        session['dob'] = dob

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET dob = %s WHERE id = %s"
            values = (dob, user_id)
            execute_query(query, values)
        return redirect(url_for('create_account_password'))
    return render_template('create_account_dob.html')


@app.route('/create_account_password', methods=['GET', 'POST'])
def create_account_password():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords don't match. Please try again.", 'error')
            return redirect(url_for('create_account_password'))

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET password = %s WHERE id = %s"
            values = (hashed_password, user_id)
            execute_query(query, values)
        return render_template('registration_success.html')

    return render_template('create_account_password.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the database
        query_check_username = "SELECT id, password FROM users WHERE username = %s"
        values_check_username = (username,)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query_check_username, values_check_username)
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            # Successful login, store user ID in session
            session['user_id'] = user['id']
            return redirect(url_for('registration-success.html'))  # Redirect to the dashboard or another page

        # Invalid login credentials
        flash("Invalid username or password. Please try again.", 'error')
        return render_template('login-account.html')

    # Redirect to login page if the request method is not POST
    return render_template('login-account.html')

if __name__ == '__main__':
    app.run(debug=True)
