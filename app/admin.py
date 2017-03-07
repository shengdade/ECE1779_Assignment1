import random

import boto3
import celery
from flask import redirect, url_for, request

import config
from app import webapp


@webapp.route('/admin/create', methods=['POST'])
def ec2_create():
    num_create = int(request.form.get('num-new'))
    ec2 = boto3.resource('ec2', **config.conn_args)
    instances = ec2.create_instances(ImageId=config.ami_id,
                                     InstanceType=config.instance_type,
                                     SecurityGroups=config.security_group,
                                     KeyName=config.key_name,
                                     UserData=config.userdata,
                                     MinCount=1,
                                     MaxCount=num_create)
    id_list = []
    id_port_list = []
    for ins in instances:
        id_list.append(ins.id)
        id_port_list.append({'Id': ins.id, 'Port': 80})

    ec2.create_tags(Resources=id_list, Tags=[{'Key': 'Name', 'Value': 'a1-worker'}])
    register_instance.apply_async(args=[id_list, id_port_list], countdown=60)

    return redirect(url_for('admin'))


@celery.task
def register_instance(id_list, id_port_list):
    print 'begin celery register task'

    while not all_instances_running(id_list):
        print 'not all new instances running'

    print 'all running, begin registering'

    elb = boto3.client('elbv2', **config.conn_args)
    elb.register_targets(TargetGroupArn=config.ARN, Targets=id_port_list)

    print 'celery register task done'


def all_instances_running(id_list):
    ec2 = boto3.resource('ec2', **config.conn_args)
    for i in id_list:
        ins = ec2.Instance(i)
        if ins.state['Name'] != 'running':
            return False
    return True


@webapp.route('/admin/destroy', methods=['POST'])
def ec2_destroy():
    num_destroy = int(request.form.get('num-del'))
    ec2 = boto3.resource('ec2', **config.conn_args)
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
