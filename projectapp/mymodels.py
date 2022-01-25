import datetime
from enum import unique

from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



product_category = db.Table('product_category',
            db.Column('product_id',db.Integer, db.ForeignKey('products.id')),
            db.Column('category_id',db.Integer, db.ForeignKey('category.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_username = db.Column(db.String(30),nullable=False,unique=True)
    user_email = db.Column(db.String(60),nullable=False)
    user_password = db.Column(db.String(200),nullable=False)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return "You're unauthorized to access this page"

class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    prod_title = db.Column(db.String(40),nullable=False)
    prod_description = db.Column(db.String(150),nullable=False)
    prod_price = db.Column(db.Float(11),nullable=False)
    prod_image = db.Column(db.String(255),nullable=False)
    prod_date_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    prod_date_updated = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    prod_cat = db.relationship('Category',secondary=product_category,backref='prods')

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cat_name = db.Column(db.String(40),nullable=False)
    cat_description = db.Column(db.String(150),nullable=False)


# c = Category()
# p = Products()
# p.prod_cat.append(c)
# db.session.add(p)
# db.session.commit()