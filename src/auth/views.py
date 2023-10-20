from flask import Blueprint, current_app, redirect, render_template, request, flash, url_for, abort, session
from ..utils.utils import db
from loguru import logger
from decouple import config
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, url_for, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from .. models import(
    Message, User
)

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        phone_number = request.form['phone_number']

        # check if email exists
        email_exists = User.query.filter_by(user_email=email).first()

        #check if phone number exists
        phone_number_exists = User.query.filter_by(phone_number=phone_number).first()

        if email_exists:
            flash('Email already exists, choose another one.', 'primary')
        
        elif phone_number_exists:
            flash('The phone number provided already exists. Please enter another one!', 'primary')

        else:
            
            try:
                
                new_user = User(
                    user_name = username,
                    password = generate_password_hash(password, method='scrypt'),
                    user_email = email,
                    phone_number = phone_number,
                    )
                db.session.add(new_user)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logger.critical(f'Failed to save new user instance to database: ', e)
                flash('Failed to save user data, Please Try Again. If issue persists Contact The Support Team', 'danger')
                return render_template('signup.html', **locals())
                        
            else:
                login_user(new_user, remember=True)
                flash('User created, you can log in with the registered credentials', 'success')
                

                return redirect(url_for('main.home'))

    
    return render_template('signup.html', **locals())

    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Login successful', 'success')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # check if user exists
        user = User.query.filter_by(user_email=email).first()

        if user:

            if user.is_active:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash('Logged in Successfully!', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Username or Password is incorrect!', 'danger')

            elif not user.is_active:
                flash("Your personal account has been suspended for violating our terms of service. You can check your email for further information or call our support team.", "danger")
        
        else:
    
            flash('Username or Password is incorrect!', 'danger')

    return render_template('login.html', **locals())


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))