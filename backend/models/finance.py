from extensions import db


class FinanceRecord(db.Model):
    __tablename__ = 'finance_records'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(20))  # revenue, expense
    category = db.Column(db.String(60))
    amount = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'id': self.id, 'record_type': self.record_type,
                'category': self.category, 'amount': self.amount,
                'department': self.department, 'description': self.description,
                'date': self.date.isoformat() if self.date else None}
