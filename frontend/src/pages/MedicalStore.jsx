import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { hospitalAPI, extractData } from '../services/api';
import { Pill, AlertTriangle, Package, TrendingDown } from 'lucide-react';

const MedicalStore = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await hospitalAPI.getMedicines();
        setMedicines(extractData(res, 'medicines') || []);
      } catch (err) { 
        console.error(err); 
        setMedicines([]);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  const lowStock = medicines.filter(m => m.is_low_stock);
  const expired = medicines.filter(m => m.is_expired);

  return (
    <div className="animate-fade-in">
      <TopBar title="Medical Store" subtitle="Medicine inventory and stock management" />

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
        <div className="stat-card flex items-center gap-4">
          <div className="w-11 h-11 bg-primary-100 rounded-xl flex items-center justify-center">
            <Package className="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{medicines.length}</p>
            <p className="text-xs text-gray-500">Total Items</p>
          </div>
        </div>
        <div className="stat-card flex items-center gap-4">
          <div className="w-11 h-11 bg-amber-100 rounded-xl flex items-center justify-center">
            <TrendingDown className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-amber-600">{lowStock.length}</p>
            <p className="text-xs text-gray-500">Low Stock</p>
          </div>
        </div>
        <div className="stat-card flex items-center gap-4">
          <div className="w-11 h-11 bg-rose-100 rounded-xl flex items-center justify-center">
            <AlertTriangle className="w-5 h-5 text-rose-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-rose-600">{expired.length}</p>
            <p className="text-xs text-gray-500">Expired</p>
          </div>
        </div>
        <div className="stat-card flex items-center gap-4">
          <div className="w-11 h-11 bg-emerald-100 rounded-xl flex items-center justify-center">
            <Pill className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-emerald-600">{medicines.filter(m => !m.is_low_stock && !m.is_expired).length}</p>
            <p className="text-xs text-gray-500">In Stock</p>
          </div>
        </div>
      </div>

      {/* Medicine Table */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-slide-up">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Medicine</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Stock</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Price</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Expiry</th>
                  <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {medicines.map((med) => (
                  <tr key={med.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <p className="font-semibold text-sm text-gray-900">{med.name}</p>
                      <p className="text-xs text-gray-400">{med.manufacturer}</p>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{med.category}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div className={`h-2 rounded-full ${med.is_low_stock ? 'bg-amber-500' : 'bg-emerald-500'}`}
                            style={{ width: `${Math.min((med.stock / (med.reorder_level * 3)) * 100, 100)}%` }}></div>
                        </div>
                        <span className="text-sm font-medium text-gray-700">{med.stock}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">₹{med.unit_price}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{med.expiry_date ? new Date(med.expiry_date).toLocaleDateString() : 'N/A'}</td>
                    <td className="px-6 py-4">
                      {med.is_expired ? <span className="badge-danger">Expired</span> :
                       med.is_low_stock ? <span className="badge-warning">Low Stock</span> :
                       <span className="badge-success">In Stock</span>}
                    </td>
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

export default MedicalStore;
