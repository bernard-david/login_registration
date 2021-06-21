from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login_register():
    return render_template("login_register.html")

@app.route("/user/create", methods=["POST"])
def create_user():
    if User.validate(request.form):
        print("#"*80)
        print("Success!")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        user_id = User.create(data)
        session["user_id"] = user_id
        return redirect(f"/user/{user_id}")
    else:
        print("#"*80)
        print("Failed!")
        return redirect("/")

@app.route("/user/<int:user_id>")
def welcome_user(user_id):
    data = {
        'id': user_id
    }
    user = User.get_user(data)

    return render_template('welcome_user.html', user = user)

@app.route("/user/login", methods=["POST"])
def login():
    data = { "email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id
    user_id = session['user_id']
    return redirect(f"/user/{user_id}")
