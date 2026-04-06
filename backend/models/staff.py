from extensions import db


class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30))
    department = db.Column(db.String(80))
    specialization = db.Column(db.String(120))
    shift = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role,
                'department': self.department, 'specialization': self.specialization,
                'shift': self.shift, 'status': self.status}
