from celery import Celery
from flask import Flask

webapp = Flask(__name__)

webapp.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

celery = Celery(webapp.name, broker=webapp.config['CELERY_BROKER_URL'])
celery.conf.update(webapp.config)

from app import upload
from app import login
from app import view
from app import admin
