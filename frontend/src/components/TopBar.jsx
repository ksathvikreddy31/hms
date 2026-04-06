import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Bell, Search } from 'lucide-react';

const TopBar = ({ title, subtitle }) => {
  const { user } = useAuth();

  return (
    <div className="flex items-center justify-between mb-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-4">
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search..."
            className="pl-10 pr-4 py-2.5 rounded-xl bg-white border border-gray-200 text-sm w-64 focus:border-primary-400 focus:ring-2 focus:ring-primary-100 outline-none transition-all"
          />
        </div>
        <button className="relative p-2.5 rounded-xl bg-white border border-gray-200 hover:bg-gray-50 transition-colors">
          <Bell className="w-5 h-5 text-gray-500" />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-hospital-rose text-white text-[10px] font-bold rounded-full flex items-center justify-center">3</span>
        </button>
        <div className="hidden md:flex items-center gap-3 px-4 py-2 bg-white rounded-xl border border-gray-200">
          <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-hospital-purple rounded-lg flex items-center justify-center text-white font-semibold text-xs">
            {user?.name?.charAt(0) || 'U'}
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-900">{user?.name}</p>
            <p className="text-[11px] text-gray-400 capitalize">{user?.role}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
