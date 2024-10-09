from flask import Flask, render_template, flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_a_very_secret_key'
