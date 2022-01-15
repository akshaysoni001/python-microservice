
from crypt import methods
from email.policy import default
import json
from math import prod
from os import abort
import string
import requests
from flask import Flask,jsonify
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from producer import publish


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@db/main"
CORS(app)

db=SQLAlchemy(app)

@dataclass # its beacuse json object is not serializable
class Product(db.Model):
    id: int # becuse it was showing empty data
    title: str
    image: str
    likes: int
    comment:str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    likes = db.Column(db.Integer,default=0)
    comment=  db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id=db.Column(db.Integer)



@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/product/<int:id>/like',methods=['POST'])
def like(id):
    req = requests.get('http://backend:8000/api/user')
    data = json.loads(req.text)
    print(data)
    try:
        
        productUser = ProductUser(user_id=data['id'],product_id=id)
        db.session.add(productUser)
        db.session.commit()

        product = Product.query.get(id)
        product.likes = product.likes + 1
        db.session.commit()

        publish('product_liked',id)

    except:
        abort(400,"You already liked this product")
        # abort()
    
    return jsonify({
        'message':'sucess'
    })

@app.route('/api/product/<int:id>/comment/<string:comment>',methods=['POST'])
def comment(id,comment):
    req = requests.get('http://backend:8000/api/user')
    data = json.loads(req.text)

    try:
        product = Product.query.get(id)
        product.comment = str(comment)
        db.session.commit()

        publish(comment,id)

    except:
        abort(400,"Product not found")
    
    return jsonify({
            'message':'sucess'
    })






if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0')