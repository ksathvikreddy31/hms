from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.staff import Staff
from models.bed import Bed
from models.equipment import Equipment
from models.medicine import Medicine
from decorators import role_required
from datetime import datetime

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


@hospital_bp.route('/staff/<int:id>', methods=['PUT'])
@jwt_required()
def update_staff(id):
    data = request.json
    staff = Staff.query.get_or_404(id)
    if 'status' in data:
        staff.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Staff updated successfully', 'data': {'staff': staff.to_dict()}})

@hospital_bp.route('/medicines', methods=['GET'])
@jwt_required()
def get_medicines():
    meds = Medicine.query.all()
    return jsonify({'message': 'Medicines fetched successfully', 'data': {'medicines': [m.to_dict() for m in meds]}})

@hospital_bp.route('/medicines', methods=['POST'])
@jwt_required()
def add_medicine():
    data = request.json
    try:
        expiry_date = None
        if data.get('expiry_date'):
            expiry_date = datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00'))
            
        med = Medicine(
            name=data.get('name'),
            category=data.get('category'),
            manufacturer=data.get('manufacturer'),
            stock=data.get('stock', 0),
            unit_price=data.get('unit_price', 0),
            batch_number=data.get('batch_number'),
            expiry_date=expiry_date,
            reorder_level=data.get('reorder_level', 10),
            supplier=data.get('supplier')
        )
        db.session.add(med)
        db.session.commit()
        return jsonify({'message': 'Medicine added successfully', 'data': {'medicine': med.to_dict()}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e), 'data': None}), 400

@hospital_bp.route('/medicines/bulk', methods=['POST'])
@jwt_required()
def bulk_add_medicines():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part', 'data': None}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'message': 'Please upload a CSV file', 'data': None}), 400

    try:
        import csv
        import io
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        
        added_count = 0
        for row in reader:
            expiry_date = None
            if row.get('expiry_date'):
                try:
                    expiry_date = datetime.fromisoformat(row['expiry_date'].replace('Z', '+00:00'))
                except:
                    pass
            
            med = Medicine(
                name=row.get('name'),
                category=row.get('category'),
                manufacturer=row.get('manufacturer'),
                stock=int(row.get('stock', 0)),
                unit_price=float(row.get('unit_price', 0)),
                batch_number=row.get('batch_number'),
                expiry_date=expiry_date,
                reorder_level=int(row.get('reorder_level', 10)),
                supplier=row.get('supplier')
            )
            db.session.add(med)
            added_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Successfully imported {added_count} medicines', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e), 'data': None}), 500

@hospital_bp.route('/medicines/low-stock', methods=['GET'])
@role_required(['doctor'])
def get_low_stock_medicines():
    meds = Medicine.query.filter(Medicine.stock < 100).all()
    return jsonify({'message': 'Low stock medicines fetched', 'data': {'medicines': [m.to_dict() for m in meds]}})

@hospital_bp.route('/medicines/<int:id>', methods=['PUT'])
@jwt_required()
def update_medicine(id):
    data = request.json
    med = Medicine.query.get_or_404(id)
    try:
        if 'name' in data: med.name = data['name']
        if 'category' in data: med.category = data['category']
        if 'manufacturer' in data: med.manufacturer = data['manufacturer']
        if 'stock' in data: med.stock = data['stock']
        if 'unit_price' in data: med.unit_price = data['unit_price']
        if 'batch_number' in data: med.batch_number = data['batch_number']
        if 'reorder_level' in data: med.reorder_level = data['reorder_level']
        if 'supplier' in data: med.supplier = data['supplier']
        if 'expiry_date' in data and data['expiry_date']:
            med.expiry_date = datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00'))
        
        db.session.commit()
        return jsonify({'message': 'Medicine updated successfully', 'data': {'medicine': med.to_dict()}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e), 'data': None}), 400

@hospital_bp.route('/beds/<int:id>', methods=['PUT'])
@jwt_required()
def update_bed(id):
    data = request.json
    bed = Bed.query.get_or_404(id)
    if 'status' in data:
        bed.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Bed updated successfully', 'data': {'bed': bed.to_dict()}})

@hospital_bp.route('/equipment/<int:id>', methods=['PUT'])
@jwt_required()
def update_equipment(id):
    data = request.json
    equip = Equipment.query.get_or_404(id)
    if 'status' in data:
        equip.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Equipment updated successfully', 'data': {'equipment': equip.to_dict()}})
