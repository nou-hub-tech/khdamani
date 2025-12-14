/**
 * Authentication Hook
 * 
 * React hook for authentication with loading and error states
 */

import { useState, useCallback } from 'react';
import { authApi, UserRegister, UserLogin, TokenResponse, User } from '@/services/api/auth';

interface UseAuthReturn {
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegister) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  user: User | null;
}

export const useAuth = (): UseAuthReturn => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (credentials: UserLogin) => {
    setIsLoading(true);
    setError(null);
    try {
      const tokens = await authApi.login(credentials);
      // Optionally fetch user data
      const currentUser = await authApi.getCurrentUser();
      setUser(currentUser);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (userData: UserRegister) => {
    setIsLoading(true);
    setError(null);
    try {
      await authApi.register(userData);
      // Auto-login after registration
      await login({ email: userData.email, password: userData.password });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Registration failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [login]);

  const logout = useCallback(() => {
    authApi.logout();
    setUser(null);
    setError(null);
  }, []);

  return {
    login,
    register,
    logout,
    isLoading,
    error,
    isAuthenticated: authApi.isAuthenticated(),
    user,
  };
};

