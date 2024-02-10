from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
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
        email = request.form['email']

        # Store user details in the MySQL database
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
        values = (first_name, last_name, email)

        cursor = db.cursor()  # Define cursor here
        cursor.execute(query, values)
        db.commit()  # Commit changes to the database
        cursor.close()  # Close cursor after use

        # Get the last inserted ID (user ID)
        user_id = cursor.lastrowid

        # Store user ID in the session
        session['user_id'] = user_id

        # Store user input in the session for later use
        session['first_name'] = first_name
        session['last_name'] = last_name
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

    # Render the HTML page
    return render_template('create_account_dob.html')

@app.route('/create_account_password', methods=['GET', 'POST'])
def create_account_password():
    if request.method == 'POST':
        # Assuming your form has an input field named 'password'
        password = request.form['password']

        # You may want to hash the password before storing it in the database
        # Here, we'll just use the password directly for demonstration purposes
        session['password'] = password

        user_id = session.get('user_id', None)
        if user_id:
            query = "UPDATE users SET password = %s WHERE id = %s"
            values = (password, user_id)
            execute_query(query, values)

        # Redirect to a success page or perform additional actions if needed
        return render_template('registration_success.html')

    # Render the HTML page
    return render_template('create_account_password.html')



if __name__ == '__main__':
    app.run(debug=True)
