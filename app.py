from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DB_NAME = "C:/Users/18173/OneDrive - Wellington College/13DTS/Python/Flask/smile.db"

app = Flask(__name__)


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
    con = create_connection(DB_NAME)

    query = "SELECT id, name, description, volume, price, image FROM product"

    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()

    return render_template("menu.html", products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


@app.route('/login')
def render_login_page():
    return render_template('login.html')


@app.route('/signup')
def render_signup_page():
    return render_template('signup.html')


app.run(host='0.0.0.0')
