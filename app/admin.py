import boto3
from flask import redirect, url_for

import config
from app import webapp


@webapp.route('/ec2_examples/create', methods=['POST'])
# Start a new EC2 instance
def ec2_create():
    ec2 = boto3.resource('ec2')

    ec2.create_instances(ImageId=config.ami_id,
                         InstanceType=config.instance_type,
                         SecurityGroups=config.security_group,
                         KeyName=config.key_name,
                         MinCount=1,
                         MaxCount=1)

    return redirect(url_for('admin'))
