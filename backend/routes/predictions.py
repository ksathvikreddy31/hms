from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import random
from datetime import datetime, timedelta

predictions_bp = Blueprint('predictions', __name__)


def generate_time_series(days, base, variance):
    data = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days - i)).strftime('%Y-%m-%d')
        data.append({'date': date, 'value': int(base + random.uniform(-variance, variance))})
    return data


@predictions_bp.route('/patient-inflow', methods=['GET'])
@jwt_required()
def patient_inflow():
    return jsonify({
        'title': 'Patient Inflow Prediction',
        'confidence': 0.87,
        'historical': generate_time_series(30, 45, 15),
        'predicted': generate_time_series(7, 52, 10),
        'insight': '📈 Expected 15% increase in OPD visits next week due to seasonal trends.'
    })


@predictions_bp.route('/revenue', methods=['GET'])
@jwt_required()
def revenue_prediction():
    return jsonify({
        'title': 'Revenue Forecast',
        'confidence': 0.82,
        'historical': generate_time_series(30, 250000, 80000),
        'predicted': generate_time_series(7, 280000, 60000),
        'insight': '💰 Revenue projected to grow 12% next month with new cardiology cases.'
    })


@predictions_bp.route('/disease-trends', methods=['GET'])
@jwt_required()
def disease_trends():
    return jsonify({
        'title': 'Disease Outbreak Prediction',
        'description': 'AI-powered early warning system for disease patterns',
        'trends': [
            {'disease': 'Dengue', 'current_cases': 23, 'predicted_next_week': 31, 'trend': 'increasing', 'risk_level': 'high'},
            {'disease': 'Flu', 'current_cases': 45, 'predicted_next_week': 38, 'trend': 'decreasing', 'risk_level': 'medium'},
            {'disease': 'COVID-19', 'current_cases': 8, 'predicted_next_week': 10, 'trend': 'stable', 'risk_level': 'low'},
            {'disease': 'Typhoid', 'current_cases': 12, 'predicted_next_week': 18, 'trend': 'increasing', 'risk_level': 'medium'},
        ],
        'season_alert': '⚠️ Monsoon season approaching. Expect increased vector-borne diseases.'
    })


@predictions_bp.route('/resource-demand', methods=['GET'])
@jwt_required()
def resource_demand():
    return jsonify({
        'title': 'Resource Demand Forecast',
        'resources': [
            {'resource': 'ICU Beds', 'current': 8, 'predicted_need': 12, 'unit': 'beds'},
            {'resource': 'Ventilators', 'current': 5, 'predicted_need': 7, 'unit': 'units'},
            {'resource': 'Blood Units (O+)', 'current': 15, 'predicted_need': 22, 'unit': 'units'},
            {'resource': 'Nurses (Night)', 'current': 10, 'predicted_need': 14, 'unit': 'staff'},
            {'resource': 'Oxygen Cylinders', 'current': 30, 'predicted_need': 25, 'unit': 'units'},
            {'resource': 'PPE Kits', 'current': 200, 'predicted_need': 150, 'unit': 'kits'},
        ],
        'insight': '🔮 AI predicts ICU bed and ventilator shortage in 5 days. Initiate procurement.'
    })
