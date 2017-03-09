from flask import json, request

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


@webapp.route('/admin/setting-cpu-grow', methods=['POST'])
def set_cpu_grow():
    data = request.form['data']
    update_setting("cpuGrow", int(data.strip('%')))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@webapp.route('/admin/setting-cpu-shrink', methods=['POST'])
def set_cpu_shrink():
    data = request.form['data']
    update_setting("cpuShrink", int(data.strip('%')))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@webapp.route('/admin/setting-ratio-expand', methods=['POST'])
def set_ratio_expand():
    data = request.form['data']
    update_setting("ratioExpand", int(data))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@webapp.route('/admin/setting-ratio-shrink', methods=['POST'])
def set_ratio_shrink():
    data = request.form['data']
    update_setting("ratioShrink", int(data))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
