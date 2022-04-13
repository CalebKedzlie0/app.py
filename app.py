from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import bcrypt

DB_NAME = "C:/Users/18173/OneDrive - Wellington College/13DTS/Python/Flask/smile.db"

app = Flask(__name__)
app.secret_key = "h172django7853nvme91Audra5iq7w9Unzip123"


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
    return render_template('home.html', logged_in=is_logged_in())


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

    return render_template("menu.html", products=product_list, logged_in=is_logged_in())


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html', logged_in=is_logged_in())


@app.route('/logout')
def log_out():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect(request.referrer + '/?message=See+you+soon')


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        con = create_connection(DB_NAME)
        query = "SELECT id, fname, password FROM customer WHERE email = ? "
        cur = con.cursor()
        cur.execute(query, email)
        user_data = cur.fetchall()
        con.close()

        try:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        # if not bcrypt.check_password_hash(db_password, password):
            # return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        if db_password is not password:
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['first_name'] = first_name
        print(session)
        return redirect('/')
    return render_template('login.html', logged_in=is_logged_in(), fname=session.get("fname"), lname=session.get("lname"))


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'POST':
        # Gets all the variables the user inputted in the signup form.
        print(request.form)
        firstname = request.form.get('fname').strip().title()
        lastname = request.form.get('lname').strip().title()
        email = request.form.get('email').strip().lower()
        password = request.form.get('pass').strip()
        password2 = request.form.get('pass2').strip()

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        if len(password) < 8:
            return redirect('/signup?error=Passwords+must+be+8+characters+or+more')

        # hashed_password = bcrypt.generate_password_hash(password)

        # Creates the database connection.
        con = create_connection(DB_NAME)

        # Creates the query.
        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"

        # Executes the query to upload to database then commits the change and closes database.
        cur = con.cursor()

        try:
            cur.execute(query, (firstname, lastname, email, password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+is+already+in+use')

        con.commit()
        con.close()
        return redirect('/')

    return render_template('signup.html')


def is_logged_in():
    if session.get("email") is None:
        print("not logged in")
        return False
    else:
        print("logged in")
        return True


app.run(host='0.0.0.0')
