from flask import Flask

webapp = Flask(__name__)

from app import upload
from app import login
from app import view
from app import admin
