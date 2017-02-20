import os
from datetime import timedelta

import boto3
import mysql.connector
from flask import g
from flask import redirect, render_template, request, session, url_for, escape

from app import webapp
from app.config import db_config

webapp.secret_key = os.urandom(24)


class ServerError(Exception):
    pass


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@webapp.before_request
def make_session_permanent():
    session.permanent = True
    webapp.permanent_session_lifetime = timedelta(minutes=5)


@webapp.route('/', methods=['GET'])
@webapp.route('/index', methods=['GET'])
# Return html with pointers to the examples
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    s3 = boto3.resource('s3')
    s3_cli = boto3.client('s3')
    username = str(session['username'])
    bucket = s3.Bucket(username)
    images = bucket.objects.all()
    image_list = []
    for image in images:
        url = s3_cli.generate_presigned_url('get_object', Params={'Bucket': username, 'Key': image.key}, ExpiresIn=100)
        image_list.append(url)
        print url

    username_session = escape(session['username']).capitalize()
    return render_template('main.html', user_name=username_session, image_list=image_list)


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':

            # connect to database
            cnx = get_db()
            cursor = cnx.cursor()

            # determine whether valid username
            username_form = request.form['username']
            query = "SELECT COUNT(*) FROM users WHERE login = %s"
            cursor.execute(query, (username_form,))
            if not cursor.fetchone()[0]:
                raise ServerError('Invalid username')

            # verify user password
            password_form = request.form['password']
            query = "SELECT password FROM users WHERE login = %s"
            cursor.execute(query, (username_form,))
            if cursor.fetchone()[0] == password_form:
                session['username'] = request.form['username']
                return redirect(url_for('index'))

            raise ServerError('Invalid password')

    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@webapp.route('/register', methods=['POST'])
def register():
    username_form = request.form['username']
    password_form = request.form['password']
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''INSERT INTO users (login,password) VALUES (%s,%s)'''
    cursor.execute(query, (username_form, password_form))
    cnx.commit()
    return redirect('/login')


@webapp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
