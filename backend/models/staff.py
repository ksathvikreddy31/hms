from extensions import db


class Staff(db.Model):
    __tablename__ = 'staff'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30))
    department = db.Column(db.String(80))
    specialization = db.Column(db.String(120))
    shift = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    unavailable_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role,
                'department': self.department, 'specialization': self.specialization,
                'shift': self.shift, 'status': self.status, 
                'unavailable_date': self.unavailable_date.isoformat() if self.unavailable_date else None}
