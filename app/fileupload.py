import boto3
from flask import render_template, request, session, redirect, url_for

from app import webapp


@webapp.route('/test/FileUpload/form', methods=['GET'])
# Return file upload form
def upload_form():
    return render_template("fileupload/form.html")


@webapp.route('/test/FileUpload', methods=['POST'])
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

    s3 = boto3.client('s3')
    username = str(session['username'])
    s3.create_bucket(Bucket=username)
    s3.upload_fileobj(new_file, username, new_file.filename)

    return redirect(url_for('index'))
