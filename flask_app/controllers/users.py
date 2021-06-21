from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login_register():
    # renders the main page with registration form and login
    return render_template("login_register.html")

@app.route("/create", methods=["POST"])
def create_user():
    # validate the form
    if User.validate(request.form):
        # if valid then hash the password and save it to a dictionary
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        # create the new user
        User.create(data)
        # save that user into session
        session["first_name"] = data["first_name"]
        flash("You've been logged in!")
        return redirect("/success")
    else:
        # if form is invalid, redirect to the main page with the registration form
        return redirect("/")

@app.route("/success")
def welcome_user():
    if not "first_name" in session:
        flash("You need to login first!")
        return redirect("/")
    return render_template('welcome_user.html')

@app.route("/login", methods=["POST"])
def login():
    data = { "email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['first_name'] = user_in_db.first_name
    flash("You've been logged in!")
    return redirect("/success")

@app.route("/logout")
def logout():
    if "first_name" in session:
        flash("You've been logged out.")
        session.pop("first_name", None)
        return redirect("/")
