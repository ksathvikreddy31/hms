-- Database Initialization for MNH Hospital OS
-- Seeding data from backend/scripts/init_db.py

CREATE DATABASE IF NOT EXISTS mnh_hospital_db;
USE mnh_hospital_db;

-- ---------------------------------------------------------
-- TABLE CREATION
-- ---------------------------------------------------------

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'patient',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    age INT,
    gender VARCHAR(10),
    blood_group VARCHAR(5),
    bmi FLOAT,
    conditions TEXT,
    allergies TEXT,
    lifestyle TEXT,
    emergency_contact VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Staff Table
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(30),
    department VARCHAR(80),
    specialization VARCHAR(120),
    shift VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_name VARCHAR(120),
    department VARCHAR(80),
    date DATETIME,
    time_slot VARCHAR(20),
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- 5. Beds Table
CREATE TABLE IF NOT EXISTS beds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ward VARCHAR(80),
    bed_number VARCHAR(10) UNIQUE,
    floor INT DEFAULT 1,
    bed_type VARCHAR(20),
    status VARCHAR(20) DEFAULT 'available',
    patient_id INT,
    daily_rate FLOAT DEFAULT 1000,
    admitted_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE SET NULL
);

-- 6. Equipment Table
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(80),
    department VARCHAR(80),
    status VARCHAR(20) DEFAULT 'operational',
    serial_number VARCHAR(40),
    purchase_date DATETIME,
    last_maintenance DATETIME,
    next_maintenance DATETIME,
    cost FLOAT
);

-- 7. Medicines Table
CREATE TABLE IF NOT EXISTS medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(80),
    manufacturer VARCHAR(120),
    stock INT DEFAULT 0,
    unit_price FLOAT DEFAULT 0,
    batch_number VARCHAR(40),
    expiry_date DATETIME,
    reorder_level INT DEFAULT 10,
    supplier VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Billings Table
CREATE TABLE IF NOT EXISTS billings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    items TEXT NOT NULL,
    subtotal FLOAT DEFAULT 0,
    tax FLOAT DEFAULT 0,
    discount FLOAT DEFAULT 0,
    total FLOAT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- 9. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    billing_id INT NOT NULL,
    amount FLOAT NOT NULL,
    method VARCHAR(20) DEFAULT 'cash',
    transaction_id VARCHAR(40),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (billing_id) REFERENCES billings(id) ON DELETE CASCADE
);

-- 10. Finance Records Table
CREATE TABLE IF NOT EXISTS finance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    record_type VARCHAR(20),
    category VARCHAR(60),
    amount FLOAT NOT NULL,
    department VARCHAR(80),
    description TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
-- SEED DATA
-- ---------------------------------------------------------

-- Note: All passwords are set to 'admin123', 'doctor123', or 'patient123' based on role.
-- Hash corresponds to: scrypt:32768:8:1$79195e01f6170a1c8f807d571067

-- Users
INSERT INTO users (id, email, name, password_hash, role) VALUES
(1, 'admin@mnh.com', 'Dr. Admin Kumar', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'admin'),
(2, 'doctor@mnh.com', 'Dr. Priya Sharma', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'doctor'),
(3, 'rahul@email.com', 'Rahul Verma', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'patient'),
(4, 'sneha@email.com', 'Sneha Patel', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'patient'),
(5, 'amit@email.com', 'Amit Singh', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'patient'),
(6, 'priya@email.com', 'Priya Reddy', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'patient'),
(7, 'vikram@email.com', 'Vikram Joshi', 'scrypt:32768:8:1$79195e01f6170a1c8f807d571067', 'patient');

-- Patients
INSERT INTO patients (id, user_id, age, gender, blood_group, bmi, conditions, lifestyle, emergency_contact) VALUES
(1, 3, 28, 'male', 'B+', 23.5, '["Diabetes", "None"]', '{"exercise": "daily", "smoking": false, "alcohol": "none"}', '+91 9876543210'),
(2, 4, 35, 'female', 'O+', 26.1, '["Hypertension", "None"]', '{"exercise": "weekly", "smoking": true, "alcohol": "occasional"}', '+91 9876543211'),
(3, 5, 45, 'male', 'A+', 29.3, '["Asthma", "None"]', '{"exercise": "rarely", "smoking": false, "alcohol": "regular"}', '+91 9876543212'),
(4, 6, 32, 'female', 'AB+', 22.8, '["None", "None"]', '{"exercise": "daily", "smoking": false, "alcohol": "none"}', '+91 9876543213'),
(5, 7, 55, 'male', 'O-', 27.6, '["Diabetes", "Hypertension"]', '{"exercise": "weekly", "smoking": true, "alcohol": "occasional"}', '+91 9876543214');

