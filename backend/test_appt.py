from app import create_app
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
import json

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    user = User.query.filter_by(role='patient').first()
    if not user:
        print("No patient user found")
    else:
        token = create_access_token(identity=str(user.id))
        client = app.test_client()
        
        # Test book
        res = client.post('/api/appointments/', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'doctor_name': 'Test Doc',
            'department': 'Cardio',
            'date': '2026-10-10',
            'time_slot': '10:00 AM'
        })
        print("Book Status:", res.status_code)
        print("Book Data:", res.data.decode('utf-8'))
        
        # Test cancel
        if res.status_code == 201:
            aid = json.loads(res.data)['data']['appointment']['id']
            res_c = client.put(f'/api/appointments/{aid}/cancel', headers={
                'Authorization': f'Bearer {token}'
            })
            print("Cancel Status:", res_c.status_code)
            print("Cancel Data:", res_c.data.decode('utf-8'))
