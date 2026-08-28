from flask import request, jsonify
from marshmallow import ValidationError
from application.extensions import db, cache
from application.models import Mechanic
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
@cache.cached(timeout=60) # Cached for 60s to reduce repetitive database queries on this read-heavy route
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': f'Mechanic id {mechanic_id} deleted successfully'}), 200

@mechanics_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    mechanics = db.session.query(Mechanic).all()
    mechanics.sort(key=lambda mechanic: len(mechanic.tickets), reverse=True)
    return mechanics_schema.jsonify(mechanics), 200