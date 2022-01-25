from flask import Blueprint
adminobj = Blueprint('bpadmin', __name__, template_folder='templates', static_folder='static')

from . import admin_routes