from __future__ import division

from datetime import datetime, timedelta
from operator import itemgetter

import boto3
import mysql.connector
from flask import g

import config
from master_app import master
from master_app.config import db_config


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@master.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class ServerError(Exception):
    pass


def get_cpu_stats(instance_id):
    client = boto3.client('cloudwatch', **config.conn_args)

    metric_name = 'CPUUtilization'

    #    CPUUtilization, NetworkIn, NetworkOut, NetworkPacketsIn,
    #    NetworkPacketsOut, DiskWriteBytes, DiskReadBytes, DiskWriteOps,
    #    DiskReadOps, CPUCreditBalance, CPUCreditUsage, StatusCheckFailed,
    #    StatusCheckFailed_Instance, StatusCheckFailed_System

    namespace = 'AWS/EC2'
    statistic = 'Average'  # could be Sum,Maximum,Minimum,SampleCount,Average

    cpu = client.get_metric_statistics(
        Period=1 * 60,
        StartTime=datetime.utcnow() - timedelta(seconds=60 * 60),
        EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
        MetricName=metric_name,
        Namespace=namespace,  # Unit='Percent',
        Statistics=[statistic],
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
    )

    cpu_stats = []

    for point in cpu['Datapoints']:
        hour = point['Timestamp'].hour
        minute = point['Timestamp'].minute
        time = hour + minute / 60
        cpu_stats.append([time, point['Average']])

    return sorted(cpu_stats, key=itemgetter(0))


def update_setting(field, value):
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''UPDATE setting SET ''' + field + '''=%s'''
    cursor.execute(query, (value,))
    cnx.commit()


def get_setting():
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''SELECT * FROM setting'''
    cursor.execute(query)
    row = cursor.fetchone()
    return row
