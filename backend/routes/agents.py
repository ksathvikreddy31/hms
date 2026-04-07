from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import random
from datetime import datetime
import sys
import os

# Add agents folder to path so backend can import it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from agents.orchestrator import handle_query
except ImportError:
    handle_query = None

agents_bp = Blueprint('agents', __name__)

# In-memory activity log
agent_activities = []

AGENT_PROFILES = {
    'medical': {'name': 'Medical Agent', 'icon': '🩺', 'domain': 'Clinical Operations'},
    'operations': {'name': 'Operations Agent', 'icon': '⚙️', 'domain': 'Hospital Logistics'},
    'finance': {'name': 'Finance Agent', 'icon': '💰', 'domain': 'Financial Management'},
    'ceo': {'name': 'CEO Agent', 'icon': '👔', 'domain': 'Strategic Decisions'},
}

SCENARIOS = {
    'high_patient_load': [
        {'agent': 'medical', 'action': 'Detected 40% surge in ER admissions', 'status': 'alert', 'recommendation': 'Activate overflow protocol'},
        {'agent': 'operations', 'action': 'Reallocating 12 beds from General Ward to ER', 'status': 'executing', 'recommendation': 'Deploy 4 additional nurses'},
        {'agent': 'finance', 'action': 'Approved emergency staffing budget ₹2.5L', 'status': 'approved', 'recommendation': 'Track overtime costs'},
        {'agent': 'ceo', 'action': 'Final approval: Emergency protocol activated', 'status': 'final_approval', 'recommendation': 'Monitor situation hourly'},
    ],
    'medicine_shortage': [
        {'agent': 'medical', 'action': 'Critical shortage: Insulin Glargine stock at 5 units', 'status': 'critical', 'recommendation': 'Switch to alternative insulin'},
        {'agent': 'operations', 'action': 'Emergency order placed with Novo Nordisk distributor', 'status': 'executing', 'recommendation': 'ETA 24 hours'},
        {'agent': 'finance', 'action': 'Emergency procurement budget ₹1.8L approved', 'status': 'approved', 'recommendation': 'Update reorder levels'},
        {'agent': 'ceo', 'action': 'Approved vendor fast-track. Review supplier contracts.', 'status': 'final_approval', 'recommendation': 'Negotiate bulk pricing'},
    ],
    'cost_optimization': [
        {'agent': 'finance', 'action': 'Identified 18% overspend in Lab department', 'status': 'alert', 'recommendation': 'Audit lab consumable usage'},
        {'agent': 'operations', 'action': 'Proposing shared reagent procurement across labs', 'status': 'executing', 'recommendation': 'Potential savings ₹4.2L/month'},
        {'agent': 'medical', 'action': 'Validated: No impact on diagnostic quality', 'status': 'approved', 'recommendation': 'Maintain current test protocols'},
        {'agent': 'ceo', 'action': 'Approved cost optimization plan. Implement next quarter.', 'status': 'final_approval', 'recommendation': 'Monthly review scheduled'},
    ],
}


@agents_bp.route('/trigger', methods=['POST'])
@jwt_required()
def trigger_agents():
    data = request.get_json()
    scenario = data.get('scenario', 'high_patient_load')
    activities = SCENARIOS.get(scenario, SCENARIOS['high_patient_load'])
    timestamp = datetime.utcnow().isoformat()
    for a in activities:
        entry = {**a, 'timestamp': timestamp, 'scenario': scenario}
        agent_activities.insert(0, entry)
    return jsonify({'message': f'Scenario "{scenario}" triggered', 'activities': activities})


@agents_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_activity():
    limit = request.args.get('limit', 30, type=int)
    return jsonify({'activities': agent_activities[:limit], 'profiles': AGENT_PROFILES})


@agents_bp.route('/chat', methods=['POST'])
@jwt_required(optional=True)
def ufo_chat():
    """Endpoint for the UFO AI Assistant (Step 2 Implementation)."""
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
        
    if handle_query:
        # Extract patient_id from JWT if available, or from frontend_state
        patient_id = None
        try:
            # Try to get from JWT (if user is logged in)
            from flask_jwt_extended import get_jwt_identity
            user_id = get_jwt_identity()
            if user_id:
                from models.user import User
                user = User.query.get(int(user_id))
                if user and user.role == 'patient':
                    # Get patient record for this user
                    from models.patient import Patient
                    patient = Patient.query.filter_by(user_id=user.id).first()
                    if patient:
                        patient_id = patient.id
        except:
            # JWT not present or invalid, try frontend_state
            patient_id = data.get('patient_id') or data.get('frontend_state', {}).get('patient_id')
        
        # Calls the actual UFO orchestrator
        frontend_state = data.get('frontend_state', {})
        user_role = "unknown"
        try:
            from models.user import User
            user = User.query.get(int(user_id)) if user_id else None
            if user:
                user_role = user.role or "unknown"
                if user.role == 'patient':
                    from models.patient import Patient
                    patient = Patient.query.filter_by(user_id=user.id).first()
                    if patient:
                        patient_id = patient.id
        except Exception:
            pass

        if frontend_state.get('user_role'):
            user_role = frontend_state['user_role']

        context = {
            "endpoint": "/api/agents/chat",
            "frontend_state": frontend_state,
            "patient_id": patient_id,
            "user_role": user_role,
        }
        result = handle_query(query, context=context)
        return jsonify(result)
    else:
        return jsonify({"error": "AI Orchestrator not loaded properly"}), 500
