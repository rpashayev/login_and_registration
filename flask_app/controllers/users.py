from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/users/dashboard')
def get_one_user():
    if 'id' not in session:
        return redirect('/logout')
    id = {
        'id': session['id']
    }
    return render_template('dashboard.html', one_user = user.User.get_one_user(id))

@app.route('/users/register', methods=['POST'])
def register_new_user():
    if not user.User.validate_user_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    
    session['id'] = user.User.register_user(data)
    
    return redirect ('/users/dashboard')

@app.route('/users/login', methods=['POST'])
def login_user():
    data = {
        'email': request.form['login_email']
    }
    login_user = user.User.get_user_by_email(data)

    if not login_user:
        flash('No user found','login_error')
        return redirect('/')
    if not bcrypt.check_password_hash(login_user.password, request.form['login_password']):
        flash('Wrong password','login_error')
        return redirect('/')
    
    session['id'] = login_user.id
    
    return redirect ('/users/dashboard')

@app.route('/users/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
