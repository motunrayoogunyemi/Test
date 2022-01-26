from flask import flash, render_template, request, redirect, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from projectapp.forms import LoginForm, RegisterForm
from projectapp.mymodels import db,User,Products,Category

from . import userobj


@userobj.route('/')
def home():
    return render_template('index.html')

@userobj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data)
        new = User(user_username=form.username.data, user_email=form.email.data, user_password=hashed_pass)
        db.session.add(new)
        db.session.commit()
        # session['user'] = new.id
        return 'user created'
        # return f'<h1>user: {form.email.data}</h1>'

    return render_template('register.html', form=form)

@userobj.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_username=form.username.data).first()
        if user:
            # loggedin = user.id
            check = check_password_hash(user.user_password,form.password.data)
            if check:
                # session['user'] = loggedin
                login_user(user)
                return redirect(url_for('bpuser.dashboard'))
        flash('invalid username or password')
        return redirect(url_for('bpuser.login'))
        
        # return f'<h1>user: {form.username.data}</h1>'

    return render_template('login.html', form=form)

@userobj.route('/dashboard')
@login_required
def dashboard():
    user = current_user.user_username
    return render_template('dashboard.html', user=user)   


@userobj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('bpuser.home'))
    

@userobj.route('/shop')
def shop():
    myshop = Products.query.all()
    return render_template('shop.html', myshop=myshop)