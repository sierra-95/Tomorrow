from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import flash
from flask import Flask
import logging
from flask_bcrypt import Bcrypt
#pending fix

    query = "SELECT id FROM users WHERE username = %s"
    values = (username)
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, values)
    user = cursor.fetchone()
    cursor.close()
    if user:
        id = user['id']  # Extract user ID
        print(f"User ID: {id}")  # Print user ID to the terminal
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



#******************************************************************#
#working
@app.route('/create_account_password', methods=['GET', 'POST'])
def create_account_password():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords don't match. Please try again.", 'error')
            return redirect(url_for('create_account_password'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"Hash method used: {hashed_password.split('$')[1]}")

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET password = %s WHERE id = %s"
            values = (hashed_password, user_id)
            execute_query(query, values)

        user_info = get_user_info(user_id)
        send_welcome_email(user_info['email'], user_info)    
        return render_template('registration_success.html')

    return render_template('create_account_password.html')

def send_welcome_email(user_email, user_info):
    msg = Message(subject='Welcome to Tomorrow - Your Journey Starts Now!',
                  sender='mailtrap@holb20233m8xq2.tech',
                  recipients=[user_email],
                  html="""<html>
                          <head>
                              <style>
                                  body {
                                      font-family: 'Arial', sans-serif;
                                      max-width: 600px;
                                      margin: auto;
                                      padding: 20px;
                                  }
                                  img {
                                      display: block;
                                      margin: auto;
                                      max-width: 100%;
                                  }
                                  p {
                                      text-align: justify;
                                  }
                                  .footer {
                                      margin-top: 20px;
                                      text-align: center;
                                      color: #777;
                                  }
                              </style>
                          </head>
                          <body>
                              <p>Dear {user_info['first_name']},</p>
                              <p>We hope this email finds you well. Welcome to Tomorrow!</p>
                              <img src="http://127.0.0.1:5000/static/images/Logo/Light-cyan.png" alt="Tomorrow Logo">
                              <p>We're thrilled to have you on board, and your journey towards a brighter, more organized future begins right now.</p>
                              <p>Picture a stress-free tomorrow where your tasks effortlessly align with your goals. That's the Tomorrow experience we're excited to bring to you.</p>
                              <p>Thank you for choosing Tomorrow.</p>
                              <p class="footer">Best regards,<br>The Tomorrow Team</p>
                          </body>
                          </html>""")
    mail.send(msg)
#working
@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = get_event_info(event_id)

    if not event:
        flash("Event not found.", 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        updated_event_name = request.form.get('event_name')
        updated_event_date = request.form.get('event_date')
        updated_event_description = request.form.get('event_description')

        flash("Event updated successfully.", 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_event.html', event=event)
#working
def get_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    events = cursor_events.fetchall()
    cursor_events.close()

    return events

def get_user_info(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    values = (user_id,)
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, values)
    user = cursor.fetchone()
    cursor.close()

    return user
#works with the function
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        user = get_user_info(user_id)
        events = get_future_user_events(user_id)
        if user:
            return render_template('index.html', user=user, events=events)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))
    return redirect(url_for('login'))
#working
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT * FROM users WHERE email = %s OR first_name = %s"
        values = (email, email)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password = user['password']
            user_id = user['id'] 
            first_name = user['first_name']

            print(f"User ID: {user_id}") 

            if password == first_name: #or (stored_password and check_password_hash(stored_password, password)):
                session['user_id'] = user_id
                print(session['user_id'])
                flash("Login successful!", 'success')
                #return render_template('index.html', user=user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password. Please try again.", 'error')
                return redirect(url_for('login_account'))
    return render_template('login_account.html')
#working
# Save event route
@app.route('/save_event', methods=['POST'])
def save_event():
    print('Received request to save event...')
    data = request.json
    event_name = data.get('eventName')
    event_description = data.get('eventDescription')  # Add this line

    # Get user_id from the session or wherever you store it
    user_id = session.get('user_id')

    if event_name and user_id:
        print('Event name:', event_name)
        print('Event description:', event_description)  # Add this line
        print('User ID:', user_id)

        # Save the event to the database
        query = "INSERT INTO events (user_id, event_name, event_description) VALUES (%s, %s, %s)"  # Modify this line
        values = (user_id, event_name, event_description)  # Modify this line

        try:
            execute_query(query, values)
            print('Event saved successfully.')
            return jsonify({'message': 'Event saved successfully'}), 200
        except Exception as e:
            print('Error saving event:', str(e))
            return jsonify({'error': 'Error saving event to the database'}), 500

    else:
        print('Invalid data or user not logged in.')
        return jsonify({'error': 'Invalid data or user not logged in'}), 400
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

