import os
import joblib
import pandas as pd
import numpy as np
import random
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

predictions_bp = Blueprint('predictions', __name__)

# Base directory for models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, 'ml')

# Load models lazily
def load_ml_models():
    """Load all ML models and assets."""
    models = {}
    
    # Inflow Model
    inflow_path = os.path.join(ML_DIR, 'inflowcheck', 'inflow_model.pkl')
    if os.path.exists(inflow_path):
        models['inflow'] = joblib.load(inflow_path)
    
    # Disease Model and Assets
    disease_dir = os.path.join(ML_DIR, 'diseaseprediction')
    if os.path.exists(os.path.join(disease_dir, 'disease_model.pkl')):
        models['disease'] = joblib.load(os.path.join(disease_dir, 'disease_model.pkl'))
        models['disease_encoder'] = joblib.load(os.path.join(disease_dir, 'label_encoder.pkl'))
        models['disease_columns'] = joblib.load(os.path.join(disease_dir, 'symptom_columns.pkl'))
        
    return models

# Cache models
_models = None

def get_models():
    global _models
    if _models is None:
        _models = load_ml_models()
    return _models


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

# --- Real Prediction Routes ---

@predictions_bp.route('/predict-inflow', methods=['POST'])
@jwt_required()
def predict_inflow():
    """Predict inflow for a specific date given by GUI."""
    data = request.get_json()
    date_str = data.get('date')
    
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
        
    try:
        models = get_models()
        if 'inflow' not in models:
            return jsonify({'error': 'Inflow model not found'}), 500
            
        date_obj = pd.to_datetime(date_str)
        day_ordinal = date_obj.toordinal()
        
        prediction = models['inflow'].predict([[day_ordinal]])
        
        return jsonify({
            'date': date_str,
            'predicted_inflow': int(prediction[0]),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@predictions_bp.route('/predict-disease', methods=['POST'])
@jwt_required()
def predict_disease():
    """Predict disease based on symptoms given by GUI."""
    data = request.get_json()
    symptoms = data.get('symptoms', []) # Should be a list or comma separated string
    
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(",")]
    
    if not symptoms:
        return jsonify({'error': 'Symptoms are required'}), 400
        
    try:
        models = get_models()
        if 'disease' not in models:
            return jsonify({'error': 'Disease model not found'}), 500
            
        columns = models['disease_columns']
        encoder = models['disease_encoder']
        model = models['disease']
        
        # Create input vector
        input_data = np.zeros(len(columns))
        found_symptoms = []
        
        for s in symptoms:
            if s in columns:
                input_data[columns.index(s)] = 1
                found_symptoms.append(s)
            
        if not found_symptoms:
             return jsonify({
                 'error': 'No matching symptoms found. Please provide valid symptoms.',
                 'available_symptoms_sample': columns[:10]
             }), 400

        # Predict
        prediction = model.predict([input_data])
        disease = encoder.inverse_transform(prediction)[0]
        
        return jsonify({
            'disease': disease,
            'provided_symptoms': symptoms,
            'matched_symptoms': found_symptoms,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
