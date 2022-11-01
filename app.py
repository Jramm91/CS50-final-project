from crypt import methods
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configur Flask applictaion
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATE_AUTO_RELOAD"] = True

# establish any jinja filters here if needed

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diy-app.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
# @login_required
def index():
    """Displays main page"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # username = request.form.get("username")
        # password = request.form.get("password")
        # # admin priv
        # if username == admin and password == admin_pass:
        #     return redirect("/")
        # # set an error message default
        # error = None
        # # Ensure username was submited 
        # if not request.form.get("username"):
        #     return redirect("/login")
        # elif not request.form.get('password'):
        #     return redirect('/login')
        
        # # Query database for username
        # rows = db.execure("Select * FROM users WHERE username = ?",
        #                     username = request.form.get('username'))
        # # Ensure username exists and passord is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]['hash'], request.form.get('password')):
        #     return redirect('/login')
        
        # # Remember which user has logged in
        # session['user_id'] = rows[0]["ID"]

        # Redirect user to home page
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        # check if fields are entered
        # todo

        # set password requirments
        password = request.form.get("password")
        l, u, d, s = 0, 0, 0, 0
        if (len(password) >=8):
            for i in password:
                # lowercase
                if (i.islower()):
                    l += 1
                # uppercase
                if (i.isupper()):
                    u += 1
                # count digit
                if (i.isdigit()):
                    d += 1
                # special
                if (i == "@" or i == "!" or i == "?"):
                    s += 1
            if not (l >= 1 and u >= 1 and d >= 1 and s >= 1):
                return redirect("/regiser")
            # check if confirmation is entered

            # ensure confirmation matches password
            if request.form.get("confirmation") != request.form.get("password"):
                return redirect("/register")
            
            # make a hash of entered password
            hash = generate_password_hash(request.form.get("password"))

            # enter values into database
            # see if username is already entered
            try:
                new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
            except:
                return redirect("/register")

            session["user_id"] = new_user

            return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)