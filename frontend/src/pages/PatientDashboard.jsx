import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { hospitalAPI, appointmentAPI, billingAPI, paymentAPI, extractData } from '../services/api';
import { Calendar, CreditCard, Activity, ChevronRight, UserRound, Stethoscope, ArrowRight } from 'lucide-react';

const PatientDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [departments, setDepartments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [deptRes, docRes, apptRes, payRes] = await Promise.all([
          hospitalAPI.getDepartments(),
          hospitalAPI.getStaff(),
          appointmentAPI.getMine(),
          billingAPI.getMine()
        ]);
        
        setDepartments(extractData(deptRes, 'departments') || []);
        const allStaff = extractData(docRes, 'staff') || [];
        setDoctors(allStaff.filter(s => s.role === 'doctor'));
        
        let allAppts = extractData(apptRes, 'appointments') || [];
        setAppointments(allAppts.filter(a => a.status === 'scheduled'));
        
        let allPayments = extractData(payRes, 'billings') || [];
        setPayments(allPayments.filter(p => p.status === 'pending'));
      } catch (err) {
        console.error("Failed to load patient data", err);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-10 h-10 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in max-w-7xl mx-auto">
      {/* Header / Intro */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-3xl p-8 sm:p-12 mb-8 text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-3xl sm:text-4xl font-bold mb-4">Welcome back, {user?.name}</h1>
          <p className="text-primary-100 text-lg max-w-2xl">
            Manage your health journey with MNH Autonomous AI Hospital. Book appointments, view reports, and stay updated with your care plan seamlessly.
          </p>
          <button 
            onClick={() => navigate('/appointments')}
            className="mt-6 px-6 py-3 bg-white text-primary-700 font-semibold rounded-xl hover:bg-primary-50 transition-colors shadow-sm inline-flex items-center gap-2"
          >
            Book New Appointment
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
        <div className="absolute right-0 top-0 opacity-10 pointer-events-none">
          <Activity className="w-96 h-96" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Quick Stats & Suggestions */}
        <div className="lg:col-span-2 space-y-8">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {/* Appointments Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col items-start hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-4">
                <Calendar className="w-6 h-6" />
              </div>
              <h3 className="text-gray-500 font-medium mb-1">Upcoming Appointments</h3>
              <p className="text-3xl font-bold text-gray-900 mb-4">{appointments.length}</p>
              
              {appointments.length > 0 ? (
                <div className="w-full space-y-2 mt-auto">
                  {appointments.slice(0, 3).map(appt => (
                    <div key={appt.id} className="text-sm border-l-2 border-blue-500 pl-3 py-1">
                      <p className="font-semibold text-gray-800">{appt.department} • {appt.doctor_name}</p>
                      <p className="text-gray-500">{appt.date} at {appt.time_slot}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-400 mt-auto">No upcoming appointments</p>
              )}
            </div>

            {/* Payments Card */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col items-start hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center mb-4">
                <CreditCard className="w-6 h-6" />
              </div>
              <h3 className="text-gray-500 font-medium mb-1">Pending Payments</h3>
              <p className="text-3xl font-bold text-gray-900 mb-4">{payments.length}</p>
              
              {payments.length > 0 ? (
                <div className="w-full space-y-2 mt-auto">
                  {payments.slice(0, 3).map(pay => (
                    <div key={pay.id} className="flex justify-between items-center text-sm bg-gray-50 p-2 rounded-lg">
                      <span className="font-medium text-gray-700">Bill #{pay.id}</span>
                      <span className="font-bold text-amber-600">₹{pay.total}</span>
                    </div>
                  ))}
                  <button 
                    onClick={() => navigate('/payments')}
                    className="w-full mt-2 text-sm text-primary-600 font-medium hover:text-primary-700 text-left"
                  >
                    View all pending &rarr;
                  </button>
                </div>
              ) : (
                <p className="text-sm text-gray-400 mt-auto">All clear! No pending payments.</p>
              )}
            </div>
          </div>

          {/* Departments */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-gray-900">Explore Departments</h3>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {departments.slice(0, 6).map((dept, idx) => (
                <div key={idx} className="bg-gray-50 hover:bg-primary-50 rounded-xl p-4 text-center cursor-pointer transition-colors border border-transparent hover:border-primary-100">
                  <div className="w-10 h-10 mx-auto bg-white rounded-full shadow-sm flex items-center justify-center text-primary-500 mb-3">
                    <Stethoscope className="w-5 h-5" />
                  </div>
                  <h4 className="font-medium text-gray-800 text-sm">{dept}</h4>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Top Doctors & Tips */}
        <div className="space-y-8">
          
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
              <UserRound className="w-5 h-5 text-primary-500" />
              Leading Specialists
            </h3>
            <div className="space-y-4">
              {doctors.slice(0, 4).map((doc, idx) => (
                <div key={idx} className="flex items-center gap-4 p-3 hover:bg-gray-50 rounded-xl transition-colors">
                  <div className="w-12 h-12 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-bold text-lg">
                    {doc.name.charAt(0)}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 text-sm">Dr. {doc.name}</h4>
                    <p className="text-xs text-gray-500">{doc.department} • {doc.specialization}</p>
                  </div>
                  <button onClick={() => navigate('/appointments')} className="w-8 h-8 flex items-center justify-center bg-gray-100 hover:bg-primary-100 text-gray-600 hover:text-primary-600 rounded-lg transition-colors">
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-blue-50 rounded-2xl p-6 border border-blue-100">
            <h3 className="text-blue-900 font-bold mb-2">Health Tip of the Day</h3>
            <p className="text-blue-800 text-sm leading-relaxed">
              Drink at least 8 glasses of water a day. Staying hydrated is essential for your body to function properly, maintaining energy levels and supporting overall health.
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};

export default PatientDashboard;
