from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.billing import Billing
from models.patient import Patient
from models.user import User
from decorators import role_required
import json

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/all', methods=['GET'])
@role_required(['doctor', 'admin'])
def get_billings_all():
    billings = Billing.query.order_by(Billing.created_at.desc()).all()
    return jsonify({'message': 'All billings fetched', 'data': {'billings': [b.to_dict() for b in billings]}})

@billing_bp.route('/', methods=['GET'])
@jwt_required()
def get_billings_mine():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({'message': 'Patient profile not found', 'data': {'billings': []}})
    billings = Billing.query.filter_by(patient_id=patient.id).order_by(Billing.created_at.desc()).all()
    return jsonify({'message': 'My billings fetched', 'data': {'billings': [b.to_dict() for b in billings]}})

@billing_bp.route('/generate', methods=['POST'])
@role_required(['doctor', 'admin'])
def generate_bill():
    data = request.get_json()
    items = data.get('items', [])
    patient_id = data.get('patient_id')
    
    if not patient_id:
        return jsonify({'message': 'patient_id is required', 'data': None}), 400
        
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found', 'data': None}), 404

    subtotal = sum(i['rate'] * i['quantity'] for i in items)
    tax = subtotal * 0.05
    discount = data.get('discount', 0)
    total = subtotal + tax - discount
    bill = Billing(
        patient_id=patient_id,
        items=json.dumps(items),
        subtotal=round(subtotal, 2),
        tax=round(tax, 2),
        discount=round(discount, 2),
        total=round(total, 2)
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({'message': 'Bill generated successfully', 'data': {'billing': bill.to_dict()}}), 201
