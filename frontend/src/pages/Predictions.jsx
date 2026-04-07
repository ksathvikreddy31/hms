import React, { useState, useEffect } from 'react';
import TopBar from '../components/TopBar';
import { predictionAPI } from '../services/api';
import { Users, IndianRupee, Activity, Package, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Predictions = () => {
  const [inflow, setInflow] = useState(null);
  const [revenue, setRevenue] = useState(null);
  const [disease, setDisease] = useState(null);
  const [resource, setResource] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [i, r, d, res] = await Promise.all([
          predictionAPI.getPatientInflow(), predictionAPI.getRevenue(),
          predictionAPI.getDiseaseTrends(), predictionAPI.getResourceDemand()
        ]);
        setInflow(i.data); setRevenue(r.data); setDisease(d.data); setResource(res.data);
      } catch (err) { console.error(err); }
      setLoading(false);
    };
    fetchAll();
  }, []);

  if (loading) return <div className="flex items-center justify-center h-96"><div className="w-10 h-10 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div></div>;

  const trendIcon = (t) => t === 'increasing' ? <TrendingUp className="w-4 h-4 text-rose-500" /> :
    t === 'decreasing' ? <TrendingDown className="w-4 h-4 text-emerald-500" /> : <Minus className="w-4 h-4 text-gray-400" />;

  const riskColor = (r) => r === 'high' ? 'badge-danger' : r === 'medium' ? 'badge-warning' : 'badge-success';

  return (
    <div className="animate-fade-in">
      <TopBar title="AI Predictions" subtitle="ML-powered forecasting and analytics" />

      {/* Prediction Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-8">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 animate-slide-up">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-9 h-9 bg-blue-100 rounded-lg flex items-center justify-center"><Users className="w-4 h-4 text-blue-600" /></div>
            <div>
              <h3 className="font-semibold text-gray-900">{inflow?.title}</h3>
              <p className="text-xs text-gray-500">Confidence: {(inflow?.confidence * 100).toFixed(0)}%</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={[...(inflow?.historical?.slice(-10)||[]), ...(inflow?.predicted||[])]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="date" tick={{fontSize:10,fill:'#94A3B8'}} />
              <YAxis tick={{fontSize:10,fill:'#94A3B8'}} />
              <Tooltip contentStyle={{borderRadius:'12px',border:'1px solid #E2E8F0'}} />
              <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-sm text-blue-600 bg-blue-50 px-3 py-2 rounded-lg mt-3">{inflow?.insight}</p>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 animate-slide-up" style={{animationDelay:'100ms'}}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-9 h-9 bg-emerald-100 rounded-lg flex items-center justify-center"><IndianRupee className="w-4 h-4 text-emerald-600" /></div>
            <div>
              <h3 className="font-semibold text-gray-900">{revenue?.title}</h3>
              <p className="text-xs text-gray-500">Confidence: {(revenue?.confidence * 100).toFixed(0)}%</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={[...(revenue?.historical?.slice(-10)||[]), ...(revenue?.predicted||[])]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="date" tick={{fontSize:10,fill:'#94A3B8'}} />
              <YAxis tick={{fontSize:10,fill:'#94A3B8'}} />
              <Tooltip contentStyle={{borderRadius:'12px',border:'1px solid #E2E8F0'}} />
              <Line type="monotone" dataKey="value" stroke="#10B981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-sm text-emerald-600 bg-emerald-50 px-3 py-2 rounded-lg mt-3">{revenue?.insight}</p>
        </div>
      </div>

      {/* Disease Trends */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-5 animate-slide-up" style={{animationDelay:'200ms'}}>
        <h3 className="text-lg font-semibold text-gray-900 mb-1 flex items-center gap-2"><Activity className="w-5 h-5 text-primary-500" /> {disease?.title}</h3>
        <p className="text-sm text-gray-500 mb-4">{disease?.description}</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {disease?.trends?.map((t, i) => (
            <div key={i} className="p-4 bg-gray-50 rounded-xl">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-sm text-gray-900">{t.disease}</span>
                {trendIcon(t.trend)}
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-500">Now: {t.current_cases}</span>
                <span className="text-gray-500">Next: {t.predicted_next_week}</span>
              </div>
              <div className="mt-2"><span className={riskColor(t.risk_level)}>{t.risk_level} risk</span></div>
            </div>
          ))}
        </div>
        <p className="text-sm text-amber-600 bg-amber-50 px-3 py-2 rounded-lg mt-4">{disease?.season_alert}</p>
      </div>

      {/* Resource Demand */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 animate-slide-up" style={{animationDelay:'300ms'}}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2"><Package className="w-5 h-5 text-hospital-purple" /> {resource?.title}</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {resource?.resources?.map((r, i) => {
            const shortage = r.predicted_need > r.current;
            return (
              <div key={i} className={`p-4 rounded-xl border-2 ${shortage ? 'border-amber-200 bg-amber-50' : 'border-emerald-200 bg-emerald-50'}`}>
                <p className="font-semibold text-sm text-gray-900">{r.resource}</p>
                <div className="flex items-center justify-between mt-2 text-xs text-gray-600">
                  <span>Current: {r.current} {r.unit}</span>
                  <span>Need: {r.predicted_need} {r.unit}</span>
                </div>
                {shortage && <p className="text-xs text-amber-700 mt-2 font-medium">⚠️ Shortage predicted</p>}
              </div>
            );
          })}
        </div>
        <p className="text-sm text-primary-600 bg-primary-50 px-3 py-2 rounded-lg mt-4">{resource?.insight}</p>
      </div>
    </div>
  );
};

export default Predictions;
