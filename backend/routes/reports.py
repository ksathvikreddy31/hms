from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.report import Report
from models.user import User
from models.patient import Patient

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'patient':
        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            return jsonify({'message': 'Patient profile not found', 'data': {'reports': []}})
        reports = Report.query.filter_by(patient_id=patient.id).all()
    else:
        # For simplicity, returning all for doctors/admin initially
        reports = Report.query.all()
        
    return jsonify({
        'message': 'Reports fetched successfully',
        'data': {'reports': [r.to_dict() for r in reports]}
    })

@reports_bp.route('/', methods=['POST'])
@jwt_required()
def add_report():
    data = request.json
    new_report = Report(
        patient_id=data.get('patient_id'),
        doctor_name=data.get('doctor_name'),
        visit_date=db.func.current_timestamp(),
        diagnosis=data.get('diagnosis'),
        suggestions=data.get('suggestions')
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify({
        'message': 'Report added successfully',
        'data': {'report': new_report.to_dict()}
    })
