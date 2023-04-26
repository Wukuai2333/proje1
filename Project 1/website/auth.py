from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
 # . means __init__.py 
from . import db  
from flask_login import login_user, login_required, logout_user, current_user

#  (the name of the blueprint, the module where the blueprint belongs to)
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # retrieve a user from a database based on their email address.
        user = User.query.filter_by(email=email).first()
        # if a user object was found in the database
        if user:
            # if the provided password matches the hashed password stored in the user.password
            if check_password_hash(user.password, password):
                flash('You are logged in!!', category='success')
                # set a cookie in the browser: the remember parameter is set to True.
                login_user(user, remember=True)
                # redirect the user to the home page
                # url_for Blueprint.Function name, will be better than simply '/' 
                # because it will be easier in potential further editing
                return redirect(url_for('views.home'))
                # if password is not match: remind the user to enter the password again
            else:
                flash('Please enter the correct password to log in!', category='error')
        # if user is not found
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
# should first be logged in to log out!
@login_required
def logout():
    logout_user()
    # redirect to the login page
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # make sure every input is valid
        user = User.query.filter_by(email=email).first()
        # if a user object was found in the database
        # a new user should not sign up with the existed e-mail
        if user:
            flash('Email already exists.', category='error')

        # if the email is not found in the database, the user can continue registering
        # simple length condition for valid info
        elif len(email) < 7:
            flash('Email must be greater than 6 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')        
        elif len(password1) < 6:
            flash('Password must be at least 5 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')

        # when there is no such user existed in the database, and length conditions are all met
        # a new user will be created and a hashed password will be generated
        # argon 2 hashing algorithm is used here due to its strongness
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='argon2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account is created!', category='success')
            # url_for Blueprint.Function name, will be better than simply '/' 
            # because it will be easier in potential further editing
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)



