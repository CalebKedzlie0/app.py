from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error

DB_NAME = "C:/Users/18173/OneDrive - Wellington College/13DTS/Python/Flask/smile.db"

app = Flask(__name__)
app.secret_key = "h172djaooqe7853nvbze91udha5iq7w9egnzlp123"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print(connection)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    # Creates the connection to the database.
    con = create_connection(DB_NAME)

    # Gets the values from the product table.
    query = "SELECT id, name, description, volume, price, image FROM product"

    # Executes the query to download from the database.
    cur = con.cursor()
    cur.execute(query)
    # Converts the values into a list to be sent through the site then closes the database.
    product_list = cur.fetchall()
    con.close()

    return render_template("menu.html", products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip().lower()

        con = create_connection(DB_NAME)

        query = "SELECT id, fname, password FROM customer WHERE email = ?"


    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'POST':
        # Gets all the variables the user inputted in the signup form.
        print(request.form)
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('pass')
        password2 = request.form.get('pass2')

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        if len(password) < 8:
            return redirect('/signup?error=Passwords+must+be+8+characters+or+more')

        # Creates the database connection.
        con = create_connection(DB_NAME)

        # Creates the query.
        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"

        # Executes the query to upload to database then commits the change and closes database.
        cur = con.cursor()
        cur.execute(query, (firstname, lastname, email, password))
        con.commit()
        con.close()

    return render_template('signup.html')


app.run(host='0.0.0.0')
