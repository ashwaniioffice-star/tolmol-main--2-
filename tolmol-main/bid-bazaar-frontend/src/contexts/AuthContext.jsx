import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { storage } from '../utils/helpers';
import { authAPI } from '../services/api';

// Auth context
const AuthContext = createContext();

// Auth actions
const AUTH_ACTIONS = {
  LOGIN_START: 'LOGIN_START',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  LOGOUT: 'LOGOUT',
  REGISTER_START: 'REGISTER_START',
  REGISTER_SUCCESS: 'REGISTER_SUCCESS',
  REGISTER_FAILURE: 'REGISTER_FAILURE',
  CLEAR_ERROR: 'CLEAR_ERROR',
  LOAD_USER_START: 'LOAD_USER_START',
  LOAD_USER_SUCCESS: 'LOAD_USER_SUCCESS',
  LOAD_USER_FAILURE: 'LOAD_USER_FAILURE'
};

// Initial state
const initialState = {
  user: null,
  token: null,
  isLoading: false,
  error: null,
  isAuthenticated: false
};

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.LOGIN_START:
    case AUTH_ACTIONS.REGISTER_START:
    case AUTH_ACTIONS.LOAD_USER_START:
      return {
        ...state,
        isLoading: true,
        error: null
      };
      
    case AUTH_ACTIONS.LOGIN_SUCCESS:
    case AUTH_ACTIONS.REGISTER_SUCCESS:
    case AUTH_ACTIONS.LOAD_USER_SUCCESS:
      return {
        ...state,
        isLoading: false,
        user: action.payload.user,
        token: action.payload.token || state.token,
        isAuthenticated: true,
        error: null
      };
      
    case AUTH_ACTIONS.LOGIN_FAILURE:
    case AUTH_ACTIONS.REGISTER_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload,
        user: null,
        token: null,
        isAuthenticated: false
      };
      
    case AUTH_ACTIONS.LOAD_USER_FAILURE:
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false
      };
      
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...initialState
      };
      
    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };
      
    default:
      return state;
  }
};

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Load user from API on mount
  useEffect(() => {
    const loadUser = async () => {
      const savedUser = storage.get('user');
      
      if (savedUser) {
        dispatch({
          type: AUTH_ACTIONS.LOAD_USER_START
        });
        
        try {
          const response = await authAPI.getCurrentUser();
          storage.set('user', response.user);
          dispatch({
            type: AUTH_ACTIONS.LOAD_USER_SUCCESS,
            payload: { user: response.user }
          });
        } catch (error) {
          // If session expired, clear saved user
          storage.remove('user');
          storage.remove('token');
          dispatch({ type: AUTH_ACTIONS.LOAD_USER_FAILURE });
        }
      }
    };
    
    loadUser();
  }, []);

  // Login function
  const login = async (credentials) => {
    dispatch({ type: AUTH_ACTIONS.LOGIN_START });
    
    try {
      const response = await authAPI.login(credentials);
      
      // Save to localStorage
      storage.set('user', response.user);
      
      dispatch({
        type: AUTH_ACTIONS.LOGIN_SUCCESS,
        payload: { user: response.user }
      });
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.message || 'Invalid username or password';
      dispatch({
        type: AUTH_ACTIONS.LOGIN_FAILURE,
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Register function
  const register = async (userData) => {
    dispatch({ type: AUTH_ACTIONS.REGISTER_START });
    
    try {
      const response = await authAPI.register(userData);
      
      // Save to localStorage
      storage.set('user', response.user);
      
      dispatch({
        type: AUTH_ACTIONS.REGISTER_SUCCESS,
        payload: { user: response.user }
      });
      
      return { success: true };
    } catch (error) {
      const errorMessage = error.message || 'Registration failed';
      dispatch({
        type: AUTH_ACTIONS.REGISTER_FAILURE,
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      storage.remove('user');
      storage.remove('token');
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  };

  // Clear error function
  const clearError = () => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  };

  const value = {
    ...state,
    login,
    register,
    logout,
    clearError
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

