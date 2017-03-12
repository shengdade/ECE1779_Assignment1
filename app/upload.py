import os

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

    static_folder = 'app/static'
    path0 = os.path.join(static_folder, 'tran0')
    new_file.save(path0)

    name, extn = new_file.filename.split('.')
    extn = '.' + extn
    key0 = name + extn
    key1 = name + '_1' + extn
    key2 = name + '_2' + extn
    key3 = name + '_3' + extn

    upload_transformations.delay(username, path0, static_folder, key1, key2, key3)

    with open(path0) as f:
        s3.upload_fileobj(f, username, key0)

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
def upload_transformations(username, path0, static_folder, key1, key2, key3):
    print 'begin celery upload task'
    s3 = boto3.client('s3', **config.conn_args)

    path1 = os.path.join(static_folder, 'tran1')
    path2 = os.path.join(static_folder, 'tran2')
    path3 = os.path.join(static_folder, 'tran3')

    img = Image(filename=path0)
    trans1 = img.clone()
    trans2 = img.clone()
    trans3 = img.clone()
    trans1.rotate(180)
    trans2.rotate(90)
    trans3.rotate(270)
    trans1.save(filename=path1)
    trans2.save(filename=path2)
    trans3.save(filename=path3)

    with open(path1) as f:
        s3.upload_fileobj(f, username, key1)
    with open(path2) as f:
        s3.upload_fileobj(f, username, key2)
    with open(path3) as f:
        s3.upload_fileobj(f, username, key3)

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

    static_folder = 'app/static'
    path0 = os.path.join(static_folder, 'tran0')
    new_file.save(path0)

    name, extn = new_file.filename.split('.')
    extn = '.' + extn
    key0 = name + extn
    key1 = name + '_1' + extn
    key2 = name + '_2' + extn
    key3 = name + '_3' + extn

    upload_transformations.delay(username, path0, static_folder, key1, key2, key3)

    with open(path0) as f:
        s3.upload_fileobj(f, username, key0)

    cnx = get_db()
    cursor = cnx.cursor()

    query = '''SELECT id FROM users WHERE login = %s'''
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''INSERT INTO images (userId,key1,key2,key3,key4) VALUES (%s,%s,%s,%s,%s)'''
    cursor.execute(query, (user_id, key0, key1, key2, key3))
    cnx.commit()

    return render_template("upload.html", error='upload successfully')
