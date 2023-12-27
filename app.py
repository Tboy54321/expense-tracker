from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import  SQLAlchemy
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
from wtforms import StringField, FloatField, BooleanField, SubmitField, DateField, HiddenField
from flask_login import UserMixin
import mysql.connector
import re
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime
from flask_migrate import Migrate
import bcrypt

connection = mysql.connector.connect(host='localhost',
        database='pythonlogin', user='root', password='12345')

cursor = connection.cursor()
app = Flask(__name__)
app.app_context().push()

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'pythonlogin'

#mysql = MySQL(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/pythonlogin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'oluwatimothyllll2222'
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50))
    date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

# class ExpenseForm(FlaskForm):
#     category = StringField('Category', validators=[DataRequired()])
#     amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message='Amount must be greater than 0')])
#     status = StringField('Status', validators=[DataRequired()])
#     date = StringField('Date', validators=[DataRequired()])
#     submit = SubmitField('Add Expense')

class ExpenseForm(FlaskForm):
    category = StringField('Category')
    amount = FloatField('Amount')
    has_paid = BooleanField('Has Paid')
    date = DateField('Date', format='%Y-%m-%d')  # Add the format parameter
    submit = SubmitField('Add Expense')
    user_id = HiddenField('User ID')


@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            stored_hashed_password = account[1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                if account[3]:
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['email'] = account[2]
                    return redirect(url_for('home'))
                else:
                    msg = 'Account is deactivated'
            else:
                msg = 'Incorrect username or password!'
        else:
            msg = 'Incorrect username or password!'

        return render_template('login.html', msg = msg)

    return render_template('login.html', msg = msg)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (hashed_password, email, 1))
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


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'current-password' in request.form and 'new-password' in request.form and 'confirm-password' in request.form:
            msg = change_password()
        elif 'action' in request.form and request.form['action'] == 'deactivate_account':
            user_id = session['id']
            cursor.execute('UPDATE user SET is_active = %s WHERE id = %s', (0, user_id,))
            connection.commit()
            session.clear()

            return redirect(url_for('login'))

    return render_template('settings.html', msg=msg)


def change_password():
    if 'loggedin' in session:
        user_id = session['id']
        current_password = request.form['current-password']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        cursor.execute('SELECT password FROM user WHERE id = %s', (user_id,))
        current_db_password = cursor.fetchone()[0]

        if current_password == current_db_password:
            if new_password == confirm_password:
                cursor.execute('UPDATE user SET password = %s WHERE id = %s', (new_password, user_id))
                connection.commit()
                msg = 'Password updated successfully!'
            else:
                msg = 'Passwords do not match'
        else:
            msg = 'Incorrect current password'
    else:
        msg = 'You must be logged in to change your password'
    
    return msg


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    form = ExpenseForm()

    if form.validate_on_submit():
        try:
            user_id = session['id']
            new_expense = Expense(
                category=form.category.data,
                amount=form.amount.data,
                status='Paid' if form.has_paid.data else 'Not Paid',
                date=form.date.data.strftime('%Y-%m-%d'),
                user_id=user_id
            )

            db.session.add(new_expense)
            db.session.commit()
            
            response_data = {
                'success': True,
                'date': new_expense.date,
                'category': new_expense.category,
                'amount': new_expense.amount,
                'status': new_expense.status,
            }
            flash('Expense added successfully!', 'success')
            return jsonify(response_data)
        
        except Exception as e:
            flash(f"Error adding expense: {e}", 'error')
    else:
        print("how far")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field '{getattr(form, field).label.text}': {error}", 'error')

    expenses = Expense.query.filter_by(user_id=session['id']).all()
    print(expenses)
    print("hello")
    return render_template('add_expense.htm', form=form, expenses=expenses)

@app.route('/expense_list')
def expense_list():
    if 'loggedin' in session:
        expenses = Expense.query.filter_by(user_id=session['id']).all()
        print(expenses)
        return render_template('expense_list.html', expenses=expenses)
    
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()


    print("Database tables created successfully.")
    app.run(debug=True)

