from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import random
from datetime import datetime

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
