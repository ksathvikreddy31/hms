from extensions import db
import json


class Billing(db.Model):
    __tablename__ = 'billings'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)  # JSON
    subtotal = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    patient = db.relationship('Patient', backref='billings')

    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id,
                'items': json.loads(self.items) if self.items else [],
                'subtotal': self.subtotal, 'tax': self.tax,
                'discount': self.discount, 'total': self.total,
                'status': self.status,
                'created_at': self.created_at.isoformat() if self.created_at else None}
