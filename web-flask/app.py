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

def execute_query(query, values=None):
    cursor = db.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    db.commit()
    cursor.close()

######Landing page######
@app.route('/')
def index():
    return render_template('index-landing.html')
@app.route('/index_landing')
def index_landing():
    return render_template('index-landing.html')



######Account routes######
@app.route('/welcome_create_account')
def welcome_create_account():
    return render_template('welcome_create_account.html')

@app.route('/create_account_names', methods=['GET', 'POST'])
def create_account_names():
    session.clear()
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
            flash("User with this email already exists. Please log in.", 'error')
            return render_template('login_account.html')
        query = "INSERT INTO users (first_name, last_name, username, email) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, username, email)
        cursor = db.cursor() 
        cursor.execute(query, values)

        # Get the last inserted ID (user ID)
        user_id = cursor.lastrowid
        cursor.close() 
        session['user_id'] = user_id        
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
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"Hash method used: {hashed_password.split('$')[1]}")

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET password = %s WHERE id = %s"
            values = (hashed_password, user_id)
            execute_query(query, values)
        return render_template('registration_success.html')

    return render_template('create_account_password.html')

@app.route('/login_account')
def login_account():
    session.clear()
    return render_template('login_account.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login_account.html')

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
                return redirect(url_for('login'))
    return render_template('login_account.html')



###########Dashboard section#################
#no limit display events
def get_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s ORDER BY event_date ASC"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    events = cursor_events.fetchall()
    cursor_events.close()

    return events
#set limit display future events
def get_future_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s AND event_date >= CURRENT_DATE() ORDER BY event_date ASC LIMIT 14"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    future_events = cursor_events.fetchall()
    cursor_events.close()

    return future_events
#No limit display future events
def get_all_future_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s AND event_date >= CURRENT_DATE() ORDER BY event_date ASC"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    future_events = cursor_events.fetchall()
    cursor_events.close()

    return future_events
#display all past events
def get_past_user_events(user_id):
    query_events = "SELECT * FROM events WHERE user_id = %s AND event_date <= CURRENT_DATE() ORDER BY event_date DESC"
    values_events = (user_id,)
    cursor_events = db.cursor(dictionary=True)
    cursor_events.execute(query_events, values_events)
    future_events = cursor_events.fetchall()
    cursor_events.close()

    return future_events
#Display user info
def get_user_info(user_id):
    query_user = "SELECT * FROM users WHERE id = %s"
    values_user = (user_id,)
    cursor_user = db.cursor(dictionary=True)
    cursor_user.execute(query_user, values_user)
    user = cursor_user.fetchone()
    cursor_user.close()

    user['events'] = get_user_events(user_id)
    return user

#######Dashboard###########
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

#Expired tasks
@app.route('/expired_tasks')
def expired_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = get_user_info(user_id)

        events = get_past_user_events(user_id)

        if user:
            return render_template('expired_tasks.html', user=user, events=events)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))
    return redirect(url_for('login'))

#All future tasks
@app.route('/all_future_tasks')
def all_future_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = get_user_info(user_id)

        events = get_all_future_user_events(user_id)

        if user:
            return render_template('all_future_tasks.html', user=user, events=events)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))
    return redirect(url_for('login'))

###################Saving Events section###########
from flask import session
# Save event route
@app.route('/save_event', methods=['POST'])
def save_event():
    print('Received request to save event...')
    data = request.json
    event_name = data.get('eventName')
    event_description = data.get('eventDescription')
    event_date = data.get('eventDate')    
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

##########edit event############
#fetch
def get_event_info(event_id):
    query_event = "SELECT * FROM events WHERE event_id = %s"
    values_event = (event_id,)
    
    cursor_event = db.cursor(dictionary=True)
    cursor_event.execute(query_event, values_event)
    
    event = cursor_event.fetchone()
    cursor_event.close()

    return event
