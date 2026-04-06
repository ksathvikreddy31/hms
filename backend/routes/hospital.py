from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.staff import Staff
from models.bed import Bed
from models.equipment import Equipment
from models.medicine import Medicine
from decorators import role_required

hospital_bp = Blueprint('hospital', __name__)


@hospital_bp.route('/staff', methods=['GET'])
@jwt_required()
def get_staff():
    staff = Staff.query.all()
    return jsonify({'message': 'Staff fetched successfully', 'data': {'staff': [s.to_dict() for s in staff]}})

@hospital_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    departments = db.session.query(Staff.department).filter(Staff.role == 'doctor').distinct().all()
    dept_list = [d[0] for d in departments if d[0]]
    if not dept_list:
        dept_list = ['Cardiology', 'Orthopedics', 'Neurology', 'Pediatrics', 'General Medicine']
    return jsonify({'message': 'Departments fetched successfully', 'data': {'departments': dept_list}})

@hospital_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    department = request.args.get('department')
    query = Staff.query.filter_by(role='doctor')
    if department:
        query = query.filter_by(department=department)
    return jsonify({'message': 'Doctors fetched successfully', 'data': {'doctors': [d.to_dict() for d in query.all()]}})



@hospital_bp.route('/beds', methods=['GET'])
@jwt_required()
def get_beds():
    beds = Bed.query.all()
    return jsonify({'message': 'Beds fetched successfully', 'data': {'beds': [b.to_dict() for b in beds]}})

@hospital_bp.route('/beds/assign', methods=['POST'])
@role_required(['doctor'])
def assign_bed():
    data = request.json
    bed_id = data.get('bed_id')
    patient_id = data.get('patient_id')
    
    if not bed_id or not patient_id:
        return jsonify({'message': 'bed_id and patient_id are required', 'data': None}), 400
        
    bed = Bed.query.get_or_404(bed_id)
    if bed.status != 'Available':
        return jsonify({'message': 'Bed is not available', 'data': None}), 400
        
    bed.patient_id = patient_id
    bed.status = 'Occupied'
    db.session.commit()
    
    return jsonify({'message': 'Bed assigned successfully', 'data': {'bed': bed.to_dict()}})

@hospital_bp.route('/beds/release', methods=['POST'])
@role_required(['doctor'])
def release_bed():
    data = request.json
    bed_id = data.get('bed_id')
    
    if not bed_id:
        return jsonify({'message': 'bed_id is required', 'data': None}), 400
        
    bed = Bed.query.get_or_404(bed_id)
    bed.patient_id = None
    bed.status = 'Available'
    db.session.commit()
    
    return jsonify({'message': 'Bed released successfully', 'data': {'bed': bed.to_dict()}})


@hospital_bp.route('/equipment', methods=['GET'])
@jwt_required()
def get_equipment():
    equip = Equipment.query.all()
    return jsonify({'message': 'Equipment fetched successfully', 'data': {'equipment': [e.to_dict() for e in equip]}})


@hospital_bp.route('/medicines', methods=['GET'])
@jwt_required()
def get_medicines():
    meds = Medicine.query.all()
    return jsonify({'message': 'Medicines fetched successfully', 'data': {'medicines': [m.to_dict() for m in meds]}})

@hospital_bp.route('/medicines/low-stock', methods=['GET'])
@role_required(['doctor'])
def get_low_stock_medicines():
    # Let's say threshold is 100 for now. Using < 100
    meds = Medicine.query.filter(Medicine.stock < 100).all()
    return jsonify({'message': 'Low stock medicines fetched', 'data': {'medicines': [m.to_dict() for m in meds]}})
