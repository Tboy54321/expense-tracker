from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
import mysql.connector

connection = mysql.connector.connect(host='localhost',
        database='pythonlogin', user='root', password='')

cursor = connection.cursor()
app = Flask(__name__)

app.secret_key = ''

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'pythonlogin'

#mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

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
        print(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            #session['username'] = account['username']
            session['email'] = account[3]
            return redirect(url_for('home'))
            # Redirect to home page
            #return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg = msg)
    #return '<h1>WRONG PASSWORD</h1>'


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.htm')

@app.route('/expense_list')
def expense_list():
    return render_template('expense_list.html')

if __name__ == '__main__':
    app.run(debug=True)
