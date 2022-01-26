from flask import Blueprint, blueprints
from flask_restx import Api

apiobj = Blueprint('bpapi', __name__,url_prefix='/test/api')
# blueprint = Blueprint('api', __name__)
api= Api(apiobj)

from . import api_routes