from flask import Flask, render_template, flash, url_for, request
import sqlite3

connection = sqlite3.connect('dojobase.db', check_same_thread=False)

cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, cardholder TEXT, PAN TEXT, expiryDate TEXT, serviceCode TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS dojos (id INTEGER PRIMARY KEY, Fname TEXT, Sname TEXT, email TEXT, password TEXT, cardID INTEGER, FOREIGN KEY(cardID) REFERENCES cards(id))")
cursor.close()
#REFERENCES cards(id))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secret_key'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sessions')
def sessions():
    return render_template('sessions.html')

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
        print('Form data received')
    else:
        return render_template('sign-in.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'post':
        print('Form data received')
    else:
        return render_template('sign-up.html')

if __name__ == '__main__':
    app.run(debug=True)