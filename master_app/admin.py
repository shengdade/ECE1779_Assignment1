from __future__ import division

import math
import random
from datetime import timedelta

import boto3
import celery
from celery.task import periodic_task
from flask import redirect, url_for, request, render_template

import config
from master_app import master
from utils import get_cpu_stats, get_setting, get_db


@master.route('/index', methods=['GET'])
@master.route('/', methods=['GET'])
# Return html with pointers to the examples
def index():
    ec2 = boto3.resource('ec2', **config.conn_args)

    cpu_stats = []
    instance_list = []

    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-master']},
                 {'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        cpu_stats.append(get_cpu_stats(instance.id))
    instance_list.extend(list(instances))

    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-primary']},
                 {'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        cpu_stats.append(get_cpu_stats(instance.id))
    instance_list.extend(list(instances))

    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-worker']},
                 {'Name': 'instance-state-name', 'Values': ['running', 'pending']}])
    for instance in instances:
        cpu_stats.append(get_cpu_stats(instance.id))
    instance_list.extend(list(instances))

    return render_template('admin.html', cpu_stats=cpu_stats, instances=instance_list)


@master.route('/admin/create', methods=['POST'])
def ec2_create():
    num_create = int(request.form.get('num-new'))
    create_instances(num_create)
    return redirect(url_for('index'))


def create_instances(num_create):
    ec2 = boto3.resource('ec2', **config.conn_args)
    instances = ec2.create_instances(ImageId=config.ami_id,
                                     InstanceType=config.instance_type,
                                     SecurityGroups=config.security_group,
                                     KeyName=config.key_name,
                                     UserData=config.userdata,
                                     Monitoring={'Enabled': True},
                                     MinCount=1,
                                     MaxCount=num_create)
    id_list = []
    id_port_list = []
    for ins in instances:
        id_list.append(ins.id)
        id_port_list.append({'Id': ins.id, 'Port': 80})
    ec2.create_tags(Resources=id_list, Tags=[{'Key': 'Name', 'Value': 'a1-worker'}])
    register_instance.apply_async(args=[id_list, id_port_list], countdown=20)


@celery.task
def register_instance(id_list, id_port_list):
    print 'begin celery register task'

    while not all_new_workers_running(id_list):
        print 'not all new instances running'

    print 'all running, begin registering'

    elb = boto3.client('elbv2', **config.conn_args)
    elb.register_targets(TargetGroupArn=config.ARN, Targets=id_port_list)

    print 'celery register task done'


def all_new_workers_running(id_list):
    ec2 = boto3.resource('ec2', **config.conn_args)
    for i in id_list:
        ins = ec2.Instance(i)
        if ins.state['Name'] == 'pending':
            return False
    return True


def all_workers_running():
    ec2 = boto3.resource('ec2', **config.conn_args)
    preparing_workers = list(ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-worker', 'a1-primary']},
                 {'Name': 'instance-state-name', 'Values': ['pending', 'shutting-down']}]))
    return len(preparing_workers) == 0


@master.route('/admin/destroy', methods=['POST'])
def ec2_destroy():
    num_destroy = int(request.form.get('num-del'))
    if destroy_instances(num_destroy):
        return redirect(url_for('index'))
    else:
        return 'No worker can be further destroyed.'


def destroy_instances(num_destroy):
    ec2 = boto3.resource('ec2', **config.conn_args)
    workers = list(ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-worker']},
                 {'Name': 'instance-state-name', 'Values': ['running', 'pending']}]))
    if num_destroy > len(workers):
        return False
    else:
        random.shuffle(workers)
        for i in range(num_destroy):
            workers[i].terminate()
        return True


@master.route('/admin/delete-all', methods=['POST'])
def delete_all_images():
    # delete all images (keep users)
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''DELETE FROM images;'''
    cursor.execute(query)
    cnx.commit()

    # delete all objects of all buckets (keep bucket names)
    s3 = boto3.resource('s3', **config.conn_args)
    for bucket in s3.buckets.all():
        for obj in bucket.objects.all():
            obj.delete()

    return redirect(url_for('index'))


def mean(numbers):
    return sum(numbers) / max(len(numbers), 1)


@periodic_task(run_every=timedelta(seconds=60))
def check_status():
    ec2 = boto3.resource('ec2', **config.conn_args)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag-value', 'Values': ['a1-primary', 'a1-worker']},
                 {'Name': 'instance-state-name', 'Values': ['running']}])
    cpu_list = []
    for instance in instances:
        cpu_status = get_cpu_stats(instance.id)
        if len(cpu_status) > 0:
            cpu = cpu_status[-1][1]
            cpu_list.append(cpu)
    num_cpu = len(cpu_list)
    average = mean(cpu_list)
    print 'cpu average utilization is ' + str(average)

    with master.app_context():
        (auto_scaling, cpu_grow_threshold, cpu_shrink_threshold, ratio_expand, ratio_shrink) = get_setting()

    # Auto-scaling is on
    if auto_scaling == 1 and all_workers_running():

        # Average Utilization above threshold
        if average > cpu_grow_threshold:
            num_create = (ratio_expand - 1) * num_cpu
            print 'average above threshold, creating ' + str(num_create) + ' workers'
            create_instances(num_create)

        # Average Utilization below threshold
        elif average < cpu_shrink_threshold:
            num_destroy = num_cpu - int(math.ceil(num_cpu / ratio_shrink))
            if num_destroy > 0:
                print 'average below threshold, destroying ' + str(num_destroy) + ' workers'
                destroy_instances(num_destroy)
