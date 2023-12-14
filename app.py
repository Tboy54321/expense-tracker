from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
import mysql.connector
import re
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

connection = mysql.connector.connect(host='localhost',
        database='pythonlogin', user='root', password='')

cursor = connection.cursor()
app = Flask(__name__)

app.secret_key = 'oluwatimothyllll2222'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'pythonlogin'

#mysql = MySQL(app)


@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        #username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        ##cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            #session['username'] = account['username']
            session['email'] = account[2]
            return redirect(url_for('home'))
            # Redirect to home page
            #return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg = msg)
    return render_template('login.html', msg = msg)
    #return '<h1>WRONG PASSWORD</h1>'


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
    # Create variables for easy access
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            #hash = password + app.secret_key
            #hash = hashlib.sha1(hash.encode())
            #password = hash.hexdigest()
            hashed_password = generate_password_hash(password, method='sha256')
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s)', (password, email,))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('sign_up.html', msg = msg)


@app.route('/logout')
def logout ():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/settings')
def settings():
    if 'loggedin' in session:
        return render_template('settings.html')
    else:
        return redirect(url_for('login'))


@app.route('/add_expense')
def add_expense():
    if 'loggedin' in session:
        return render_template('add_expense.htm')
    else:
        return redirect(url_for('login'))


@app.route('/expense_list')
def expense_list():
    if 'loggedin' in session:
        return render_template('expense_list.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
