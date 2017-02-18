from flask import render_template

from app import webapp


@webapp.route('/', methods=['GET'])
# Return html with pointers to the examples
def main():
    return render_template("login.html")
