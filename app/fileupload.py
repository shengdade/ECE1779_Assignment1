import os
import tempfile

from flask import render_template, request

from app import webapp


@webapp.route('/test/FileUpload/form', methods=['GET'])
# Return file upload form
def upload_form():
    return render_template("fileupload/form.html")


@webapp.route('/test/FileUpload', methods=['POST'])
# Upload a new file and store in the systems temp directory
def file_upload():
    userid = request.form.get("userID")
    passowrd = request.form.get("password")

    # check if the post request has the file part
    if 'uploadedfile' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['uploadedfile']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    tempdir = tempfile.gettempdir()

    new_file.save(os.path.join(tempdir, new_file.filename))

    return "Success"
