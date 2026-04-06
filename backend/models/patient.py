from extensions import db


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    bmi = db.Column(db.Float)
    conditions = db.Column(db.Text)  # JSON
    allergies = db.Column(db.Text)
    lifestyle = db.Column(db.Text)  # JSON
    emergency_contact = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('patient', uselist=False))

    def to_dict(self):
        import json
        return {'id': self.id, 'user_id': self.user_id,
                'name': self.user.name if self.user else None,
                'email': self.user.email if self.user else None,
                'age': self.age, 'gender': self.gender,
                'blood_group': self.blood_group, 'bmi': self.bmi,
                'conditions': json.loads(self.conditions) if self.conditions else [],
                'lifestyle': json.loads(self.lifestyle) if self.lifestyle else {}}
