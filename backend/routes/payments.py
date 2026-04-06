from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.payment import Payment
from models.billing import Billing
from models.finance import FinanceRecord
from models.patient import Patient
from models.user import User
from decorators import role_required

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/process', methods=['POST'])
@jwt_required()
def process_payment():
    data = request.get_json()
    if 'billing_id' not in data:
        return jsonify({'message': 'billing_id is required', 'data': None}), 400
        
    billing = Billing.query.get_or_404(data['billing_id'])
    
    # Ownership Validation
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role == 'patient':
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient or billing.patient_id != patient.id:
            return jsonify({'message': 'Access forbidden', 'data': None}), 403

    if billing.status == 'paid':
        return jsonify({'message': 'Bill is already paid', 'data': None}), 400

    payment = Payment(billing_id=billing.id, amount=billing.total, method=data.get('method', 'cash'))
    billing.status = 'paid'
    # Create finance record
    fr = FinanceRecord(record_type='revenue', category='patient_payment',
                       amount=billing.total, department='Billing',
                       description=f'Payment for bill #{billing.id}')
    db.session.add(payment)
    db.session.add(fr)
    db.session.commit()
    return jsonify({'message': 'Payment processed successfully', 'data': {'payment': payment.to_dict()}})


@payments_bp.route('/', methods=['GET'])
@role_required(['admin']) # Only admin should see all hospital payments. Or maybe billing department?
def get_payments():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return jsonify({'message': 'Payments fetched successfully', 'data': {'payments': [p.to_dict() for p in payments]}})
