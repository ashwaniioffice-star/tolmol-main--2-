import React, { createContext, useState, useContext, useEffect } from 'react';
import { loginUser, registerUser, logoutUser } from '../lib/helpers'; // Assuming helpers.js is in lib

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for a token in localStorage or sessionStorage on mount
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you'd validate the token with your backend
      // For this example, we'll just assume it's valid
      setUser({ token }); // Or fetch user details based on token
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const data = await loginUser(credentials);
      localStorage.setItem('token', data.token);
      setUser(data);
      return data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const data = await registerUser(userData);
      localStorage.setItem('token', data.token);
      setUser(data);
      return data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    logoutUser();
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
