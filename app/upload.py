import os
import tempfile

import boto3
from flask import render_template, request, session, redirect, url_for
from wand.image import Image

import config
from app import webapp, celery
from utils import get_db, ServerError


@webapp.route('/upload', methods=['POST'])
# Upload a new file and store in the systems temp directory
def file_upload():
    # check if the post request has the file part
    if 'uploadedfile' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['uploadedfile']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    if 'username' not in session:
        return redirect(url_for('login'))

    s3 = boto3.client('s3', **config.conn_args)
    username = str(session['username'])
    s3.create_bucket(Bucket=username)

    name, extn = new_file.filename.split('.')
    extn = '.' + extn
    key0 = name + extn
    key1 = name + '_1' + extn
    key2 = name + '_2' + extn
    key3 = name + '_3' + extn

    with Image(file=new_file) as image:

        fd, path = tempfile.mkstemp()
        try:
            image.save(filename=path)
            with os.fdopen(fd, 'r') as tmp:
                s3.upload_fileobj(tmp, username, key0)
        finally:
            upload_transformations.delay(username, path, key1, key2, key3)

    cnx = get_db()
    cursor = cnx.cursor()

    query = '''SELECT id FROM users WHERE login = %s'''
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''INSERT INTO images (userId,key1,key2,key3,key4) VALUES (%s,%s,%s,%s,%s)'''
    cursor.execute(query, (user_id, key0, key1, key2, key3))
    cnx.commit()

    return redirect(url_for('index'))


@celery.task
def upload_transformations(username, tmp_path, key1, key2, key3):
    print 'begin celery upload task'
    s3 = boto3.client('s3', **config.conn_args)

    try:
        img = Image(filename=tmp_path)
        trans1 = img.clone()
        trans2 = img.clone()
        trans3 = img.clone()
        trans1.rotate(180)
        trans2.rotate(90)
        trans3.rotate(270)

        trans1.save(filename=tmp_path)
        with open(tmp_path) as f:
            s3.upload_fileobj(f, username, key1)

        trans2.save(filename=tmp_path)
        with open(tmp_path) as f:
            s3.upload_fileobj(f, username, key2)

        trans3.save(filename=tmp_path)
        with open(tmp_path) as f:
            s3.upload_fileobj(f, username, key3)

    finally:
        os.remove(tmp_path)

    print 'celery upload task done'


@webapp.route('/test/FileUpload/form', methods=['GET'])
# Return file upload form
def upload_form():
    return render_template("upload.html")


@webapp.route('/test/FileUpload', methods=['POST'])
# Upload a new file and store in the systems temp directory
def test_file_upload():
    # check if the post request has the file part
    if 'uploadedfile' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['uploadedfile']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    # connect to database
    cnx = get_db()
    cursor = cnx.cursor()

    username_form = request.form['userID']
    password_form = request.form['password']

    try:
        # determine whether valid username
        query = "SELECT COUNT(*) FROM users WHERE login = %s"
        cursor.execute(query, (username_form,))
        if not cursor.fetchone()[0]:
            raise ServerError('Invalid username')

        # verify user password
        query = "SELECT password FROM users WHERE login = %s"
        cursor.execute(query, (username_form,))
        if cursor.fetchone()[0] != password_form:
            raise ServerError('Invalid password')

    except ServerError as e:
        return render_template("upload.html", error=str(e))

    s3 = boto3.client('s3', **config.conn_args)
    username = username_form
    s3.create_bucket(Bucket=username)

    name, extn = new_file.filename.split('.')
    extn = '.' + extn
    key0 = name + extn
    key1 = name + '_1' + extn
    key2 = name + '_2' + extn
    key3 = name + '_3' + extn

    with Image(file=new_file) as image:

        fd, path = tempfile.mkstemp()
        try:
            image.save(filename=path)
            with os.fdopen(fd, 'r') as tmp:
                s3.upload_fileobj(tmp, username, key0)
        finally:
            upload_transformations.delay(username, path, key1, key2, key3)

    cnx = get_db()
    cursor = cnx.cursor()

    query = '''SELECT id FROM users WHERE login = %s'''
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''INSERT INTO images (userId,key1,key2,key3,key4) VALUES (%s,%s,%s,%s,%s)'''
    cursor.execute(query, (user_id, key0, key1, key2, key3))
    cnx.commit()

    return render_template("upload.html", error='upload successfully')
