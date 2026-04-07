from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.appointment import Appointment
from models.patient import Patient
from models.user import User
from models.notification import Notification
from decorators import role_required

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/slots', methods=['GET'])
@jwt_required()
def get_slots():
    doctor_id = request.args.get('doctor_id')
    date_str = request.args.get('date')
    if not doctor_id or not date_str:
        return jsonify({'message': 'doctor_id and date are required', 'data': None}), 400
        
    from models.staff import Staff
    doctor = Staff.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found', 'data': None}), 404
        
    all_slots = ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM']
    
    from sqlalchemy import func
    from sqlalchemy import func, or_
    booked = Appointment.query.filter(
        or_(
            Appointment.doctor_name == doctor.name,
            Appointment.doctor_name == f"Dr. {doctor.name}",
            Appointment.doctor_name.contains(doctor.name)
        ),
        func.date(Appointment.date) == date_str,
        Appointment.status != 'cancelled'
    ).all()
    
    booked_slots = [b.time_slot for b in booked]
    available_slots = [s for s in all_slots if s not in booked_slots]
    
    return jsonify({'message': 'Slots fetched successfully', 'data': {'slots': available_slots}})


@appointments_bp.route('/all', methods=['GET'])
@role_required(['doctor'])
def get_appointments_all():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return jsonify({'message': 'Appointments fetched successfully', 'data': {'appointments': [a.to_dict() for a in appointments]}})

@appointments_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments_mine():
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({'message': 'Patient profile not found', 'data': {'appointments': []}})
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc()).all()
    return jsonify({'message': 'Appointments fetched successfully', 'data': {'appointments': [a.to_dict() for a in appointments]}})

@appointments_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    patient_id = data.get('patient_id')
    if user.role == 'patient':
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            patient = Patient(user_id=user.id)
            db.session.add(patient)
            db.session.commit()
        patient_id = patient.id
    elif not patient_id:
        return jsonify({'message': 'patient_id is required', 'data': None}), 400

    
    from datetime import datetime
    date_obj = None
    date_str = data.get('date')
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    appt = Appointment(
        patient_id=patient_id,
        doctor_name=data.get('doctor_name'),
        department=data.get('department'),
        date=date_obj,
        time_slot=data.get('time_slot', '10:00 AM'),
        notes=data.get('notes', '')
    )
    db.session.add(appt)
    
    # Generate notification
    if user.role == 'patient':
        notif = Notification(
            user_id=user.id,
            type='success',
            title='Appointment Confirmed',
            message=f"Your appointment with {data.get('doctor_name')} on {date_str} at {data.get('time_slot', '10:00 AM')} is confirmed."
        )
        db.session.add(notif)
    elif patient_id:
        p = Patient.query.get(patient_id)
        if p and p.user_id:
            notif = Notification(
                user_id=p.user_id,
                type='success',
                title='Appointment Scheduled',
                message=f"An appointment was scheduled with {data.get('doctor_name')} on {date_str} at {data.get('time_slot', '10:00 AM')}."
            )
            db.session.add(notif)

    db.session.commit()
    return jsonify({'message': 'Appointment booked', 'data': {'appointment': appt.to_dict()}}), 201

@appointments_bp.route('/<int:aid>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(aid):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    appt = Appointment.query.get_or_404(aid)
    
    if user.role == 'patient':
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient or appt.patient_id != patient.id:
            return jsonify({'message': 'Access forbidden', 'data': None}), 403
            
        notif = Notification(
            user_id=user.id,
            type='warning',
            title='Appointment Cancelled',
            message=f"Your appointment with {appt.doctor_name} has been cancelled."
        )
        db.session.add(notif)
    else:
        p = Patient.query.get(appt.patient_id)
        if p and p.user_id:
            notif = Notification(
                user_id=p.user_id,
                type='warning',
                title='Appointment Cancelled',
                message=f"Your appointment with {appt.doctor_name} was cancelled by the hospital."
            )
            db.session.add(notif)

    appt.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Appointment cancelled', 'data': {'appointment': appt.to_dict()}})
