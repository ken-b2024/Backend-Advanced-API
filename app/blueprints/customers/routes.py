from.import customers_bp
from.schemas import Customer, customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db
from sqlalchemy import select, delete


@customers_bp.route("/", methods=['POST'])
def create_customer():

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], make_model=customer_data['make_model'], VIN=customer_data['VIN'])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"New customer has been created successfully": customer_schema.dump(new_customer)}),201

@customers_bp.route("/", methods=['GET'])
def get_customers():

    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return jsonify({"Customers": customers_schema.dump(result)}), 200

@customers_bp.route("/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):

    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Customer has been successfully updated": customer_schema.dump(customer)}), 200

@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):

    query = delete(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query)

    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer with ID: {customer_id}"})