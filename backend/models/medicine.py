from extensions import db
from datetime import datetime


class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80))
    manufacturer = db.Column(db.String(120))
    stock = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0)
    batch_number = db.Column(db.String(40))
    expiry_date = db.Column(db.DateTime)
    reorder_level = db.Column(db.Integer, default=10)
    supplier = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level

    @property
    def is_expired(self):
        return self.expiry_date and self.expiry_date < datetime.utcnow()

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'category': self.category,
                'manufacturer': self.manufacturer, 'stock': self.stock,
                'unit_price': self.unit_price, 'batch_number': self.batch_number,
                'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
                'reorder_level': self.reorder_level, 'supplier': self.supplier,
                'is_low_stock': self.is_low_stock, 'is_expired': self.is_expired}
