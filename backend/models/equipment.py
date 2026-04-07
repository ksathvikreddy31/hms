from extensions import db


class Equipment(db.Model):
    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80))
    department = db.Column(db.String(80))
    status = db.Column(db.String(20), default='operational')
    serial_number = db.Column(db.String(40))
    purchase_date = db.Column(db.DateTime)
    last_maintenance = db.Column(db.DateTime)
    next_maintenance = db.Column(db.DateTime)
    cost = db.Column(db.Float)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'category': self.category,
                'department': self.department, 'status': self.status,
                'serial_number': self.serial_number,
                'next_maintenance': self.next_maintenance.isoformat() if self.next_maintenance else None,
                'cost': self.cost}
