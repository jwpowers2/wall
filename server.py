#!/usr/bin/pyton
# an insert returns last row index/id something like that
# The Wall

import re
import datetime
import calendar
import time
from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import bcrypt


app = Flask(__name__)
app.secret_key = "key"
mysql = MySQLConnector(app,'wall')

@app.route('/')

def index():
    # need to clear all flashes?
    if 'status' not in session:
        session['status'] = 'False'
        session['first_name'] = ''
        session['id'] = 0
        flash("Welcome to the Wall, Login or register to have a look at what is going on!")

    if session['status'] == 'True':

        return redirect('/wall')
        
    flash("Welcome to the Wall, Login or register to have a look at what is going on!")

    return render_template('index.html')

@app.route('/signin')

def signin():

    return render_template('signin.html')

@app.route('/signup')

def signup():

    return render_template('signup.html')

@app.route('/login', methods=['POST'])

def login():

    try:

        users = mysql.query_db("SELECT * FROM users WHERE email='{}'".format(request.form['email']))

        if bcrypt.checkpw(request.form['password'].encode(), users[0]['password'].encode()):
            session['status'] = 'True'
            session['id'] = users[0]['id']
            session['first_name'] = users[0]['first_name']
            return redirect('/wall')
        else:
            session['status'] = 'False'
            flash("Bad login, would you like to register?")
            return render_template('register.html')
            
    except:
        session['status'] = 'False'
        flash("Bad login, would you like to register?")
        return render_template('register.html')

@app.route('/register', methods=['POST'])

def register():

    proceed = True

    if session['status'] == 'True':
        return redirect('/wall')
    
    if not re.match("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$",request.form['email']):
        flash("Not valid email")
        proceed = False

    if not re.search("[a-zA-Z]{2,30}",request.form['first_name']):
        flash("first name must be all letters and at least two characters")
        proceed = False

    if not re.search("[a-zA-Z]{2,30}",request.form['last_name']):
        flash("last name must be all letters and at least two characters")
        proceed = False

    if len(request.form['password']) < 9:
        flash("Password is not long enough")
        proceed = False

    if request.form['password'] != request.form['confirm_password']:
        flash("Confirm password is not the same as password")
        proceed = False

    if proceed:

        password_hashed = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
        
        now = datetime.datetime.utcnow()
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)\
                 VALUES (:first_name, :last_name, :email, :password, :created_at, :updated_at)"

        data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': password_hashed,
	        'created_at':now,
	        'updated_at':now
               }

        good_register = mysql.query_db(query, data)

        if type(good_register) == long:

            session['status'] = 'True'
            name_query = "SELECT id,first_name FROM users WHERE email = '{}'".format(request.form['email'])
            person = mysql.query_db(name_query)
            session['first_name'] = person[0].get('first_name')
            session['id'] = person[0].get('id')
            return redirect('/wall')

        else:
            return redirect('/signup')

    else:
        return redirect('/signup')

@app.route('/wall')

def wall():
    # this will display the wall
    # show a message and all its related comments sorted so newest posts show up at top

    # display a list of objects with messages + comments
    # build list of dictionaries using select all from messages
    return render_template('wall.html', messages = mysql.query_db("SELECT * from messages"))

@app.route('/messages', methods=['POST'])

def messages():
    # this will display the wall
    # show a message and all its related comments sorted so newest posts show up at top
    # makes a message from a form on wall.html and insert into messages DB
    print request.form['message']
    print type(session['id'])
    now = datetime.datetime.utcnow()
    query = "INSERT INTO messages (user_id, message, created_at, updated_at) VALUES (:user_id,:message,:created_at, :updated_at)"

    data = {
            'user_id': session['id'],
            'message': request.form['message'],
	    'created_at':now,
	    'updated_at':now
           }

    add_message = mysql.query_db(query, data)

    if type(add_message) == long:
        return redirect('/wall')

    else:
        return redirect('/wall')

    return redirect('/wall')

@app.route('/comments', methods=['POST'])

def comments():
    # this will display the wall
    # show a message and all its related comments sorted so newest posts show up at top
    pass


@app.route('/logoff', methods=['GET'])

def logoff():

    session['status'] = 'False'
    return redirect('/')


@app.route('/<path:path>')

def catch_all(path):

    return render_template('error.html', file_path="img/ninja.png")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)      

