import os
import tempfile

from flask import render_template, request
from wand.image import Image

from app import webapp


@webapp.route('/imagetransform/form', methods=['GET'])
# Return file upload form
def image_form():
    return render_template("imagetransform/form.html")


@webapp.route('/imagetransform', methods=['POST'])
# Upload a new image and tranform it
def image_transform():
    # check if the post request has the file part
    if 'image_file' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['image_file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    tempdir = tempfile.gettempdir()

    fname = os.path.join('app/static', new_file.filename)

    new_file.save(fname)

    img = Image(filename=fname)
    i = img.clone()
    i.rotate(90)

    fname_rotated = os.path.join('app/static', 'rotated_' + new_file.filename)

    i.save(filename=fname_rotated)

    return render_template("imagetransform/view.html",
                           f1=fname[4:],
                           f2=fname_rotated[4:])
