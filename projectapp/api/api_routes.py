import json
from flask import jsonify,request

from . import apiobj
from projectapp.mymodels import db


@apiobj.route('/getall/',methods=['GET'])
def getall():
    pass

@apiobj.route('/add/',methods=['POST'])
def add():
    pass

@apiobj.route('/getone/<int:id>/',methods=['GET'])
def getone(id):
    pass

@apiobj.route('/update/<int:id>/',methods=['PUT'])
def update(id):
    pass

@apiobj.route('/delete/<int:id>/',methods=['DELETE'])
def delete(id):
    pass