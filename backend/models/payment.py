from extensions import db
import uuid


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(20), default='cash')
    transaction_id = db.Column(db.String(40), default=lambda: f'TXN-{uuid.uuid4().hex[:12].upper()}')
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    billing = db.relationship('Billing', backref='payments')

    def to_dict(self):
        return {'id': self.id, 'billing_id': self.billing_id,
                'amount': self.amount, 'method': self.method,
                'transaction_id': self.transaction_id, 'status': self.status,
                'created_at': self.created_at.isoformat() if self.created_at else None}
