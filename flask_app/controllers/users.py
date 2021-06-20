from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User

@app.route("/")
def login_register():
    return render_template("login_register.html")

@app.route("/user/create", methods=["POST"])
def create_user():
    if User.validate(request.form):
        print("#"*80)
        print("Success!")
        user_id = User.create(request.form)
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