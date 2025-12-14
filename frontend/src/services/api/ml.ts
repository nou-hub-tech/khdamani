/**
 * ML Services API
 * 
 * Handles ML-powered feature API calls to the ML microservice
 */

import { mlClient } from './client';
import { AxiosError } from 'axios';

/**
 * Salary Prediction
 */
export interface SalaryPredictionRequest {
  work_year: number;
  experience_level: 'ENTRY_LEVEL' | 'JUNIOR' | 'MID_LEVEL' | 'SENIOR' | 'EXECUTIVE';
  employment_type: 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'TEMPORARY' | 'INTERNSHIP' | 'FREELANCE';
  job_title: string;
  employee_residence: string;
  remote_ratio: number;
  company_location: string;
  company_size: 'STARTUP' | 'SMALL' | 'MEDIUM' | 'LARGE' | 'ENTERPRISE';
}

export interface SalaryPredictionResponse {
  predicted_salary_usd: number;
  salary_range_min: number;
  salary_range_max: number;
  confidence_score: number;
}

/**
 * Job Recommendations
 */
export interface JobSeekerProfile {
  experience_level: 'ENTRY_LEVEL' | 'JUNIOR' | 'MID_LEVEL' | 'SENIOR' | 'EXECUTIVE';
  skills: string[];
  preferred_location?: string;
  preferred_employment_type?: 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'TEMPORARY' | 'INTERNSHIP' | 'FREELANCE';
  desired_salary_min?: number;
  desired_salary_max?: number;
}

export interface RecommendedJob {
  job_id: string;
  title: string;
  company: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  match_score: number;
  match_reasons: string[];
}

export interface JobRecommendationResponse {
  recommended_jobs: RecommendedJob[];
  total_matches: number;
}

/**
 * Country Recommendations
 */
export interface CountryRecommendationRequest {
  job_title: string;
  experience_level: 'ENTRY_LEVEL' | 'JUNIOR' | 'MID_LEVEL' | 'SENIOR' | 'EXECUTIVE';
}

export interface CountryRecommendation {
  country: string;
  country_code: string;
  score: number;
  average_salary_usd: number;
  job_opportunities: number;
  growth_rate: number;
  reasons: string[];
}

export interface CountryRecommendationResponse {
  recommended_countries: CountryRecommendation[];
}

/**
 * Fraud Detection
 */
export interface FraudDetectionRequest {
  job_posting: {
    title: string;
    description: string;
    location: string;
    salary_min?: number;
    salary_max?: number;
    [key: string]: any;
  };
}

export interface FraudDetectionResponse {
  is_fraud: boolean;
  fraud_probability: number;
  reasons: string[];
}

/**
 * ML API service
 */
export const mlApi = {
  /**
   * Predict salary for a job
   */
  predictSalary: async (
    request: SalaryPredictionRequest
  ): Promise<SalaryPredictionResponse> => {
    try {
      const response = await mlClient.post<SalaryPredictionResponse>(
        '/salary/predict-salary',
        request
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 400) {
        throw new Error(axiosError.response?.data?.detail || 'Invalid prediction request');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to predict salary');
    }
  },

  /**
   * Get job recommendations based on profile
   */
  getJobRecommendations: async (
    profile: JobSeekerProfile
  ): Promise<JobRecommendationResponse> => {
    try {
      const response = await mlClient.post<JobRecommendationResponse>(
        '/jobs/recommend-jobs',
        profile
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 400) {
        throw new Error(axiosError.response?.data?.detail || 'Invalid profile data');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to get job recommendations');
    }
  },

  /**
   * Get country recommendations
   */
  getCountryRecommendations: async (
    request: CountryRecommendationRequest
  ): Promise<CountryRecommendationResponse> => {
    try {
      const response = await mlClient.post<CountryRecommendationResponse>(
        '/country/recommend-countries',
        request
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 400) {
        throw new Error(axiosError.response?.data?.detail || 'Invalid request data');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to get country recommendations');
    }
  },

  /**
   * Detect fraud in job posting
   */
  detectFraud: async (
    request: FraudDetectionRequest
  ): Promise<FraudDetectionResponse> => {
    try {
      const response = await mlClient.post<FraudDetectionResponse>(
        '/fraud/detect',
        request
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 400) {
        throw new Error(axiosError.response?.data?.detail || 'Invalid job posting data');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to detect fraud');
    }
  },
};