def update_event(event_id, event_name=None, event_date=None, event_description=None):
    # Initialize an empty list to store the SET clauses for the SQL query
    set_clauses = []
    # Check if each field is provided and add it to the SET clauses
    if event_name is not None:
        set_clauses.append("event_name = %s")
    if event_date is not None:
        set_clauses.append("event_date = %s")
    if event_description is not None:
        set_clauses.append("event_description = %s")
    # Construct the SET part of the SQL query
    set_clause = ", ".join(set_clauses)
    # Build the SQL query
    query_update_event = f"UPDATE events SET {set_clause} WHERE event_id = %s"

    # Prepare the values for the SQL query
    values_update_event = []
    if event_name is not None:
        values_update_event.append(event_name)
    if event_date is not None:
        values_update_event.append(event_date)
    if event_description is not None:
        values_update_event.append(event_description)
    print(f"Updating event with ID: {event_id}")
    print(f"New event name: {event_name}")
    print(f"New event date: {event_date}")
    print(f"New event description: {event_description}")
    values_update_event.append(event_id)
    cursor_update_event = db.cursor()
    cursor_update_event.execute(query_update_event, values_update_event)
    db.commit()
    cursor_update_event.close()

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    # Retrieve event information based on event_id
    event = get_event_info(event_id)

    if not event:
        flash("Event not found.", 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        updated_event_name = request.form.get('event_name')
        updated_event_date = request.form.get('event_date')
        updated_event_description = request.form.get('event_description')

        
        print(f"Form submission for editing event with ID: {event_id}")
        print(f"New event name: {updated_event_name}")
        print(f"New event date: {updated_event_date}")
        print(f"New event description: {updated_event_description}")

        update_event(event_id, updated_event_name, updated_event_date, updated_event_description)

        flash("Event updated successfully.", 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_event.html', event=event)

#delete event
@app.route('/delete_event/<int:event_id>', methods=['GET'])
def delete_event(event_id):
    print(f'Received request to delete event with id {event_id}')

    # Get user_id from the session or wherever you store it
    user_id = session.get('user_id')

    if user_id:
        delete_query = "DELETE FROM events WHERE event_id = %s AND user_id = %s"
        delete_values = (event_id, user_id)

        try:
            execute_query(delete_query, delete_values)
            print(f'Event with id {event_id} deleted successfully.')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard after deletion
        except Exception as e:
            print(f'Error deleting event with id {event_id}: {str(e)}')
            return jsonify({'error': f'Error deleting event with id {event_id}'}), 500
    else:
        print('User not logged in.')
        return jsonify({'error': 'User not logged in'}), 401
        

############account section###################
@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if 'user_id' in session:
        user_id = session['user_id']

        if request.method == 'POST':           
            updated_first_name = request.form.get('first_name')
            updated_last_name = request.form.get('last_name')
            updated_username = request.form.get('username')
            updated_email = request.form.get('email')
            updated_dob = request.form.get('dob')
            
            update_user_details(user_id, updated_first_name, updated_last_name, updated_username, updated_email, updated_dob)

            flash("User details updated successfully.", 'success')
            return redirect(url_for('my_account'))
       
        user = get_user_info(user_id)

        if user:
            return render_template('account.html', user=user)
        else:
            flash("User not found.", 'error')
            return redirect(url_for('login'))

    return redirect(url_for('login'))

def update_user_details(user_id, first_name=None, last_name=None, username=None, email=None, dob=None):
    print(f"Updating user with ID: {user_id}")
    print(f"New first name: {first_name}")
    print(f"New last name: {last_name}")
    print(f"New username: {username}")
    print(f"New email: {email}")
    print(f"New date of birth: {dob}")

    query_update_user = "UPDATE users SET first_name = %s, last_name = %s, username = %s, email = %s, dob = %s WHERE id = %s"
    values_update_user = [first_name, last_name, username, email, dob, user_id]

    cursor_update_user = db.cursor()
    cursor_update_user.execute(query_update_user, values_update_user)
    db.commit()
    cursor_update_user.close()

#DANGER ZONE -DELETE ACCOUNT
def delete_user(user_id):
    query_delete_user = "DELETE FROM users WHERE id = %s"
    values_delete_user = (user_id,)
    cursor_delete_user = db.cursor()
    cursor_delete_user.execute(query_delete_user, values_delete_user)
    db.commit()
    cursor_delete_user.close()

@app.route('/delete_user/<int:user_id>')
def delete_user_route(user_id):
    delete_user(user_id)
    flash("User deleted successfully.", 'success')
    print(f"Deleted user id: {user_id}")
    return redirect(url_for('index_landing'))

if __name__ == '__main__':
    app.run(debug=True)
