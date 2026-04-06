from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists', 'data': None}), 400
    user = User(email=data['email'], name=data.get('name', ''), role=data.get('role', 'patient'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    if user.role == 'patient':
        from models.patient import Patient
        patient = Patient(user_id=user.id)
        db.session.add(patient)
        db.session.commit()
        
    return jsonify({'message': 'Registration successful', 'data': {'user': user.to_dict()}}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'message': 'Invalid credentials', 'data': None}), 401
    token = create_access_token(identity=str(user.id))
    
    # Keeping top-level token and user for aggressive frontend compatibility, 
    # but adhering to standard format too.
    return jsonify({'message': 'Login successful', 'token': token, 'user': user.to_dict(), 'data': {'token': token, 'user': user.to_dict()}})


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'message': 'User not found', 'data': None}), 404
    return jsonify({'message': 'User fetched successfully', 'data': {'user': user.to_dict()}})


@auth_bp.route('/switch-role', methods=['POST'])
@jwt_required()
def switch_role():
    data = request.get_json()
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'message': 'User not found', 'data': None}), 404
    new_role = data.get('role', 'patient')
    if new_role in ['patient', 'doctor', 'admin']:
        user.role = new_role
        db.session.commit()
        return jsonify({'message': f'Role switched to {new_role}', 'data': {'user': user.to_dict()}})
    return jsonify({'message': 'Invalid role', 'data': None}), 400
