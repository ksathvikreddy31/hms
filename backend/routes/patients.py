from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.patient import Patient
from models.user import User
from models.notification import Notification
from decorators import role_required

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/all', methods=['GET'])
@role_required(['doctor']) # Admin automatically gets access via decorator
def get_patients():
    patients = Patient.query.all()
    return jsonify({'message': 'Patients fetched successfully', 'data': {'patients': [p.to_dict() for p in patients]}})

@patients_bp.route('/profile', methods=['GET'])
@jwt_required()
def my_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({'message': 'Profile not found', 'data': None}), 404
    return jsonify({'message': 'Profile fetched successfully', 'data': {'patient': patient.to_dict()}})

@patients_bp.route('/full-profile', methods=['GET'])
@jwt_required()
def my_full_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({'message': 'Profile not found', 'data': None}), 404
    # Include related data if necessary. For now returning patient to_dict
    return jsonify({'message': 'Full profile fetched successfully', 'data': {'patient': patient.to_dict()}})

@patients_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_my_profile():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    
    # Auto-create patient record if it doesn't exist
    if not patient:
        patient = Patient(user_id=user_id)
        db.session.add(patient)
    
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = ['gender', 'blood_group', 'dob', 'age', 'bmi', 'allergies', 'emergency_contact']
    for key in allowed_fields:
        if key in data:
            setattr(patient, key, data[key])
    
    # Also allow updating user name
    if 'name' in data:
        user = User.query.get(user_id)
        if user:
            user.name = data['name']
            
    # Notify user about profile update
    notif = Notification(
        user_id=user_id,
        type='info',
        title='Profile Updated',
        message='Your personal information has been successfully updated.'
    )
    db.session.add(notif)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'data': {'patient': patient.to_dict()}})

@patients_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    user_id = int(get_jwt_identity())
    patient = Patient.query.get_or_404(id)
    
    # Check ownership
    from models.user import User
    user = User.query.get(user_id)
    if user.role == 'patient' and patient.user_id != user_id:
        return jsonify({'message': 'Access forbidden', 'data': None}), 403
        
    data = request.json
    for key, value in data.items():
        if hasattr(patient, key) and key not in ['id', 'user_id', 'created_at']:
            setattr(patient, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Patient updated successfully', 'data': {'patient': patient.to_dict()}})

@patients_bp.route('/<int:id>', methods=['DELETE'])
@role_required(['admin']) # Ensure only admin can delete patient records
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully', 'data': None})
