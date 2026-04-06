import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { hospitalAPI, extractData } from '../services/api';
import { Users, BedDouble, Wrench, UserPlus, ChevronDown } from 'lucide-react';

const HospitalOps = () => {
  const [staff, setStaff] = useState([]);
  const [beds, setBeds] = useState([]);
  const [equipment, setEquipment] = useState([]);
  const [activeTab, setActiveTab] = useState('staff');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [staffRes, bedsRes, equipRes] = await Promise.all([
          hospitalAPI.getStaff(), hospitalAPI.getBeds(), hospitalAPI.getEquipment()
        ]);
        setStaff(extractData(staffRes, 'staff') || []);
        setBeds(extractData(bedsRes, 'beds') || []);
        setEquipment(extractData(equipRes, 'equipment') || []);
      } catch (err) { 
        console.error(err); 
        setStaff([]);
        setBeds([]);
        setEquipment([]);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  const tabs = [
    { id: 'staff', label: 'Staff', icon: Users, count: staff.length },
    { id: 'beds', label: 'Beds', icon: BedDouble, count: beds.length },
    { id: 'equipment', label: 'Equipment', icon: Wrench, count: equipment.length },
  ];

  const statusBadge = (status) => {
    const map = {
      active: 'badge-success', operational: 'badge-success', available: 'badge-success',
      leave: 'badge-warning', maintenance: 'badge-warning',
      inactive: 'badge-danger', occupied: 'badge-danger', retired: 'badge-danger',
    };
    return map[status] || 'badge-info';
  };

  return (
    <div className="animate-fade-in">
      <TopBar title="Hospital Operations" subtitle="Staff, beds, and equipment management" />

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map((tab) => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all ${
              activeTab === tab.id ? 'bg-primary-500 text-white shadow-md shadow-primary-500/20' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}>
            <tab.icon className="w-4 h-4" />
            {tab.label}
            <span className={`text-xs px-2 py-0.5 rounded-full ${activeTab === tab.id ? 'bg-white/20' : 'bg-gray-100'}`}>{tab.count}</span>
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      ) : (
        <>
          {/* Staff Table */}
          {activeTab === 'staff' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-slide-up">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-50 border-b border-gray-100">
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Name</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Role</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Department</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Shift</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {staff.map((s) => (
                      <tr key={s.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 font-semibold text-sm">
                              {s.name.charAt(0)}
                            </div>
                            <div>
                              <p className="font-semibold text-gray-900 text-sm">{s.name}</p>
                              {s.specialization && <p className="text-xs text-gray-400">{s.specialization}</p>}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600 capitalize">{s.role}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{s.department}</td>
                        <td className="px-6 py-4 text-sm text-gray-600 capitalize">{s.shift}</td>
                        <td className="px-6 py-4"><span className={statusBadge(s.status)}>{s.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Beds Grid */}
          {activeTab === 'beds' && (
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 animate-slide-up">
              {beds.map((b) => (
                <div key={b.id} className={`p-4 rounded-xl border-2 text-center transition-all hover:shadow-md cursor-pointer ${
                  b.status === 'available' ? 'border-emerald-200 bg-emerald-50' :
                  b.status === 'occupied' ? 'border-rose-200 bg-rose-50' :
                  'border-amber-200 bg-amber-50'}`}>
                  <BedDouble className={`w-6 h-6 mx-auto mb-2 ${
                    b.status === 'available' ? 'text-emerald-500' : b.status === 'occupied' ? 'text-rose-500' : 'text-amber-500'}`} />
                  <p className="font-bold text-sm text-gray-900">{b.bed_number}</p>
                  <p className="text-xs text-gray-500">{b.ward}</p>
                  <p className="text-xs text-gray-400 capitalize mt-1">{b.bed_type}</p>
                </div>
              ))}
            </div>
          )}

          {/* Equipment Table */}
          {activeTab === 'equipment' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-slide-up">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-50 border-b border-gray-100">
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Equipment</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Department</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Next Maintenance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {equipment.map((e) => (
                      <tr key={e.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4 font-semibold text-sm text-gray-900">{e.name}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{e.category}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{e.department}</td>
                        <td className="px-6 py-4"><span className={statusBadge(e.status)}>{e.status}</span></td>
                        <td className="px-6 py-4 text-sm text-gray-600">{e.next_maintenance ? new Date(e.next_maintenance).toLocaleDateString() : 'N/A'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HospitalOps;
