import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

#Blueprint for authentication functions
bp = Blueprint('auth', __name__, url_prefix='/auth')

#The register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #acces = request.form['camera']
        admin = 0;
        if request.form.get('admin'):
            admin = 1;
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Username is already taken.'

        if error is None:
            db.execute(
                'INSERT INTO users (username, password, admin) VALUES (?, ?, ?)',
                (username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), admin)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
#The Login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            session['admin'] = user['admin']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#Get logged in user
@bp.before_app_request
def get_logged_in_user():
    #Try to get the user from session if already logged in
    user = session.get('username')

    if user is None:
        g.user = None
    else:
        g.user = user

#Logout function
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Decorator for requiring login on some views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

