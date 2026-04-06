import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { patientAPI, extractData } from '../services/api';
import { Users, User } from 'lucide-react';

const PatientsList = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await patientAPI.getAll();
        setPatients(extractData(res, 'patients') || []);
      } catch (err) { 
        console.error(err); 
        setPatients([]);
      }
      setLoading(false);
    };
    fetch();
  }, []);

  return (
    <div className="animate-fade-in">
      <TopBar title="Patients" subtitle="All registered patients" />
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Patient</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Age</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Gender</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Blood Group</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">BMI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {patients.map((p, i) => (
                  <tr key={p.id} className="hover:bg-gray-50 transition-colors animate-slide-up" style={{animationDelay:`${i*40}ms`}}>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 font-semibold text-sm">
                          {(p.name||'P').charAt(0)}
                        </div>
                        <div>
                          <p className="font-semibold text-sm text-gray-900">{p.name||'Patient'}</p>
                          <p className="text-xs text-gray-400">{p.email||''}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{p.age||'-'}</td>
                    <td className="px-6 py-4 text-sm text-gray-600 capitalize">{p.gender||'-'}</td>
                    <td className="px-6 py-4"><span className="badge-info">{p.blood_group||'-'}</span></td>
                    <td className="px-6 py-4 text-sm text-gray-600">{p.bmi||'-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientsList;
