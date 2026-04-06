from extensions import db


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_name = db.Column(db.String(120))
    department = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    time_slot = db.Column(db.String(20))
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    patient = db.relationship('Patient', backref='appointments')

    def to_dict(self):
        date_str = None
        if self.date:
            date_str = self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date)
            
        return {'id': self.id, 'patient_id': self.patient_id,
                'doctor_name': self.doctor_name, 'department': self.department,
                'date': date_str,
                'time_slot': self.time_slot, 'status': self.status,
                'notes': self.notes}
