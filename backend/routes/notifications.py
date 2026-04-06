from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.notification import Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    # Get user's notifications, ordered by newest first
    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return jsonify({
        'message': 'Notifications fetched successfully',
        'data': {'notifications': [n.to_dict() for n in notifs]}
    })

@notifications_bp.route('/mark-read', methods=['PUT'])
@jwt_required()
def mark_all_read():
    user_id = int(get_jwt_identity())
    Notification.query.filter_by(user_id=user_id, read=False).update({'read': True})
    db.session.commit()
    return jsonify({'message': 'All notifications marked as read', 'data': None})

@notifications_bp.route('/<int:id>/mark-read', methods=['PUT'])
@jwt_required()
def mark_one_read(id):
    user_id = int(get_jwt_identity())
    notif = Notification.query.get_or_404(id)
    if notif.user_id != user_id:
        return jsonify({'message': 'Access forbidden', 'data': None}), 403
    
    notif.read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked as read', 'data': {'notification': notif.to_dict()}})

@notifications_bp.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    # Only for testing/internal use actually, or an admin creating a notification for a user
    data = request.get_json()
    new_notif = Notification(
        user_id=data.get('user_id'),
        type=data.get('type', 'info'),
        title=data.get('title'),
        message=data.get('message')
    )
    db.session.add(new_notif)
    db.session.commit()
    return jsonify({'message': 'Notification created', 'data': {'notification': new_notif.to_dict()}})
