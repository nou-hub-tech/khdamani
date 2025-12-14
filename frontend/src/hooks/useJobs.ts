/**
 * Jobs Hook
 * 
 * React hook for job operations with loading and error states
 */

import { useState, useCallback } from 'react';
import { jobsApi, Job, JobCreate, JobUpdate, JobSearchParams, JobApplicationCreate, JobApplication } from '@/services/api/jobs';

interface UseJobsReturn {
  jobs: Job[];
  job: Job | null;
  applications: JobApplication[];
  isLoading: boolean;
  error: string | null;
  getJobs: (params?: JobSearchParams) => Promise<void>;
  getJobById: (id: string) => Promise<void>;
  createJob: (jobData: JobCreate) => Promise<Job>;
  updateJob: (id: string, jobData: JobUpdate) => Promise<Job>;
  deleteJob: (id: string) => Promise<void>;
  applyToJob: (jobId: string, applicationData: JobApplicationCreate) => Promise<JobApplication>;
  getMyApplications: (skip?: number, limit?: number) => Promise<void>;
  getJobApplications: (jobId: string, skip?: number, limit?: number) => Promise<void>;
  clearError: () => void;
}

export const useJobs = (): UseJobsReturn => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [job, setJob] = useState<Job | null>(null);
  const [applications, setApplications] = useState<JobApplication[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getJobs = useCallback(async (params?: JobSearchParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.getJobs(params);
      setJobs(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch jobs';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getJobById = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.getJobById(id);
      setJob(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch job';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createJob = useCallback(async (jobData: JobCreate): Promise<Job> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.createJob(jobData);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create job';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateJob = useCallback(async (id: string, jobData: JobUpdate): Promise<Job> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.updateJob(id, jobData);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update job';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteJob = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await jobsApi.deleteJob(id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete job';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const applyToJob = useCallback(async (jobId: string, applicationData: JobApplicationCreate): Promise<JobApplication> => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.applyToJob(jobId, applicationData);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to apply to job';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getMyApplications = useCallback(async (skip: number = 0, limit: number = 20) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.getMyApplications(skip, limit);
      setApplications(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch applications';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getJobApplications = useCallback(async (jobId: string, skip: number = 0, limit: number = 20) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await jobsApi.getJobApplications(jobId, skip, limit);
      setApplications(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch applications';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    jobs,
    job,
    applications,
    isLoading,
    error,
    getJobs,
    getJobById,
    createJob,
    updateJob,
    deleteJob,
    applyToJob,
    getMyApplications,
    getJobApplications,
    clearError,
  };
};

