import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { billingAPI, paymentAPI, extractData } from '../services/api';
import { Receipt, IndianRupee, CreditCard, CheckCircle, Clock, Plus, X } from 'lucide-react';

const Billing = () => {
  const [bills, setBills] = useState([]);
  const [selectedBill, setSelectedBill] = useState(null);
  const [showGenerate, setShowGenerate] = useState(false);
  const [items, setItems] = useState([{ name: '', category: 'consultation', rate: 0, quantity: 1 }]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchBills(); }, []);

  const fetchBills = async () => {
    try {
      const res = await billingAPI.getAll();
      setBills(extractData(res, 'billings') || []);
    } catch (err) { 
      console.error(err); 
      setBills([]);
    }
    setLoading(false);
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    try {
      await billingAPI.generate({ patient_id: 1, items, discount: 0 });
      setShowGenerate(false);
      setItems([{ name: '', category: 'consultation', rate: 0, quantity: 1 }]);
      fetchBills();
    } catch (err) { console.error(err); }
  };

  const handlePayment = async (billId) => {
    try {
      await paymentAPI.process({ billing_id: billId, method: 'upi' });
      fetchBills();
      setSelectedBill(null);
    } catch (err) { console.error(err); }
  };

  const addItem = () => setItems([...items, { name: '', category: 'consultation', rate: 0, quantity: 1 }]);
  const removeItem = (i) => setItems(items.filter((_, idx) => idx !== i));

  return (
    <div className="animate-fade-in">
      <TopBar title="Billing" subtitle="Generate and manage patient bills" />

      <div className="flex justify-end mb-6">
        <button onClick={() => setShowGenerate(true)} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> Generate Bill
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="w-8 h-8 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="grid gap-4">
          {bills.map((bill, i) => (
            <div key={bill.id} onClick={() => setSelectedBill(bill)}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer animate-slide-up"
              style={{ animationDelay: `${i * 50}ms` }}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${bill.status === 'paid' ? 'bg-emerald-50' : 'bg-amber-50'}`}>
                    {bill.status === 'paid' ? <CheckCircle className="w-6 h-6 text-emerald-500" /> : <Clock className="w-6 h-6 text-amber-500" />}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Bill #{bill.id}</p>
                    <p className="text-sm text-gray-500">{bill.items.length} items • {new Date(bill.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold text-gray-900">₹{bill.total.toFixed(2)}</p>
                  <span className={bill.status === 'paid' ? 'badge-success' : 'badge-warning'}>{bill.status}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Bill Detail Modal */}
      {selectedBill && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-8 w-full max-w-lg shadow-2xl animate-slide-up max-h-[85vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900">Bill #{selectedBill.id}</h3>
              <button onClick={() => setSelectedBill(null)} className="p-2 hover:bg-gray-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="space-y-3 mb-6">
              {selectedBill.items.map((item, i) => (
                <div key={i} className="flex justify-between p-3 bg-gray-50 rounded-xl">
                  <div>
                    <p className="font-medium text-sm text-gray-900">{item.name}</p>
                    <p className="text-xs text-gray-400 capitalize">{item.category} × {item.quantity}</p>
                  </div>
                  <p className="font-semibold text-gray-900">₹{(item.rate * item.quantity).toFixed(2)}</p>
                </div>
              ))}
            </div>
            <div className="border-t border-gray-100 pt-4 space-y-2">
              <div className="flex justify-between text-sm"><span className="text-gray-500">Subtotal</span><span>₹{selectedBill.subtotal.toFixed(2)}</span></div>
              <div className="flex justify-between text-sm"><span className="text-gray-500">GST (5%)</span><span>₹{selectedBill.tax.toFixed(2)}</span></div>
              {selectedBill.discount > 0 && <div className="flex justify-between text-sm text-emerald-600"><span>Discount</span><span>-₹{selectedBill.discount.toFixed(2)}</span></div>}
              <div className="flex justify-between text-lg font-bold pt-2 border-t border-gray-100"><span>Total</span><span>₹{selectedBill.total.toFixed(2)}</span></div>
            </div>
            {selectedBill.status === 'pending' && (
              <button onClick={() => handlePayment(selectedBill.id)} className="btn-primary w-full mt-6 flex items-center justify-center gap-2">
                <CreditCard className="w-4 h-4" /> Pay Now
              </button>
            )}
          </div>
        </div>
      )}

      {/* Generate Bill Modal */}
      {showGenerate && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-8 w-full max-w-lg shadow-2xl animate-slide-up max-h-[85vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900">Generate Bill</h3>
              <button onClick={() => setShowGenerate(false)} className="p-2 hover:bg-gray-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <form onSubmit={handleGenerate} className="space-y-4">
              {items.map((item, i) => (
                <div key={i} className="p-4 bg-gray-50 rounded-xl space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-semibold text-gray-700">Item {i + 1}</span>
                    {items.length > 1 && <button type="button" onClick={() => removeItem(i)} className="text-rose-500 text-xs">Remove</button>}
                  </div>
                  <input value={item.name} onChange={(e) => { const n = [...items]; n[i].name = e.target.value; setItems(n); }}
                    className="input-field" placeholder="Item name" required />
                  <div className="grid grid-cols-3 gap-2">
                    <select value={item.category} onChange={(e) => { const n = [...items]; n[i].category = e.target.value; setItems(n); }} className="input-field">
                      <option value="consultation">Consultation</option>
                      <option value="test">Test</option>
                      <option value="bed">Bed</option>
                      <option value="medicine">Medicine</option>
                    </select>
                    <input type="number" value={item.rate} onChange={(e) => { const n = [...items]; n[i].rate = Number(e.target.value); setItems(n); }}
                      className="input-field" placeholder="Rate" min="0" required />
                    <input type="number" value={item.quantity} onChange={(e) => { const n = [...items]; n[i].quantity = Number(e.target.value); setItems(n); }}
                      className="input-field" placeholder="Qty" min="1" required />
                  </div>
                </div>
              ))}
              <button type="button" onClick={addItem} className="btn-secondary w-full flex items-center justify-center gap-2">
                <Plus className="w-4 h-4" /> Add Item
              </button>
              <div className="text-right text-lg font-bold text-gray-900 pt-2">
                Total: ₹{(items.reduce((s, i) => s + i.rate * i.quantity, 0) * 1.05).toFixed(2)}
              </div>
              <button type="submit" className="btn-primary w-full">Generate Bill</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Billing;
