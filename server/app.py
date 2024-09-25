#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# GET all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

# GET a bakery by ID
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

# PATCH request to update a bakery's name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        data = request.form
        bakery.name = data.get('name', bakery.name)
        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

# GET baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(jsonify(baked_goods_by_price_serialized), 200)

# POST request to create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=data.get('price'),
        bakery_id=data.get('bakery_id')
    )
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(jsonify(new_baked_good.to_dict()), 201)

# DELETE request to delete a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response(jsonify({"message": "Baked good successfully deleted"}), 200)
    else:
        return make_response(jsonify({"error": "Baked good not found"}), 404)

# GET the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if most_expensive:
        return make_response(jsonify(most_expensive.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
