from flask import redirect
from flask import request

from app import webapp


@webapp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    print username, password
    return redirect('/')


@webapp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    confirm_password = request.form.get('confirm_password', "")
    print username, password, confirm_password
    return redirect('/')
