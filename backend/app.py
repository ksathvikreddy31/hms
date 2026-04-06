from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)

    # Disable strict slashes globally to prevent 308 redirects on missing trailing slashes
    app.url_map.strict_slashes = False

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.patients import patients_bp
    from routes.appointments import appointments_bp
    from routes.hospital import hospital_bp
    from routes.billing import billing_bp
    from routes.payments import payments_bp
    from routes.finance import finance_bp
    from routes.predictions import predictions_bp
    from routes.agents import agents_bp
    from routes.dashboard import dashboard_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(hospital_bp, url_prefix='/api/hospital')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(finance_bp, url_prefix='/api/finance')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')

    # Create tables
    with app.app_context():
        from models import user, patient, appointment, staff, bed, equipment, medicine, billing, payment, finance, report
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
