from flask import Blueprint, render_template, request, redirect,\
    url_for, flash
from . import db, bcrypt, model

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
@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def auth_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    