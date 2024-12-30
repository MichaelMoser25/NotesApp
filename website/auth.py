# Store roots 
from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import User, db

# allow to hash a password
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user

# given some x always generate same y but given a y can not find what the x was


# x -> y
# f(x) = x + 1
# f`(3) -> 2
# f(y) = y - 1
# y -> x

# setup blue print for flask application
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # get data requested from form
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user email is valid in database
        user = User.query.filter_by(email=email).first() # filter by email... could also do id=
        # check if password equals to hash stored on the server
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # remeber that the user is loged in till their session is clears
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
# decorator to make sure you can't access page unless user is logged in
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get("firstName")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # filter by email... could also do id=

        if user:
            flash('Email already exists.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 character.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email, 
                first_name=first_name, 
                password=generate_password_hash(password1, method='pbkdf2:sha256') # sha256 is the hashing algorithm
            ) 

            # add account to database
            db.session.add(new_user)

            # make commit to database
            db.session.commit()

            login_user(new_user, remember=True)

            # add user to database
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)
