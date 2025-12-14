/**
 * Error Handler Utilities
 * 
 * Centralized error handling and formatting
 */

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
  field?: string;
}

/**
 * Format error message for display
 */
export const formatError = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  
  if (typeof error === 'string') {
    return error;
  }
  
  return 'An unexpected error occurred';
};

/**
 * Check if error is a network error
 */
export const isNetworkError = (error: unknown): boolean => {
  if (error instanceof Error) {
    return error.message.includes('Network Error') || 
           error.message.includes('timeout') ||
           error.message.includes('ECONNREFUSED');
  }
  return false;
};

/**
 * Check if error is an authentication error
 */
export const isAuthError = (error: unknown): boolean => {
  if (error instanceof Error) {
    return error.message.includes('401') || 
           error.message.includes('Unauthorized') ||
           error.message.includes('authentication');
  }
  return false;
};

/**
 * Get user-friendly error message
 */
export const getUserFriendlyError = (error: unknown): string => {
  const message = formatError(error);
  
  if (isNetworkError(error)) {
    return 'Unable to connect to the server. Please check your internet connection.';
  }
  
  if (isAuthError(error)) {
    return 'Your session has expired. Please log in again.';
  }
  
  return message;
};

