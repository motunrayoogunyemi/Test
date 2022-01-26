import json
from flask import jsonify,request
from flask_restx import Resource
from flask_restx import reqparse, fields
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from . import api
from projectapp.mymodels import Category, db, Products, User

model = api.model('Model', {
    'username': fields.String,
    'password': fields.String
})

postmodel = api.model('postmodel', {
    'ptitle': fields.String,
    'pdesc': fields.String,
    'pprice': fields.String,
    'pfile': fields.String
})

catmodel = api.model('catmodel', {
    'cname': fields.String,
    'cdesc': fields.String
})


@api.route('/login')
class log(Resource):
    @api.expect(model)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',location='form')
        parser.add_argument('password',location='form')
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        user = User.query.filter_by(user_username=username).first()
        if user:
            check = check_password_hash(user.user_password,password)
            if check:
                access_token = create_access_token(identity=username)
                return jsonify(access_token=access_token)
            return 'invalid'
        return 'user not found'

    

@api.route('/getall/')
class Any(Resource):
    def get(self):
        data = db.session.query(Products).all()
        if data:
            records = []
            for i in data:
                a={}
                a['prodTitle']=i.prod_title
                a['prodPrice']=i.prod_price
                a['prodFile']=i.prod_image
                a['prodDesc']=i.prod_description
                records.append(a)
            resp ={"status":1,"message":"successful","data":records}
        else:
            resp ={"status":0,"message":"Not found","data":[]}
        return jsonify(resp)
        

@api.route('/add/')
class Any2(Resource):
    @api.expect(postmodel)
    @jwt_required()
    def post(self):
        if request.is_json:
            data = request.get_json() 
            prodtitle = data.get('ptitle') 
            prodfile = data.get('pfile') 
            proddesc = data.get('pdesc')
            prodprice = data.get('pprice')        
            allproducts = Products(prod_title=prodtitle, prod_image=prodfile, prod_price=prodprice,prod_description=proddesc)
            db.session.add(allproducts)
            db.session.commit()
            pid = allproducts.id
            resp = {"status":1,"message":f"Successful,added product with id {pid}","data":{allproducts}}
            return jsonify(resp)
        else:
            resp = {"status":0,"message":"Bad Format, supply JSON","data":[]}
            return jsonify(resp)


@api.route('/products/<int:id>')
class oneproduct(Resource):
    def get(self, id):
        records = db.session.query(Products).get(id)
        rsp={"prodTitle":records.prod_title,"prodPrice":records.prod_price,"prodFile":records.prod_image,"prodDesc":records.prod_description}
        return jsonify(rsp)


    @api.expect(postmodel)
    @jwt_required()
    def put(self, id):
        data = request.get_json() 
        prodtitle = data['ptitle']  
        prodfile = data['pfile']  
        prodprice = data['pprice']    
        proddesc = data['pcontact']     
        oneproduct = db.session.query(Products).get(id)
        oneproduct.prod_title=prodtitle
        oneproduct.prod_description=proddesc
        oneproduct.prod_image=prodfile
        oneproduct.prod_price=prodprice
        db.session.commit()
        return 'product updated'

    @jwt_required()
    def delete(self, id):
        oneproduct = db.session.query(Products).get(id)
        db.session.delete(oneproduct)
        db.session.commit()
        return 'successfully deleted'
        


@api.route('/getallcategory/')
class cat(Resource):
    def get(self):
        data = db.session.query(Category).all()
        if data:
            allrecords = []
            for i in data:
                a={}
                a['catName']=i.cat_name
                a['catDesc']=i.cat_description
                allrecords.append(a)
            resp ={"status":1,"message":"successful","data":allrecords}
        else:
            resp ={"status":0,"message":"Not found","data":[]}
        return jsonify(resp)

@api.route('/addcategory/')
class cat2(Resource):
    @api.expect(catmodel)
    @jwt_required()
    def post(self):
        if request.is_json:
            data = request.get_json() 
            catname = data.get('cname') 
            catdesc = data.get('cdesc')       
            cats = Category(cat_name=catname, cat_description=catdesc)
            db.session.add(cats)
            db.session.commit()
            cid = cats.id
            resp = {"status":1,"message":f"Successful,added category with id {cid}","data":[]}
            return jsonify(resp)
        else:
            resp = {"status":0,"message":"Bad Format, supply JSON","data":[]}
            return jsonify(resp)

@api.route('/catgory/<int:id>')
class onecategory(Resource):
    def get(self, id):
        records = db.session.query(Category).get(id)
        rsp={"catName":records.cat_name,"catDesc":records.cat_description}
        return jsonify(rsp)


    @api.expect(catmodel)
    @jwt_required()
    def put(self, id):
        data = request.get_json() 
        catname = data['cname']  
        catdesc = data['cdesc']       
        onecategory = db.session.query(Category).get(id)
        onecategory.cat_name=catname
        onecategory.cat_description=catdesc
        db.session.commit()
        return 'category updated'

    @jwt_required()
    def delete(self, id):
        onecategory = db.session.query(Category).get(id)
        db.session.delete(onecategory)
        db.session.commit()
        return 'successfully deleted'