from extensions import db

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_name = db.Column(db.String(120), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    patient = db.relationship('Patient', backref='reports')

    def to_dict(self):
        patient_name = None
        if self.patient and self.patient.user:
            patient_name = self.patient.user.name
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': patient_name,
            'doctor_name': self.doctor_name,
            'visit_date': self.visit_date.strftime('%Y-%m-%d') if self.visit_date else None,
            'diagnosis': self.diagnosis,
            'suggestions': self.suggestions
        }

