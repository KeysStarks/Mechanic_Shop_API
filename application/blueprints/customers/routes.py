from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, limiter
from application.models import Customer, ServiceTicket
from application.utils.util import encode_token, token_required
from . import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from application.blueprints.service_ticket.schemas import service_tickets_schema

@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.query(Customer).filter_by(email=email).first()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id)
        return jsonify({
            'status': 'success',
            'message': 'Successfully logged in',
            'auth_token': auth_token
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    tickets = db.session.query(ServiceTicket).filter_by(customer_id=customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200


@customers_bp.route('/', methods=['POST'])
@limiter.limit("3 per hour") # Rate limited to prevent abuse/spam account creation
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customers_bp.route('/', methods=['GET'])
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    return customer_schema.jsonify(customer), 200


@customers_bp.route('/', methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer id {customer_id} deleted successfully'}), 200