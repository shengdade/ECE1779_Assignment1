import boto3
from flask import render_template, request, session, redirect, url_for, escape

from app import webapp
import config
from utils import get_db, ServerError


@webapp.route('/view', methods=['POST'])
def image_view():
    key = str(request.form['key'])
    if key == "":
        return redirect(url_for('index'))

    if 'username' not in session:
        return redirect(url_for('login'))

    key = key.split('?')[0].split('/')[3]
    username = str(session['username'])
    cnx = get_db()
    cursor = cnx.cursor()

    try:
        query = '''SELECT i.key1, i.key2, i.key3, i.key4
                   FROM users u, images i
                   WHERE u.id = i.userId AND u.login = %s AND key1 = %s;'''
        cursor.execute(query, (username, key))
        row = cursor.fetchone()
        if not row:
            raise ServerError('Invalid image key')

    except ServerError:
        print 'Invalid image key'
        return redirect(url_for('index'))

    s3_cli = boto3.client('s3', **config.conn_args)
    url_list = []
    for key in row:
        url = s3_cli.generate_presigned_url('get_object', Params={'Bucket': username, 'Key': key}, ExpiresIn=10)
        url_list.append(url)

    username_session = escape(session['username']).capitalize()
    return render_template('view.html', user_name=username_session, image_list=url_list)
