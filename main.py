# Description: This is the main file for our Flask application. This file will contain all of our routes and logic for our application.

# Import the Flask module from the flask package
from flask import Flask, render_template, flash, url_for, request
import sqlite3

#Create a connection to our database
connection = sqlite3.connect('dojobase.db', check_same_thread=False)

cursor = connection.cursor() #Cursor is a control structure used to traverse and fetch records from the database. Cursor has the ability to store multiple rows returned from a query.
cursor.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY NOT NULL, card_holder TEXT NOT NULL, PAN TEXT NOT NULL, expiry_date TEXT NOT NULL, service_code TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, card_id INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS lead (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS organiser (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, price INTEGER NOT NULL, date TEXT NOT NULL, location TEXT NOT NULL, activity_1 TEXT NOT NULL, activity_2 TEXT NOT NULL, activity_3 TEXT NOT NULL, timeslot_1 TEXT NOT NULL, timeslot_2 TEXT NOT NULL, timeslot_3 TEXT NOT NULL, lead_id INTEGER NOT NULL, organiser_id INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS booking (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER NOT NULL, session_id INTEGER NOT NULL, order_total INTEGER NOT NULL)")
cursor.close()

#Create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secret_key'

def getSessions(): #Query our table to retrieve all of our products
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT session.id, session.date, lead.forname, session.location, session.activity_1, session.activity_2, session.activity_3, session.timeslot_1, session.timeslot_2, session.timeslot_3, session.price FROM session JOIN lead ON session.lead_id = lead.id JOIN organiser ON session.organiser_id = organiser.id")
        sessions = cursor.fetchall() #fetchone() vs fetchall() depending on the situation. We want all of the data here.
    except sqlite3.Error as error:
        print("Database error:", error)
    finally: #finally will always run after both a try and except. In other words: no matter if successful or not, this code will run.
        cursor.close()
        
    print(sessions)
    return sessions

#Create a route decorator to tell Flask what URL should trigger our function
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sessions')
def sessions():
    sessions = getSessions()
    return render_template('sessions.html', sessions = sessions)

@app.route('/sessions/setup')
def setup():
    return render_template('setup-session.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/booking/review')
def review():
    return render_template('review-booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == 'post':
        email = request.form['email']
        password = request.form['password']

        # To differentiate the functions, the program checks the variable form_id to see if it is a signup or login form.
        # If it is a signup form, it will insert the email, username and password into the database.
        # All errors are handled using the try and except block which prevents the program from crashing.
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT user.email, user.password FROM user WHERE email='{email}'")
            check = cursor.fetchone()
            cursor.close()
        except sqlite3.Error as error:
            flash('Database error', error)
            return render_template('login.html')
        
        if check[1] == password:
            flash('Login successful')
            return render_template('home.html')
    else:
        return render_template('sign-in.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'post':
        forname = request.form['forname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        # To differentiate the functions, the program checks the variable form_id to see if it is a signup or login form.
        # If it is a signup form, it will insert the email, username and password into the database.
        # All errors are handled using the try and except block which prevents the program from crashing.
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO user VALUES (NULL, '{forname}', '{surname}', '{email}', '{password}')")
            connection.commit()
            flash('Signup successful')
        except sqlite3.Error as error:
            flash('Database error', error)
        finally:
            cursor.close()
            return render_template('login.html')
    else:
        return render_template('sign-up.html')

if __name__ == '__main__':
    app.run(debug=True)