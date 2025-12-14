/**
 * Job Type Definitions
 */

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

export interface JobSearchParams {
  skip?: number;
  limit?: number;
  location?: string;
  title?: string;
}

