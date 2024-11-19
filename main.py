# Description: This is the main file for our Flask application. This file will contain all of our routes and logic for our application.

# Import the Flask module from the flask package
from flask import Flask, render_template, request, redirect, url_for, flash #Flask library and functions
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash #This library lets us easily hash + verify passwords
import sqlite3

#Create a connection to our database
connection = sqlite3.connect('dojobase.db', check_same_thread=False)

cursor = connection.cursor() #Cursor is a control structure used to traverse and fetch records from the database. Cursor has the ability to store multiple rows returned from a query.
cursor.execute("CREATE TABLE IF NOT EXISTS card      (id INTEGER PRIMARY KEY NOT NULL, card_holder TEXT NOT NULL, PAN TEXT NOT NULL, expiry_date TEXT NOT NULL, service_code TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS user      (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, access TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS lead      (id INTEGER PRIMARY KEY NOT NULL, photo URL NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, quote TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS review    (id INTEGER PRIMARY KEY NOT NULL, review TEXT NOT NULL, author TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS session   (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, price TEXT NOT NULL, date TEXT NOT NULL, location TEXT NOT NULL, spaces_taken INTEGER NOT NULL, capacity INTEGER NOT NULL, lead_id INTEGER NOT NULL, organiser_id INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS booking   (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER NOT NULL, session_id INTEGER NOT NULL, order_total INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS contact   (id INTEGER PRIMARY KEY NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, authority TEXT NOT NULL, message TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS timeslot  (id INTEGER PRIMARY KEY NOT NULL, session_id INTEGER NOT NULL, timeslot_start TEXT NOT NULL, timeslot_end TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS activity  (id INTEGER PRIMARY KEY NOT NULL, session_id INTEGER NOT NULL, activity TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS organiser (id INTEGER PRIMARY KEY NOT NULL, photo URL NOT NULL, forname TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, quote TEXT NOT NULL)")
cursor.close()

#Create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secret_key' # This is used for flash to work

#Create a class for our user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

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

def getReviews(): #Query our table to retrieve all of our reviews
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, review, author FROM review")
        reviews = cursor.fetchall()
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        cursor.close()
    
    return reviews

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

class User(UserMixin):
    def __init__(self, id, forname, surname, email, password):
        self.id = id
        self.forname = forname
        self.surname = surname
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(id=user[0], forname=user[1], surname=user[2], email=user[3], password=user[4])
    return None

#Create a route decorator to tell Flask what URL should trigger our function
@app.route('/')
@app.route('/home')
def home():
    reviews = getReviews()
    return render_template('home.html', reviews = reviews)

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
@login_required
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
        price = "£" + request.form['price']
        capacity = request.form['capacity']
        spaces_taken = 0
        organiser_id = 1

        query_input = (name, description, price, date, location, spaces_taken, capacity, lead_id, organiser_id)

        try:
            cursor = connection.cursor()
            cursor.execute(query_for_session, (query_input))
            exists = cursor.fetchone()
        except:
            print("Database error:", error)
            flash('Database error')
        finally:
            if exists:
                leads = getLeads()
                flash('Session name already exists')
                return render_template('setup-session.html', leads = leads)
            else:
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
                    return render_template('setup-activity.html', session = name)
    else:
        leads = getLeads()
        return render_template('setup-session.html', leads = leads)

@app.route('/sessions/setup/activity', methods=['GET', 'POST'])
@login_required
def setup_activity():
    if request.method=='POST':
        query_for_activity = """
            INSERT INTO activity (session_id, activity) 
            VALUES (?, ?)
            """
        
        form_id = request.form['form_id']
        session = request.form['session']

        if form_id == "setup_activity":
            activity = request.form['activity']
            
            try:
                cursor = connection.cursor()
                cursor.execute(f"SELECT id, name FROM session WHERE name = '{session}'") #Get the last session ID
                session = cursor.fetchone()
                cursor.execute(query_for_activity, (session[0], activity))
                connection.commit()
            except sqlite3.Error as error:
                print("Database error:", error)
                flash('Database error')
                return render_template('setup-activity.html', session = session[1])
            finally:
                cursor.close()
                return render_template('setup-activity.html', session = session[1])
        elif form_id == "go_to_timeslot":
            return render_template('setup-timeslot.html', session = session)
        else:
            flash('Function error')
            return render_template('setup-activity.html', session = "")
    else:
        return render_template('setup-activity.html', session = "")

