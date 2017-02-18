from flask import redirect, render_template, request, session, url_for, escape

from app import webapp


class ServerError(Exception):
    pass


@webapp.route('/', methods=['GET'])
@webapp.route('/index', methods=['GET'])
# Return html with pointers to the examples
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    username_session = escape(session['username']).capitalize()
    return render_template('main.html', user_name=username_session)


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            username_form = request.form['username']
            password_form = request.form['password']

            raise ServerError('Invalid password')

    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@webapp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    confirm_password = request.form.get('confirm_password', "")
    print username, password, confirm_password
    return redirect('/')


@webapp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
