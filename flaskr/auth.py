import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
#from flaskr.read import read_tag
#from multiprocessing import Pool
import threading
import RPi.GPIO as GPIO
from flaskr import create_app
from mfrc522 import SimpleMFRC522
#Blueprint for authentication functions
bp = Blueprint('auth', __name__, url_prefix='/auth')


#Decorator for requiring login on some views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#The register view function
@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        camera = request.get_json()['camera']
        admin = request.get_json()['admin']
        db = get_db()
        error = None
        input = None

        if db.execute(
            'SELECT username FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Numele ales este deja luat.'
            input = "username"
        elif db.execute(
            'SELECT id FROM camere WHERE id = ?', (camera,)
        ).fetchone() is None:
            error = 'Camera selectata nu exista.'
            input = "camera"
        #Add the user in database
        if error is None:
            db.execute(
                'INSERT INTO users (username, password, admin) VALUES (?, ?, ?)',
                (username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), admin)
            )
            db.commit()
            #Add username and camera in angajati
            try:
                db.execute(
                    'INSERT INTO angajati (id_tag, nume, acces_camera) VALUES (?, ?, ?)', (None, username, camera)
                    )
                db.commit()
            except:
                error = 'Eroare adaugand angajat.'
                input = "camera"
            #Run the function to read tag id in a parrallel process
            thr = threading.Thread(target=read_tag, args=(username, camera))
            thr.start()
        return jsonify(
            username = username,
            camera = camera,
            error = error,
            input = input
        )
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
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
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
        g.user = get_db().execute(
            'SELECT * FROM users WHERE username = ?', (user,)
        ).fetchone()

#Logout function
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def read_tag(nume, camera):
    reader = SimpleMFRC522()
    try:
           id, text = reader.read()
    finally:
           GPIO.cleanup()
    app = create_app()
    with app.app_context():
        db = get_db()
        db.execute("UPDATE angajati SET id_tag = ? WHERE nume = ? and acces_camera = ?", (id, nume, camera))
        db.commit()

@bp.route('/get_angajat')
def get_angajat():
    if request.method == 'GET':
        db = get_db()
        username = request.args["username"]
        row = db.execute("SELECT id_tag FROM angajati WHERE nume = ?", (username,)).fetchone()
        if row["id_tag"] is None:
            return jsonify(message = "NotFound")
        return jsonify(message = "Found", redirect = url_for('pontaj.index'))
