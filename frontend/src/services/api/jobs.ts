/**
 * Jobs API Service
 * 
 * Handles all job-related API calls with error handling
 */

import apiClient from './client';
import { AxiosError } from 'axios';

export interface Job {
  id: string;
  title: string;
  description: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  required_skills: string[];
  recruiter_id: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface JobCreate {
  title: string;
  description: string;
  location: string;
  salary_min?: number;
  salary_max?: number;
  required_skills: string[];
}

export interface JobUpdate {
  title?: string;
  description?: string;
  location?: string;
  salary_min?: number;
  salary_max?: number;
  required_skills?: string[];
}

export interface JobSearchParams {
  skip?: number;
  limit?: number;
  location?: string;
  title?: string;
  is_active?: boolean;
}

export interface JobApplicationCreate {
  cover_letter?: string;
  resume_url?: string;
}

export interface JobApplication {
  id: string;
  job_id: string;
  job_seeker_id: string;
  status: string;
  cover_letter?: string;
  resume_url?: string;
  applied_at: string;
  reviewed_at?: string;
}

/**
 * Jobs API service
 */
export const jobsApi = {
  /**
   * Get all jobs with optional filters
   */
  getJobs: async (params?: JobSearchParams): Promise<Job[]> => {
    try {
      const response = await apiClient.get<Job[]>('/jobs', { params });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      throw new Error(axiosError.response?.data?.detail || 'Failed to fetch jobs');
    }
  },

  /**
   * Get a single job by ID
   */
  getJobById: async (id: string): Promise<Job> => {
    try {
      const response = await apiClient.get<Job>(`/jobs/${id}`);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 404) {
        throw new Error('Job not found');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to fetch job');
    }
  },

  /**
   * Create a new job posting (recruiter only)
   */
  createJob: async (jobData: JobCreate): Promise<Job> => {
    try {
      const response = await apiClient.post<Job>('/jobs', jobData);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      throw new Error(axiosError.response?.data?.detail || 'Failed to create job');
    }
  },

  /**
   * Update a job posting (recruiter only)
   */
  updateJob: async (id: string, jobData: JobUpdate): Promise<Job> => {
    try {
      const response = await apiClient.put<Job>(`/jobs/${id}`, jobData);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 404) {
        throw new Error('Job not found');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to update job');
    }
  },

  /**
   * Delete a job posting (recruiter only)
   */
  deleteJob: async (id: string): Promise<void> => {
    try {
      await apiClient.delete(`/jobs/${id}`);
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 404) {
        throw new Error('Job not found');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to delete job');
    }
  },

  /**
   * Apply to a job (job seeker only)
   */
  applyToJob: async (jobId: string, applicationData: JobApplicationCreate): Promise<JobApplication> => {
    try {
      const response = await apiClient.post<JobApplication>(
        `/jobs/${jobId}/apply`,
        applicationData
      );
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 400) {
        throw new Error(axiosError.response?.data?.detail || 'Invalid application data');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to apply to job');
    }
  },

  /**
   * Get user's applications
   */
  getMyApplications: async (skip: number = 0, limit: number = 20): Promise<JobApplication[]> => {
    try {
      const response = await apiClient.get<JobApplication[]>('/applications/my-applications', {
        params: { skip, limit },
      });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      throw new Error(axiosError.response?.data?.detail || 'Failed to fetch applications');
    }
  },

  /**
   * Get applications for a job (recruiter only)
   */
  getJobApplications: async (jobId: string, skip: number = 0, limit: number = 20): Promise<JobApplication[]> => {
    try {
      const response = await apiClient.get<JobApplication[]>(`/applications/job/${jobId}`, {
        params: { skip, limit },
      });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<{ detail?: string }>;
      if (axiosError.response?.status === 404) {
        throw new Error('Job not found');
      }
      throw new Error(axiosError.response?.data?.detail || 'Failed to fetch applications');
    }
  },
};
