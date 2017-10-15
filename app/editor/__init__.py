from flask import Blueprint

app = Blueprint('editor', __name__)

from . import routes
