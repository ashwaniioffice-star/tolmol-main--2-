import axios from 'axios';
import { handleApiError } from '../utils/helpers';

// Get API base URL from environment variable or use default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5050';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for cookies/sessions
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage = handleApiError(error);
    return Promise.reject(new Error(errorMessage));
  }
);

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post('/api/auth/login', credentials);
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/api/auth/logout');
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

// Auctions API
export const auctionsAPI = {
  getAll: async (params = {}) => {
    const response = await api.get('/api/auctions', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/api/auctions/${id}`);
    return response.data;
  },

  create: async (auctionData) => {
    const response = await api.post('/api/auctions', auctionData);
    return response.data;
  },

  update: async (id, auctionData) => {
    const response = await api.put(`/api/auctions/${id}`, auctionData);
    return response.data;
  },

  placeBid: async (auctionId, bidData) => {
    const response = await api.post(`/api/auctions/${auctionId}/bid`, bidData);
    return response.data;
  },
};

// Categories API
export const categoriesAPI = {
  getAll: async () => {
    const response = await api.get('/api/categories');
    return response.data;
  },
};

// States API
export const statesAPI = {
  getAll: async () => {
    const response = await api.get('/api/states');
    return response.data;
  },
};

// Dashboard API
export const dashboardAPI = {
  getData: async () => {
    const response = await api.get('/api/dashboard');
    return response.data;
  },
};

export default api;

