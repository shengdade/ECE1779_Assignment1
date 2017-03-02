import random

import boto3
from flask import redirect, url_for, request

import config
from app import webapp


@webapp.route('/admin/create', methods=['POST'])
def ec2_create():
    num_create = int(request.form.get('num-new'))
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(ImageId=config.ami_id,
                                     InstanceType=config.instance_type,
                                     SecurityGroups=config.security_group,
                                     KeyName=config.key_name,
                                     MinCount=1,
                                     MaxCount=num_create)
    id_list = []
    for ins in instances:
        id_list.append(ins.id)

    ec2.create_tags(Resources=id_list, Tags=[{'Key': 'Name', 'Value': 'a1-worker'}])

    return redirect(url_for('admin'))


@webapp.route('/admin/destroy', methods=['POST'])
def ec2_destroy():
    num_destroy = int(request.form.get('num-del'))
    ec2 = boto3.resource('ec2')
    workers = list(ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-worker']},
                 {'Name': 'instance-state-name', 'Values': ['running', 'pending']}]))

    if num_destroy > len(workers):
        return 'No worker can be further destroyed.'
    else:
        random.shuffle(workers)
        for i in range(num_destroy):
            workers[i].terminate()
        return redirect(url_for('admin'))