@app.route('/sessions/setup/timeslot', methods=['GET', 'POST'])
@login_required
def setup_timeslot():
    if request.method=='POST':
        query_for_timeslot = """
            INSERT INTO timeslot (session_id, timeslot_start, timeslot_end) 
            VALUES (?, ?, ?)
            """
        session = request.form['session']
        timeslot_start = request.form['timeslot_start']
        timeslot_end = request.form['timeslot_end']

        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id, name FROM session WHERE name = {session[0]}") #Get the last session ID
            session = cursor.fetchone()
            if session:
                cursor.execute(query_for_timeslot, (session[0], timeslot_start, timeslot_end))
                connection.commit()
            else:
                flash('Session does not exist')
        except sqlite3.Error as error:
            print("Database error:", error)
            flash('Database error')
            return render_template('setup-timeslot.html', session = session[1])
        finally:
            cursor.close()
            return render_template('setup-timeslot.html', session = session[1])
    else:
        return render_template('setup-timeslot.html', session = "")

@app.route('/booking')
@login_required
def booking():
    try:
        sessions = getSessionsForBookings()
        timeslots = getTimeslots(sessions[0])
        activities = getActivities(sessions[0])
        return render_template('booking.html', sessions = sessions, timeslots = timeslots, activities = activities)
    except:
        return render_template('booking.html', session = 'none')
        

@app.route('/booking/review')
@login_required
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

        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM user WHERE email='{email}'")
            user = cursor.fetchone() #fetchone() vs fetchall() depending on the situation. We only want to find 1 user here.
        except sqlite3.Error as error:
            print("Database error:", error)
            flash('Database error')
            return render_template('sign-in.html')
        finally: #finally will always run after both a try AND except.
            cursor.close() 

        if user: #if username is found          
            #Check if password entered on login page matches DB password against that username.
            if check_password_hash(user[4], password): #[4] is the password field.
                login_user(User(id=user[0], forname=user[1], surname=user[2], email=user[3], password=user[4]))
                flash('Logged in successfully.')
                return redirect(url_for('home')) #Redirect to the homepage on correct credentials
            else: #incorrect password
                flash('Invalid email or password')
                return render_template('sign-in.html') #Return to login page if not a match (you probably want to display an error message here!)
        else: #username is not found
            flash('Invalid username or password')
            return render_template('sign-in.html')
    else:     
        return render_template('sign-in.html') #Just load the login page on a GET request.

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        forname = request.form['forname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM user WHERE email='{email}'")
            user = cursor.fetchone()
        except sqlite3.Error as error:
            print("Database error:", error)
        finally: 
            cursor.close()

        if user: #Checks if there is already a user with this email address.
            flash('Email already registered')
            return redirect(url_for('signup')) #You should provide some feedback to the user rather than just redirect to the same page like this.
        else:
            try:
                if password != confirm_password:
                    flash('Passwords do not match')
                    return render_template('sign-up.html')
                elif len(password) < 8:
                    flash('Password must be at least 8 characters')
                    return render_template('sign-up.html')
                elif password == confirm_password:
                    query = "INSERT INTO user (forname, surname, email, password, access) VALUES (?, ?, ?, ?, 'none')"
                    insert_data = (forname, surname, email, generate_password_hash(password),) #Create a tuple with all the data we want to INSERT.
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
            return redirect(url_for('signin')) #Successful signup - return to login page
    else:
        return render_template('sign-up.html')

@app.route('/sign-out')
@login_required
def signout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/user')
@login_required
def user():
    return render_template('user-panel.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin-panel.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)