-- Staff
INSERT INTO staff (name, role, department, specialization, shift) VALUES
('Dr. Priya Sharma', 'doctor', 'Cardiology', 'Interventional Cardiology', 'morning'),
('Dr. Rajesh Gupta', 'doctor', 'Orthopedics', 'Joint Replacement', 'morning'),
('Dr. Aishwarya Nair', 'doctor', 'Neurology', 'Neurological Surgery', 'afternoon'),
('Dr. Sanjay Mehta', 'doctor', 'Pediatrics', 'Neonatal Care', 'morning'),
('Dr. Kavitha Rao', 'doctor', 'General Medicine', 'Internal Medicine', 'afternoon'),
('Nurse Anita Kumari', 'nurse', 'Emergency', NULL, 'morning'),
('Nurse Deepak Pandey', 'nurse', 'ICU', NULL, 'night'),
('Nurse Fatima Khan', 'nurse', 'General Ward', NULL, 'afternoon'),
('Nurse Ravi Teja', 'nurse', 'Pediatrics', NULL, 'morning'),
('Tech Suresh Kumar', 'technician', 'Radiology', 'MRI/CT Scan', 'morning'),
('Tech Meera Das', 'technician', 'Laboratory', 'Pathology', 'morning'),
('Admin Pooja Iyer', 'admin', 'Front Office', NULL, 'morning');

-- Equipment
INSERT INTO equipment (name, category, department, cost, status, serial_number) VALUES
('MRI Machine', 'Imaging', 'Radiology', 15000000, 'operational', 'EQ-10001'),
('CT Scanner', 'Imaging', 'Radiology', 12000000, 'operational', 'EQ-10002'),
('X-Ray Machine', 'Imaging', 'Radiology', 3000000, 'operational', 'EQ-10003'),
('Ventilator', 'Life Support', 'ICU', 800000, 'operational', 'EQ-10004'),
('Defibrillator', 'Emergency', 'Emergency', 250000, 'operational', 'EQ-10005'),
('ECG Machine', 'Diagnostic', 'Cardiology', 150000, 'operational', 'EQ-10006'),
('Ultrasound', 'Imaging', 'OB-GYN', 2000000, 'operational', 'EQ-10007'),
('Blood Analyzer', 'Laboratory', 'Laboratory', 500000, 'operational', 'EQ-10008'),
('Autoclave', 'Sterilization', 'OT', 100000, 'operational', 'EQ-10009'),
('Patient Monitor', 'Monitoring', 'ICU', 300000, 'operational', 'EQ-10010');

-- Medicines
INSERT INTO medicines (name, category, manufacturer, stock, unit_price, batch_number, reorder_level, supplier) VALUES
('Paracetamol 500mg', 'Analgesic', 'Sun Pharma', 200, 5.50, 'BN-1001', 20, 'Sun Pharma Distributors'),
('Amoxicillin 250mg', 'Antibiotic', 'Cipla', 150, 12.00, 'BN-1002', 20, 'Cipla Distributors'),
('Metformin 500mg', 'Anti-diabetic', 'Dr. Reddys', 300, 8.00, 'BN-1003', 20, 'Dr. Reddys Distributors'),
('Amlodipine 5mg', 'Antihypertensive', 'Lupin', 250, 6.50, 'BN-1004', 20, 'Lupin Distributors'),
('Omeprazole 20mg', 'Antacid', 'Zydus', 180, 9.00, 'BN-1005', 20, 'Zydus Distributors'),
('Cetirizine 10mg', 'Antihistamine', 'Sun Pharma', 100, 4.00, 'BN-1006', 20, 'Sun Pharma Distributors'),
('Azithromycin 500mg', 'Antibiotic', 'Cipla', 80, 25.00, 'BN-1007', 20, 'Cipla Distributors'),
('Insulin Glargine', 'Anti-diabetic', 'Novo Nordisk', 50, 450.00, 'BN-1008', 20, 'Novo Nordisk Distributors'),
('Ibuprofen 400mg', 'NSAID', 'Abbott', 300, 7.00, 'BN-1009', 20, 'Abbott Distributors'),
('Clopidogrel 75mg', 'Antiplatelet', 'Torrent', 120, 15.00, 'BN-1010', 20, 'Torrent Distributors'),
('Salbutamol Inhaler', 'Bronchodilator', 'Cipla', 5, 180.00, 'BN-1011', 20, 'Cipla Distributors'),
('Dexamethasone 4mg', 'Steroid', 'Zydus', 90, 12.00, 'BN-1012', 20, 'Zydus Distributors');

-- Beds (Initial Selection)
INSERT INTO beds (ward, bed_number, floor, bed_type, status, daily_rate) VALUES
('General Ward A', 'BED-1', 1, 'general', 'available', 500),
('General Ward A', 'BED-2', 1, 'general', 'occupied', 500),
('General Ward B', 'BED-9', 1, 'general', 'available', 500),
('ICU', 'BED-17', 2, 'icu', 'available', 5000),
('Private Ward', 'BED-25', 3, 'private', 'available', 3500),
('Semi-Private', 'BED-33', 2, 'semi-private', 'occupied', 2000),
('Pediatric Ward', 'BED-41', 1, 'general', 'available', 1000);
