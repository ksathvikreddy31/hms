import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { billingAPI, paymentAPI, extractData } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { CreditCard, Smartphone, Banknote, CheckCircle, X } from 'lucide-react';

const Payments = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'doctor';
  const [pendingBills, setPendingBills] = useState([]);
  const [selectedBill, setSelectedBill] = useState(null);
  const [method, setMethod] = useState('upi');
  const [processing, setProcessing] = useState(false);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchPending(); }, []);

  const fetchPending = async () => {
    try {
      const res = isAdmin ? await billingAPI.getAll() : await billingAPI.getMine();
      setPendingBills((extractData(res, 'billings') || []).filter(b => b.status === 'pending'));
    } catch (err) { 
      console.error(err); 
      setPendingBills([]);
    }
    setLoading(false);
  };

  const handlePay = async () => {
    if (!selectedBill) return;
    setProcessing(true);
    try {
      const res = await paymentAPI.process({ billing_id: selectedBill.id, method });
      setSuccess(res.data?.data?.payment || res.data?.payment || null);
      fetchPending();
    } catch (err) { console.error(err); }
    setProcessing(false);
  };

  const methods = [
    { id: 'upi', label: 'UPI', icon: Smartphone, desc: 'Pay via UPI ID' },
    { id: 'card', label: 'Card', icon: CreditCard, desc: 'Debit / Credit Card' },
    { id: 'cash', label: 'Cash', icon: Banknote, desc: 'Pay at counter' },
  ];

  return (
    <div className="animate-fade-in">
      <TopBar title="Payments" subtitle="Process payments for pending bills" />

      {success ? (
        <div className="max-w-md mx-auto bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center animate-slide-up">
          <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-10 h-10 text-emerald-500" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h3>
          <p className="text-gray-500 mb-6">Your payment has been processed.</p>
          <div className="bg-gray-50 rounded-xl p-4 space-y-2 text-left mb-6">
            <div className="flex justify-between text-sm"><span className="text-gray-500">Transaction ID</span><span className="font-mono font-semibold">{success.transaction_id}</span></div>
            <div className="flex justify-between text-sm"><span className="text-gray-500">Amount</span><span className="font-semibold">₹{success.amount.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-gray-500">Method</span><span className="font-semibold capitalize">{success.method}</span></div>
            <div className="flex justify-between text-sm"><span className="text-gray-500">Status</span><span className="badge-success">{success.status}</span></div>
          </div>
          <button onClick={() => { setSuccess(null); setSelectedBill(null); }} className="btn-primary w-full">Done</button>
        </div>
      ) : selectedBill ? (
        <div className="max-w-md mx-auto animate-slide-up">
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">Pay Bill #{selectedBill.id}</h3>
              <button onClick={() => setSelectedBill(null)} className="p-2 hover:bg-gray-100 rounded-lg"><X className="w-4 h-4" /></button>
            </div>
            <div className="text-center py-4">
              <p className="text-sm text-gray-500">Amount Due</p>
              <p className="text-4xl font-bold text-gray-900 mt-1">₹{selectedBill.total.toFixed(2)}</p>
            </div>
          </div>

          <div className="space-y-3 mb-6">
            <p className="text-sm font-semibold text-gray-700">Select Payment Method</p>
            {methods.map((m) => (
              <button key={m.id} onClick={() => setMethod(m.id)}
                className={`w-full flex items-center gap-4 p-4 rounded-xl border-2 transition-all ${
                  method === m.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200 bg-white hover:border-gray-300'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${method === m.id ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-500'}`}>
                  <m.icon className="w-5 h-5" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-gray-900">{m.label}</p>
                  <p className="text-xs text-gray-500">{m.desc}</p>
                </div>
              </button>
            ))}
          </div>

          <button onClick={handlePay} disabled={processing} className="btn-primary w-full flex items-center justify-center gap-2 py-3 disabled:opacity-50">
            {processing ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> :
              <><CreditCard className="w-4 h-4" /> Pay ₹{selectedBill.total.toFixed(2)}</>}
          </button>
        </div>
      ) : (
        <div>
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="w-8 h-8 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
            </div>
          ) : pendingBills.length === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <CheckCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p className="font-medium">No pending payments</p>
              <p className="text-sm mt-1">All bills are paid!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {pendingBills.map((bill, i) => (
                <div key={bill.id} onClick={() => setSelectedBill(bill)}
                  className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer animate-slide-up flex items-center justify-between"
                  style={{ animationDelay: `${i * 50}ms` }}>
                  <div>
                    <p className="font-semibold text-gray-900">Bill #{bill.id}</p>
                    <p className="text-sm text-gray-500">{bill.items.length} items</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xl font-bold text-gray-900">₹{bill.total.toFixed(2)}</p>
                    <span className="badge-warning">pending</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Payments;
