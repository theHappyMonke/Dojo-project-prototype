# Description: This is the main file for our Flask application. This file will contain all of our routes and logic for our application.

# Import the Flask module from the flask package
from flask import Flask, render_template, request, redirect, url_for, flash #Flask library and functions
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash #This library lets us easily hash + verify passwords
import sqlite3

#Create a connection to our database
connection = sqlite3.connect('dojobase.db', check_same_thread=False)

cursor = connection.cursor() #Cursor is a control structure used to traverse and fetch records from the database. Cursor has the ability to store multiple rows returned from a query.
cursor.execute("CREATE TABLE IF NOT EXISTS quote (id INTEGER PRIMARY KEY NOT NULL, quote TEXT NOT NULL, author TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY NOT NULL, card_holder TEXT NOT NULL, PAN TEXT NOT NULL, expiry_date TEXT NOT NULL, service_code TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, card_id INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS lead (id INTEGER PRIMARY KEY NOT NULL, photo URL NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, quote TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS organiser (id INTEGER PRIMARY KEY NOT NULL, photo URL NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, quote TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, price TEXT NOT NULL, date TEXT NOT NULL, location TEXT NOT NULL, spaces_taken INTEGER NOT NULL, capacity INTEGER NOT NULL, activity_1 TEXT NOT NULL, activity_2 TEXT NOT NULL, activity_3 TEXT NOT NULL, timeslot_1 TEXT NOT NULL, timeslot_2 TEXT NOT NULL, timeslot_3 TEXT NOT NULL, lead_id INTEGER NOT NULL, organiser_id INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS timeslot (id INTEGER PRIMARY KEY NOT NULL, session_id INTEGER NOT NULL, timeslot_start TEXT NOT NULL, timeslot_end TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY NOT NULL, session_id INTEGER NOT NULL, activity TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS booking (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER NOT NULL, session_id INTEGER NOT NULL, order_total INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS contact (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, authority TEXT NOT NULL, message TEXT NOT NULL)")
cursor.close()

#Create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secret_key' # This is used for flash to work

def getSessions(): #Query our table to retrieve all of our products
    data = "session.id, session.name, session.description, session.date, lead.forname, session.location, session.spaces_taken, session.capacity, session.price"
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT {data} FROM session JOIN lead ON session.lead_id = lead.id")
        sessions = cursor.fetchall() #fetchone() vs fetchall() depending on the situation. We want all of the data here.
    except sqlite3.Error as error:
        print("Database error:", error)
    finally: #finally will always run after both a try and except. In other words: no matter if successful or not, this code will run.
        cursor.close()
        
    return sessions

def getSessionsForBookings(): #Query our table to retrieve all of our products
    data = "session.id, session.name, session.description, session.date, lead.forname, session.location, session.spaces_taken, session.capacity, session.price"
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT {data} FROM session JOIN lead ON session.lead_id = lead.id")
        sessions = cursor.fetchall() #fetchone() vs fetchall() depending on the situation. We want all of the data here.
    except sqlite3.Error as error:
        print("Database error:", error)
    finally: #finally will always run after both a try and except. In other words: no matter if successful or not, this code will run.
        cursor.close()
        
    return sessions

def getActivities(session_id): #Query our table to retrieve all of our products
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT id, activity FROM activity WHERE session_id = {session_id[0]}")
        activities = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return activities

def getTimeslots(session_id): #Query our table to retrieve all of our products
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT id, timeslot_start, timeslot_end FROM timeslot WHERE session_id = {session_id[0]}")
        timeslots = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return timeslots

def getAuthors(): #Query our table to retrieve all of our authors
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, quote, author FROM quote")
        authors = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return authors

def getLeads(): #Query our table to retrieve all of our leads
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, photo, forname, surname, quote FROM lead")
        leads = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return leads

def getOrganisers(): #Query our table to retrieve all of our organisers
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, photo, forname, surname, quote FROM organiser")
        organisers = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return organisers

#Create a route decorator to tell Flask what URL should trigger our function
@app.route('/')
@app.route('/home')
def home():
    authors = getAuthors()
    return render_template('home.html', authors = authors)

@app.route('/about')
def about():
    leads = getLeads()
    organisers = getOrganisers()
    return render_template('about.html', leads = leads, organisers = organisers)

@app.route('/sessions')
def sessions():
    sessions = getSessions()
    return render_template('sessions.html', sessions = sessions)

@app.route('/sessions/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        query_for_session = """
            INSERT INTO session (name, description, price, date, location, spaces_taken, capacity, lead_id, organiser_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        lead_id = int(request.form['lead_id'])
        location = request.form['location']
        activity = request.form['activity']
        timeslot_start = request.form['timeslot_start']
        timeslot_end = request.form['timeslot_end']
        price = "£" + request.form['price']
        capacity = request.form['capacity']
        spaces_taken = 0
        organiser_id = 1

        try:
            cursor = connection.cursor()
            cursor.execute(query_for_session, (name, description, price, date, location, spaces_taken, capacity, lead_id, organiser_id))
            connection.commit()
        except sqlite3.Error as error:
            print("Database error:", error)
            flash('Database error')
            leads = getLeads()
            return render_template('setup-session.html', leads = leads)
        finally:
            cursor.close()
            return redirect(url_for('sessions'))
    else:
        leads = getLeads()
        return render_template('setup-session.html', leads = leads)

@app.route('/booking')
def booking():
    sessions = getSessionsForBookings()
    timeslots = getTimeslots(sessions[0])
    activities = getActivities(sessions[0])
    return render_template('booking.html', sessions = sessions, timeslots = timeslots, activities = activities)

@app.route('/booking/review')
def review():
    return render_template('review-booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # To differentiate the functions, the program checks the variable form_id to see if it is a signup or login form.
        # If it is a signup form, it will insert the email, username and password into the database.
        # All errors are handled using the try and except block which prevents the program from crashing.
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT user.email, user.password FROM user WHERE email={email}")
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
    if request.method == 'POST':
        forname = request.form['forname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # To differentiate the functions, the program checks the variable form_id to see if it is a signup or login form.
        # If it is a signup form, it will insert the email, username and password into the database.
        # All errors are handled using the try and except block which prevents the program from crashing.
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
            user = cursor.fetchone()
        except sqlite3.Error as error:
            print("Database error:", error)
            flash('Database error')
        finally: 
            cursor.close()

        if user: #Checks if there is already a user with this email address.
            flash('Email already registered')
            return redirect(url_for('sign-up')) #You should provide some feedback to the user rather than just redirect to the same page like this.
        else:
            try:
                if password != confirm_password:
                    flash('Passwords do not match')
                    return render_template('sign-up.html')
                elif len(password) < 8:
                    flash('Password must be at least 8 characters')
                    return render_template('sign-up.html')
                elif password == confirm_password:
                    query = "INSERT INTO users (forname, surname, email, password) VALUES (?, ?, ?, ?)"
                    insert_data = (forname, surname, email, generate_password_hash(password)) #Create a tuple with all the data we want to INSERT.
                    cursor = connection.cursor()
                    cursor.execute(query, insert_data) #Combine the query with the data to insert + execute.
                    connection.commit() #This is necessary to permanently make the change to our DB, the change will not persist without it.
                else:
                    flash('Unknown error')
                    return render_template('sign-up.html')
            except sqlite3.Error as error:
                print("Database error:", error)
                flash('Database error')
                return render_template('sign-up.html')
            finally: 
                cursor.close()
     
            flash('Registration successful')
            return redirect(url_for('sign-in')) #Successful signup - return to login page
    else:
        return render_template('sign-up.html')

if __name__ == '__main__':
    app.run(debug=True)