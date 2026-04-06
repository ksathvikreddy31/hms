import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let token = localStorage.getItem('mnh_token');
    
    // Clear corrupted tokens from previous bugs immediately
    if (token === 'undefined' || token === 'null') {
      localStorage.removeItem('mnh_token');
      token = null;
    }
    
    const savedUser = localStorage.getItem('mnh_user');
    if (token && savedUser && savedUser !== 'undefined') {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login({ email, password });
    const { token, user: userData } = res.data;
    localStorage.setItem('mnh_token', token);
    localStorage.setItem('mnh_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const register = async (name, email, password) => {
    const res = await authAPI.register({ name, email, password });
    const { token, user: userData } = res.data;
    localStorage.setItem('mnh_token', token);
    localStorage.setItem('mnh_user', JSON.stringify(userData));
    setUser(userData);
    return userData;
  };

  const switchRole = async (role) => {
    const res = await authAPI.switchRole(role);
    const { token, user: userData } = res.data;
    
    // Only update token if the backend provided a new one
    if (token) {
      localStorage.setItem('mnh_token', token);
    }
    
    localStorage.setItem('mnh_user', JSON.stringify(userData || res.data.data?.user));
    setUser(userData || res.data.data?.user);
    return userData || res.data.data?.user;
  };

  const logout = () => {
    localStorage.removeItem('mnh_token');
    localStorage.removeItem('mnh_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, switchRole, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
