from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.patient import Patient
from models.appointment import Appointment
from models.staff import Staff
from models.bed import Bed
from models.equipment import Equipment
from models.medicine import Medicine
from models.billing import Billing
from models.finance import FinanceRecord
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    total_patients = Patient.query.count()
    total_staff = Staff.query.count()
    total_beds = Bed.query.count()
    occupied_beds = Bed.query.filter_by(status='occupied').count()
    available_beds = Bed.query.filter_by(status='available').count()
    today_appointments = Appointment.query.filter_by(status='scheduled').count()
    total_revenue = db.session.query(func.sum(FinanceRecord.amount)).filter_by(record_type='revenue').scalar() or 0
    total_expense = db.session.query(func.sum(FinanceRecord.amount)).filter_by(record_type='expense').scalar() or 0
    pending_bills = Billing.query.filter_by(status='pending').count()
    low_stock = sum(1 for m in Medicine.query.all() if m.is_low_stock)
    equipment_maintenance = Equipment.query.filter_by(status='maintenance').count()

    # Department revenue
    dept_rev = db.session.query(
        FinanceRecord.department, func.sum(FinanceRecord.amount).label('total')
    ).filter_by(record_type='revenue').group_by(FinanceRecord.department).all()
    dept_data = [{'department': d, 'revenue': round(t, 2)} for d, t in dept_rev]

    # Bed occupancy by ward
    bed_stats = db.session.query(
        Bed.ward, Bed.status, func.count(Bed.id)
    ).group_by(Bed.ward, Bed.status).all()
    ward_data = {}
    for ward, status, count in bed_stats:
        if ward not in ward_data:
            ward_data[ward] = {'ward': ward, 'available': 0, 'occupied': 0}
        ward_data[ward][status] = count

    # Alerts
    alerts = []
    if low_stock > 0:
        alerts.append({'type': 'warning', 'message': f'{low_stock} medicines running low on stock'})
    if equipment_maintenance > 0:
        alerts.append({'type': 'info', 'message': f'{equipment_maintenance} equipment under maintenance'})
    if pending_bills > 0:
        alerts.append({'type': 'warning', 'message': f'{pending_bills} bills pending payment'})
    if occupied_beds / max(total_beds, 1) > 0.8:
        alerts.append({'type': 'danger', 'message': 'Bed occupancy above 80%'})

    return jsonify({
        'total_patients': total_patients, 'total_staff': total_staff,
        'total_beds': total_beds, 'occupied_beds': occupied_beds,
        'available_beds': available_beds, 'today_appointments': today_appointments,
        'total_revenue': round(total_revenue, 2),
        'total_expense': round(total_expense, 2),
        'net_profit': round(total_revenue - total_expense, 2),
        'pending_bills': pending_bills, 'low_stock_medicines': low_stock,
        'equipment_maintenance': equipment_maintenance,
        'department_revenue': dept_data,
        'bed_occupancy': list(ward_data.values()),
        'alerts': alerts
    })
