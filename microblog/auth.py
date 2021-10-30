from flask import Blueprint, render_template, request, redirect,\
    url_for, flash
from . import db, bcrypt, model
from flask_login import current_user

bp = Blueprint('auth', __name__)

#----------------------------------------------Sign up----------------------------------- 
@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")

@bp.route("/signup",methods = ["POST"])
def auth_signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Equal passwor/singup/singupds
    if  password != request.form.get('password_repeat'):
        flash("Passwords differ")
        return redirect(url_for("auth.signup"))
    
    # Check if the email is already atthedatabase
    user = model.User.query.filter_by(email = email).first()
    if user:
        flash('User already exists') 
        return redirect(url_for("auth.signup"))

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password = password_hash)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.index'))

#----------------Log in---------------------------------------------------
import flask_login

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def auth_login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = model.User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        flask_login.login_user(user)
        return redirect(url_for('main.index'))
    else:
        flash('Wrong email or password. Try again')
        return redirect(url_for('auth.login'))

#----------------------Log out-----------------------------------------------
@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('auth.login'))