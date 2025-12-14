/**
 * Authentication API Service
 * 
 * Handles user authentication (login, register, logout)
 */

import apiClient from './client';
import { AxiosError } from 'axios';

export interface UserRegister {
  email: string;
  password: string;
  role: 'JOB_SEEKER' | 'RECRUITER';
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  role: 'JOB_SEEKER' | 'RECRUITER' | 'ADMIN';
  is_active: boolean;
  created_at: string;
}

export interface AuthError {
  message: string;
  status?: number;
  field?: string;
}

/**
 * Authentication API service
 */
export const authApi = {
  /**
   * Register a new user
   */
  register: async (userData: UserRegister): Promise<{ user_id: string; message: string }> => {
    try {
      const response = await apiClient.post<{ user_id: string; message: string }>(
        '/auth/register',
        userData
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      throw new Error(axiosError.response?.data?.detail || 'Registration failed');
    }
  },

  /**
   * Login user and get tokens
   */
  login: async (credentials: UserLogin): Promise<TokenResponse> => {
    try {
      const response = await apiClient.post<TokenResponse>(
        '/auth/login',
        credentials
      );
      
      // Store tokens
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      throw new Error(axiosError.response?.data?.detail || 'Login failed');
    }
  },

  /**
   * Logout user (clear tokens)
   */
  logout: (): void => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  /**
   * Get current user (if authenticated)
   */
  getCurrentUser: async (): Promise<User | null> => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return null;

      // This endpoint would need to be implemented in the backend
      // For now, decode token or call a /me endpoint
      const response = await apiClient.get<User>('/auth/me');
      return response.data;
    } catch (error) {
      // If token is invalid, clear it
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return null;
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },

  /**
   * Get stored access token
   */
  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },
};

