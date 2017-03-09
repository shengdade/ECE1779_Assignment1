from celery import Celery
from flask import Flask

master = Flask(__name__)

master.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

celery = Celery(master.name, broker=master.config['CELERY_BROKER_URL'])
celery.conf.update(master.config)

from master_app import admin
from master_app import setting
