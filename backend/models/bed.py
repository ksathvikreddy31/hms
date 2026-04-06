from extensions import db


class Bed(db.Model):
    __tablename__ = 'beds'
    id = db.Column(db.Integer, primary_key=True)
    ward = db.Column(db.String(80))
    bed_number = db.Column(db.String(10), unique=True)
    floor = db.Column(db.Integer, default=1)
    bed_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    daily_rate = db.Column(db.Float, default=1000)
    admitted_at = db.Column(db.DateTime)

    def to_dict(self):
        return {'id': self.id, 'ward': self.ward, 'bed_number': self.bed_number,
                'floor': self.floor, 'bed_type': self.bed_type,
                'status': self.status, 'patient_id': self.patient_id,
                'daily_rate': self.daily_rate}
