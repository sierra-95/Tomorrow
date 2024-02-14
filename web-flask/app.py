from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import flash
from flask import Flask, jsonify
import logging
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#crash logging
handler = logging.FileHandler('flask_app.log')
handler.setLevel(logging.INFO) 
app.logger.addHandler(handler)


#terminal logging
app.logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('flask_log.txt')
app.logger.addHandler(file_handler)

#Password encryption
bcrypt = Bcrypt(app)
app.secret_key = 'P@ssword@!967'

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

# Root page -Landing page
@app.route('/')
def index():
    return render_template('index-landing.html')
@app.route('/index_landing')
def index_landing():
    return render_template('index-landing.html')

@app.route('/welcome_create_account')
def welcome_create_account():
    return render_template('welcome_create_account.html')

@app.route('/create_account_names', methods=['GET', 'POST'])
def create_account_names():
    print("Executing create_account_names route")
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        query_check_email = "SELECT id FROM users WHERE email = %s"
        values_check_email = (email,)
        cursor = db.cursor()
        cursor.execute(query_check_email, values_check_email)
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            # Email already exists
            flash("User with this email already exists. Please log in.", 'error')
            return render_template('login_account.html')

        # Email doesn't exist, proceed with the insertion
        query = "INSERT INTO users (first_name, last_name, username, email) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, username, email)

        cursor = db.cursor() 
        cursor.execute(query, values)

        # Get the last inserted ID (user ID)
        user_id = cursor.lastrowid
        cursor.close() 

        # Store user ID in the session
        session['user_id'] = user_id

        # Store user input in the session for later use
        session['first_name'] = first_name
        session['last_name'] = last_name
        session['username'] = username
        session['email'] = email
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
        print(f"Hash method used: {hashed_password.split('$')[1]}")

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET password = %s WHERE id = %s"
            values = (hashed_password, user_id)
            execute_query(query, values)
        return render_template('registration_success.html')

    return render_template('create_account_password.html')
#for index-landing nav
@app.route('/login_account')
def login_account():
    return render_template('login_account.html')

@app.route('/logout')
def logout():
    return render_template('login_account.html')
########################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = "SELECT * FROM users WHERE username = %s OR first_name = %s"
        values = (username, username)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password = user['password']
            user_id = user['id']  # Extract user ID
            first_name = user['first_name']

            print(f"User ID: {user_id}")  # Print user ID to the terminal

            if password == first_name: #or (stored_password and check_password_hash(stored_password, password)):
                session['user_id'] = user_id
                print(session['user_id'])
                flash("Login successful!", 'success')
                #return render_template('index.html', user=user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password. Please try again.", 'error')
                return redirect(url_for('login'))

    # Render the login page if it's a GET request
    return render_template('login_account.html')

#Dashboard section
def get_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s ORDER BY event_date ASC"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    events = cursor_events.fetchall()
    cursor_events.close()

    return events

def get_user_info(user_id):
    query_user = "SELECT * FROM users WHERE id = %s"
    values_user = (user_id,)
    cursor_user = db.cursor(dictionary=True)
    cursor_user.execute(query_user, values_user)
    user = cursor_user.fetchone()
    cursor_user.close()

    # Fetch user events
    user['events'] = get_user_events(user_id)

    return user

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        # Retrieve user information
        user = get_user_info(user_id)

        events = get_user_events(user_id)

        if user:
            return render_template('index.html', user=user, events=events)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))

    # Handle the case where the user is not logged in
    return redirect(url_for('login'))


from flask import session
# Save event route
@app.route('/save_event', methods=['POST'])
def save_event():
    print('Received request to save event...')
    data = request.json
    event_name = data.get('eventName')
    event_description = data.get('eventDescription')
    event_date = data.get('eventDate')


    # Get user_id from the session or wherever you store it
    user_id = session.get('user_id')
    if event_name and user_id:        
        #query = "INSERT INTO events (user_id, event_name, event_date, event_description) VALUES (%s, %s, TRIM(%s), %s)"
        #values = (user_id, event_name, event_date, event_description)
        event_date_formatted = datetime.strptime(event_date, '%Y-%B-%d').date()
        event_date_trimmed = event_date_formatted.strftime('%Y-%m-%d')

        query = "INSERT INTO events (user_id, event_name, event_date, event_description) VALUES (%s, %s, %s, %s)"
        values = (user_id, event_name, event_date_trimmed, event_description)
        print('Event name:', event_name)
        print('Event description:', event_description)
        print('Event date:', event_date)
        print('User ID:', user_id)

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
    
@app.route('/my_account')
def my_account():
    if 'user_id' in session:
        user_id = session['user_id']

        # Retrieve user information
        user = get_user_info(user_id)

        if user:
            return render_template('account.html', user=user)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))

    return redirect(url_for('login')) 

@app.route('/update_user_details', methods=['POST'])
def update_user_details():
    if 'user_id' in session:
        user_id = session['user_id']

        data = request.json

        update_query = "UPDATE users SET "
        update_values = []

        for field, value in data.items():
            update_query += f"{field} = %s, "
            update_values.append(value)

        update_query = update_query.rstrip(', ')

        
        update_query += " WHERE id = %s"
        update_values.append(user_id)

        try:
            cursor = db.cursor()
            cursor.execute(update_query, update_values)
            db.commit()
            cursor.close()

            print('User details updated successfully')
            return jsonify({'success': True, 'message': 'User details updated successfully'})
        except Exception as e:
            print(f'Error updating user details: {str(e)}')
            return jsonify({'success': False, 'message': f'Error updating user details: {str(e)}'})
    
    print('User not logged in')
    return jsonify({'success': False, 'message': 'User not logged in'})



if __name__ == '__main__':
    app.run(debug=True)
