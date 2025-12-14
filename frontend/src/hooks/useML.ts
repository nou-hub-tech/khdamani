/**
 * ML Services Hook
 * 
 * React hook for ML-powered features with loading and error states
 */

import { useState, useCallback } from 'react';
import {
  mlApi,
  SalaryPredictionRequest,
  SalaryPredictionResponse,
  JobSeekerProfile,
  JobRecommendationResponse,
  CountryRecommendationRequest,
  CountryRecommendationResponse,
  FraudDetectionRequest,
  FraudDetectionResponse,
} from '@/services/api/ml';

interface UseMLReturn {
  // Salary Prediction
  salaryPrediction: SalaryPredictionResponse | null;
  predictSalary: (request: SalaryPredictionRequest) => Promise<SalaryPredictionResponse>;
  
  // Job Recommendations
  jobRecommendations: JobRecommendationResponse | null;
  getJobRecommendations: (profile: JobSeekerProfile) => Promise<JobRecommendationResponse>;
  
  // Country Recommendations
  countryRecommendations: CountryRecommendationResponse | null;
  getCountryRecommendations: (request: CountryRecommendationRequest) => Promise<CountryRecommendationResponse>;
  
  // Fraud Detection
  fraudDetection: FraudDetectionResponse | null;
  detectFraud: (request: FraudDetectionRequest) => Promise<FraudDetectionResponse>;
  
  // Common states
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

export const useML = (): UseMLReturn => {
  const [salaryPrediction, setSalaryPrediction] = useState<SalaryPredictionResponse | null>(null);
  const [jobRecommendations, setJobRecommendations] = useState<JobRecommendationResponse | null>(null);
  const [countryRecommendations, setCountryRecommendations] = useState<CountryRecommendationResponse | null>(null);
  const [fraudDetection, setFraudDetection] = useState<FraudDetectionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const predictSalary = useCallback(async (request: SalaryPredictionRequest): Promise<SalaryPredictionResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await mlApi.predictSalary(request);
      setSalaryPrediction(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to predict salary';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getJobRecommendations = useCallback(async (profile: JobSeekerProfile): Promise<JobRecommendationResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await mlApi.getJobRecommendations(profile);
      setJobRecommendations(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get job recommendations';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getCountryRecommendations = useCallback(async (request: CountryRecommendationRequest): Promise<CountryRecommendationResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await mlApi.getCountryRecommendations(request);
      setCountryRecommendations(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get country recommendations';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const detectFraud = useCallback(async (request: FraudDetectionRequest): Promise<FraudDetectionResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await mlApi.detectFraud(request);
      setFraudDetection(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to detect fraud';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    salaryPrediction,
    predictSalary,
    jobRecommendations,
    getJobRecommendations,
    countryRecommendations,
    getCountryRecommendations,
    fraudDetection,
    detectFraud,
    isLoading,
    error,
    clearError,
  };
};

