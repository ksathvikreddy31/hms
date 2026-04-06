from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.finance import FinanceRecord
from sqlalchemy import func

finance_bp = Blueprint('finance', __name__)


@finance_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    total_rev = db.session.query(func.sum(FinanceRecord.amount)).filter_by(record_type='revenue').scalar() or 0
    total_exp = db.session.query(func.sum(FinanceRecord.amount)).filter_by(record_type='expense').scalar() or 0
    # Monthly data
    monthly = []
    records = db.session.query(
        func.strftime('%Y-%m', FinanceRecord.date).label('month'),
        FinanceRecord.record_type,
        func.sum(FinanceRecord.amount).label('total')
    ).group_by('month', FinanceRecord.record_type).order_by('month').all()
    month_data = {}
    for m, rtype, total in records:
        if m not in month_data:
            month_data[m] = {'month': m, 'revenue': 0, 'expense': 0, 'profit': 0}
        month_data[m][rtype] = round(total, 2)
    for m in month_data.values():
        m['profit'] = round(m['revenue'] - m['expense'], 2)
    monthly = list(month_data.values())[-6:]
    return jsonify({'total_revenue': round(total_rev, 2), 'total_expense': round(total_exp, 2),
                    'net_profit': round(total_rev - total_exp, 2), 'monthly': monthly})


@finance_bp.route('/department-analytics', methods=['GET'])
@jwt_required()
def department_analytics():
    results = db.session.query(
        FinanceRecord.department,
        func.sum(FinanceRecord.amount).label('revenue')
    ).filter_by(record_type='revenue').group_by(FinanceRecord.department).all()
    departments = [{'department': d, 'revenue': round(r, 2)} for d, r in results]
    return jsonify({'departments': departments})
