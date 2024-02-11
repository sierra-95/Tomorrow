from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import flash
from flask import Flask
import logging
from flask_bcrypt import Bcrypt

#pending fix
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user with the given username
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user and 'password' in user:
            stored_password = user['password']
            print(f"Fetched user from database: {user}")
            print(f"Stored password from database: {stored_password}")
            
            if check_password_hash(stored_password, password):
                # Successful login, you can now redirect or perform other actions
                flash("Login successful!", 'success')
                print("Login successful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password. Please try again.", 'error')
                print("Invalid username or password.")
                return redirect(url_for('login'))

    # Render the login page if it's a GET request
    return render_template('login-account.html')

#working
logging.basicConfig(filename='flask_log.txt', level=logging.DEBUG)
@app.after_request
def log_request(response):
    app.logger.info(
        f"{request.method} {request.path} - {response.status_code}"
    )
    return response


#working
@app.route('/create_account_names', methods=['GET', 'POST'])
def create_account_names():
    print("Executing create_account_names route")
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
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
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
        values = (first_name, last_name, email)

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
        session['email'] = email

        # Redirect to the next page
        return redirect(url_for('create_account_dob'))

    return render_template('create_account_names.html')




#working
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

