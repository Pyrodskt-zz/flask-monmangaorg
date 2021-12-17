from flask import Blueprint, render_template, flash, session
from flask import request
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models import add_user, get_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        data = request.form
        username = data.get('uname')
        psw = data.get('psw')
        if psw != get_user(username)[2]:
            flash('Wrong password', category='alert')
        else:
            session['USERNAME'] = get_user(username)[0]
            flash('Connection successful !', category='success')
            return render_template('home.html')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session['USERNAME'] = ""
    return render_template('home.html')

@auth.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        data = request.form
        username = data.get('uname')
        psw = data.get('psw')
        psw_repeat = data.get('psw-repeat')

        if len(username) < 4:
            flash('username must be greater than 4 characters', category='error')
        
        elif len(psw) < 4:
            flash('password must be greater than 4 characters', category='error')

        elif psw != psw_repeat:
            flash('Both passsword must be the same', category='error')

        else:
            add_user(username, psw)

    return render_template('signup.html')
