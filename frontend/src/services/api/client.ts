/**
 * API Client Configuration
 * 
 * This file sets up the axios instance for API communication
 * with authentication interceptors and error handling.
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const ML_SERVICE_URL = import.meta.env.VITE_ML_SERVICE_URL || 'http://localhost:8001';

// Main API client for backend
export const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// ML Service client (separate microservice)
export const mlClient: AxiosInstance = axios.create({
  baseURL: `${ML_SERVICE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor: Add authentication token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string; message?: string }>) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    // Extract error message
    const message = error.response?.data?.detail || 
                   error.response?.data?.message || 
                   error.message || 
                   'An unexpected error occurred';
    
    console.error('API Error:', {
      status: error.response?.status,
      message,
      url: error.config?.url,
    });
    
    return Promise.reject(new Error(message));
  }
);

// ML Service error handling
mlClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string; message?: string }>) => {
    const message = error.response?.data?.detail || 
                   error.response?.data?.message || 
                   error.message || 
                   'ML service error occurred';
    
    console.error('ML Service Error:', {
      status: error.response?.status,
      message,
      url: error.config?.url,
    });
    
    return Promise.reject(new Error(message));
  }
);

export default apiClient;
