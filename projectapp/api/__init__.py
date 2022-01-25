from flask import Blueprint
apiobj = Blueprint('bpapi', __name__,url_prefix='/test/api')

from . import api_routes