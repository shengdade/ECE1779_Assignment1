from flask import json

from app import webapp
from utils import update_setting


@webapp.route('/admin/setting-manually', methods=['POST'])
def set_manually():
    update_setting("autoScaling", 0)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@webapp.route('/admin/setting-auto', methods=['POST'])
def set_auto():
    update_setting("autoScaling", 1)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
