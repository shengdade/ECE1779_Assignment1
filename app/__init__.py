from flask import Flask

webapp = Flask(__name__)

from app import upload
from app import router
from app import view
