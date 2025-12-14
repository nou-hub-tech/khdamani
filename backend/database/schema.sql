-- ============================================================================
-- Job Search Platform - PostgreSQL Database Schema
-- ============================================================================
-- This schema is designed for a job search platform with ML features
-- Uses UUID primary keys, ENUMs, and proper referential integrity
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

-- User roles
CREATE TYPE user_role AS ENUM ('JOB_SEEKER', 'RECRUITER', 'ADMIN');

-- Experience levels
CREATE TYPE experience_level AS ENUM (
    'ENTRY_LEVEL',
    'JUNIOR',
    'MID_LEVEL',
    'SENIOR',
    'EXECUTIVE'
);

-- Education levels
CREATE TYPE education_level AS ENUM (
    'HIGH_SCHOOL',
    'ASSOCIATE',
    'BACHELOR',
    'MASTER',
    'DOCTORATE',
    'OTHER'
);

-- Employment types
CREATE TYPE employment_type AS ENUM (
    'FULL_TIME',
    'PART_TIME',
    'CONTRACT',
    'TEMPORARY',
    'INTERNSHIP',
    'FREELANCE'
);

-- Application status
CREATE TYPE application_status AS ENUM (
    'APPLIED',
    'REVIEWED',
    'SHORTLISTED',
    'INTERVIEWED',
    'ACCEPTED',
    'REJECTED',
    'WITHDRAWN'
);

-- Company sizes
CREATE TYPE company_size AS ENUM (
    'STARTUP',
    'SMALL',
    'MEDIUM',
    'LARGE',
    'ENTERPRISE'
);

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. users
-- ----------------------------------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'JOB_SEEKER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT users_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Indexes for users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- ----------------------------------------------------------------------------
-- 2. job_seeker_profiles
-- ----------------------------------------------------------------------------
CREATE TABLE job_seeker_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    experience_level experience_level,
    education_level education_level,
    current_country VARCHAR(100),
    desired_job_title VARCHAR(255),
    skills TEXT[], -- Array of skills
    bio TEXT,
    resume_url VARCHAR(500),
    profile_picture_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT job_seeker_profiles_user_id_unique UNIQUE (user_id)
);

-- Indexes for job_seeker_profiles
CREATE INDEX idx_job_seeker_profiles_user_id ON job_seeker_profiles(user_id);
CREATE INDEX idx_job_seeker_profiles_experience_level ON job_seeker_profiles(experience_level);
CREATE INDEX idx_job_seeker_profiles_current_country ON job_seeker_profiles(current_country);
CREATE INDEX idx_job_seeker_profiles_desired_job_title ON job_seeker_profiles(desired_job_title);
CREATE INDEX idx_job_seeker_profiles_skills ON job_seeker_profiles USING GIN(skills);

-- ----------------------------------------------------------------------------
-- 3. recruiter_profiles
-- ----------------------------------------------------------------------------
CREATE TABLE recruiter_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_size company_size,
    company_location VARCHAR(255),
    industry VARCHAR(100),
    company_description TEXT,
    company_website VARCHAR(500),
    company_logo_url VARCHAR(500),
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT recruiter_profiles_user_id_unique UNIQUE (user_id)
);

-- Indexes for recruiter_profiles
CREATE INDEX idx_recruiter_profiles_user_id ON recruiter_profiles(user_id);
CREATE INDEX idx_recruiter_profiles_company_name ON recruiter_profiles(company_name);
CREATE INDEX idx_recruiter_profiles_industry ON recruiter_profiles(industry);
CREATE INDEX idx_recruiter_profiles_verified ON recruiter_profiles(verified);

-- ----------------------------------------------------------------------------
-- 4. job_postings
-- ----------------------------------------------------------------------------
CREATE TABLE job_postings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recruiter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    salary_min DECIMAL(12, 2),
    salary_max DECIMAL(12, 2),
    salary_currency VARCHAR(3) DEFAULT 'USD',
    employment_type employment_type NOT NULL DEFAULT 'FULL_TIME',
    required_experience experience_level,
    required_education education_level,
    industry VARCHAR(100),
    function VARCHAR(100), -- Job function (e.g., Engineering, Sales, Marketing)
    description TEXT NOT NULL,
    requirements TEXT,
    company_profile TEXT,
    required_skills TEXT[], -- Array of required skills
    benefits TEXT[], -- Array of benefits
    is_fraud BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    views_count INTEGER NOT NULL DEFAULT 0,
    applications_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT job_postings_salary_range CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max)
);

-- Indexes for job_postings
CREATE INDEX idx_job_postings_recruiter_id ON job_postings(recruiter_id);
CREATE INDEX idx_job_postings_title ON job_postings(title);
CREATE INDEX idx_job_postings_location ON job_postings(location);
CREATE INDEX idx_job_postings_employment_type ON job_postings(employment_type);
CREATE INDEX idx_job_postings_industry ON job_postings(industry);
CREATE INDEX idx_job_postings_function ON job_postings(function);
CREATE INDEX idx_job_postings_is_fraud ON job_postings(is_fraud);
CREATE INDEX idx_job_postings_is_active ON job_postings(is_active);
CREATE INDEX idx_job_postings_created_at ON job_postings(created_at DESC);
CREATE INDEX idx_job_postings_required_skills ON job_postings USING GIN(required_skills);
CREATE INDEX idx_job_postings_salary_range ON job_postings(salary_min, salary_max) WHERE salary_min IS NOT NULL;

-- Full-text search index for job postings
CREATE INDEX idx_job_postings_fulltext ON job_postings USING GIN(
    to_tsvector('english', 
        COALESCE(title, '') || ' ' || 
        COALESCE(description, '') || ' ' || 
        COALESCE(requirements, '')
    )
);

-- ----------------------------------------------------------------------------
-- 5. job_applications
-- ----------------------------------------------------------------------------
CREATE TABLE job_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    job_seeker_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status application_status NOT NULL DEFAULT 'APPLIED',
    cover_letter TEXT,
    resume_url VARCHAR(500),
    applied_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT job_applications_unique_application UNIQUE (job_id, job_seeker_id)
);

-- Indexes for job_applications
CREATE INDEX idx_job_applications_job_id ON job_applications(job_id);
CREATE INDEX idx_job_applications_job_seeker_id ON job_applications(job_seeker_id);
CREATE INDEX idx_job_applications_status ON job_applications(status);
CREATE INDEX idx_job_applications_applied_at ON job_applications(applied_at DESC);
CREATE INDEX idx_job_applications_job_seeker_status ON job_applications(job_seeker_id, status);

-- ============================================================================
-- ML RESULT TABLES (LIGHTWEIGHT)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 6. salary_predictions
-- ----------------------------------------------------------------------------
CREATE TABLE salary_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    job_id UUID REFERENCES job_postings(id) ON DELETE SET NULL,
    job_title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    experience_level experience_level,
    education_level education_level,
    predicted_salary_usd DECIMAL(12, 2) NOT NULL,
    salary_min_usd DECIMAL(12, 2),
    salary_max_usd DECIMAL(12, 2),
    confidence_score DECIMAL(5, 4), -- 0.0000 to 1.0000
    model_version VARCHAR(50) NOT NULL,
    input_features JSONB, -- Store input features for debugging/analysis
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT salary_predictions_confidence_range CHECK (confidence_score IS NULL OR (confidence_score >= 0 AND confidence_score <= 1))
);

-- Indexes for salary_predictions
CREATE INDEX idx_salary_predictions_user_id ON salary_predictions(user_id);
CREATE INDEX idx_salary_predictions_job_id ON salary_predictions(job_id);
CREATE INDEX idx_salary_predictions_job_title ON salary_predictions(job_title);
CREATE INDEX idx_salary_predictions_location ON salary_predictions(location);
CREATE INDEX idx_salary_predictions_created_at ON salary_predictions(created_at DESC);
CREATE INDEX idx_salary_predictions_model_version ON salary_predictions(model_version);

-- ----------------------------------------------------------------------------
-- 7. fraud_detection_results
-- ----------------------------------------------------------------------------
CREATE TABLE fraud_detection_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    fraud_probability DECIMAL(5, 4) NOT NULL, -- 0.0000 to 1.0000
    is_fraud BOOLEAN NOT NULL DEFAULT FALSE,
    model_version VARCHAR(50) NOT NULL,
    detected_features JSONB, -- Store features that contributed to detection
    reasons TEXT[], -- Array of reasons why flagged as fraud
    reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    detected_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT fraud_detection_results_probability_range CHECK (fraud_probability >= 0 AND fraud_probability <= 1)
);

-- Indexes for fraud_detection_results
CREATE INDEX idx_fraud_detection_results_job_id ON fraud_detection_results(job_id);
CREATE INDEX idx_fraud_detection_results_is_fraud ON fraud_detection_results(is_fraud);
CREATE INDEX idx_fraud_detection_results_fraud_probability ON fraud_detection_results(fraud_probability DESC);
CREATE INDEX idx_fraud_detection_results_detected_at ON fraud_detection_results(detected_at DESC);
CREATE INDEX idx_fraud_detection_results_model_version ON fraud_detection_results(model_version);

-- ----------------------------------------------------------------------------
-- 8. country_recommendations
-- ----------------------------------------------------------------------------
CREATE TABLE country_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_title VARCHAR(255),
    experience_level experience_level,
    skills TEXT[],
    recommended_countries TEXT[] NOT NULL, -- Array of country codes or names
    country_scores JSONB, -- { "country": "score" } mapping
    model_version VARCHAR(50) NOT NULL,
    input_features JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT country_recommendations_countries_not_empty CHECK (array_length(recommended_countries, 1) > 0)
);

-- Indexes for country_recommendations
CREATE INDEX idx_country_recommendations_user_id ON country_recommendations(user_id);
CREATE INDEX idx_country_recommendations_job_title ON country_recommendations(job_title);
CREATE INDEX idx_country_recommendations_created_at ON country_recommendations(created_at DESC);
CREATE INDEX idx_country_recommendations_model_version ON country_recommendations(model_version);
CREATE INDEX idx_country_recommendations_countries ON country_recommendations USING GIN(recommended_countries);

-- ============================================================================
-- ADDITIONAL TABLES FOR ML FEATURES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 9. job_recommendations (for ML job recommendation feature)
-- ----------------------------------------------------------------------------
CREATE TABLE job_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    recommendation_score DECIMAL(5, 4) NOT NULL, -- 0.0000 to 1.0000
    model_version VARCHAR(50) NOT NULL,
    recommendation_reasons TEXT[], -- Why this job was recommended
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE, -- Recommendations can expire
    
    -- Constraints
    CONSTRAINT job_recommendations_score_range CHECK (recommendation_score >= 0 AND recommendation_score <= 1),
    CONSTRAINT job_recommendations_unique UNIQUE (user_id, job_id, model_version)
);

-- Indexes for job_recommendations
CREATE INDEX idx_job_recommendations_user_id ON job_recommendations(user_id);
CREATE INDEX idx_job_recommendations_job_id ON job_recommendations(job_id);
CREATE INDEX idx_job_recommendations_score ON job_recommendations(recommendation_score DESC);
CREATE INDEX idx_job_recommendations_created_at ON job_recommendations(created_at DESC);
CREATE INDEX idx_job_recommendations_user_score ON job_recommendations(user_id, recommendation_score DESC);

-- ----------------------------------------------------------------------------
-- 10. user_job_interactions (for ML training data collection)
-- ----------------------------------------------------------------------------
CREATE TABLE user_job_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL, -- 'VIEW', 'CLICK', 'APPLY', 'SAVE', 'SHARE'
    interaction_data JSONB, -- Additional interaction metadata
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT user_job_interactions_type_check CHECK (interaction_type IN ('VIEW', 'CLICK', 'APPLY', 'SAVE', 'SHARE', 'DISMISS'))
);

-- Indexes for user_job_interactions
CREATE INDEX idx_user_job_interactions_user_id ON user_job_interactions(user_id);
CREATE INDEX idx_user_job_interactions_job_id ON user_job_interactions(job_id);
CREATE INDEX idx_user_job_interactions_type ON user_job_interactions(interaction_type);
CREATE INDEX idx_user_job_interactions_created_at ON user_job_interactions(created_at DESC);
CREATE INDEX idx_user_job_interactions_user_job ON user_job_interactions(user_id, job_id);

-- ============================================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_seeker_profiles_updated_at BEFORE UPDATE ON job_seeker_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recruiter_profiles_updated_at BEFORE UPDATE ON recruiter_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_postings_updated_at BEFORE UPDATE ON job_postings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_applications_updated_at BEFORE UPDATE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- FUNCTIONS FOR STATISTICS
-- ============================================================================

-- Function to update job_postings applications_count
CREATE OR REPLACE FUNCTION update_job_applications_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE job_postings
        SET applications_count = applications_count + 1
        WHERE id = NEW.job_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE job_postings
        SET applications_count = GREATEST(applications_count - 1, 0)
        WHERE id = OLD.job_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_job_applications_count
    AFTER INSERT OR DELETE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION update_job_applications_count();

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE users IS 'Core user accounts for both job seekers and recruiters';
COMMENT ON TABLE job_seeker_profiles IS 'Extended profile information for job seekers';
COMMENT ON TABLE recruiter_profiles IS 'Extended profile information for recruiters';
COMMENT ON TABLE job_postings IS 'Job postings created by recruiters';
COMMENT ON TABLE job_applications IS 'Applications submitted by job seekers';
COMMENT ON TABLE salary_predictions IS 'ML model predictions for salary estimates';
COMMENT ON TABLE fraud_detection_results IS 'ML model results for fraud detection on job postings';
COMMENT ON TABLE country_recommendations IS 'ML model recommendations for countries based on user profile';
COMMENT ON TABLE job_recommendations IS 'ML model recommendations for jobs based on user profile';
COMMENT ON TABLE user_job_interactions IS 'User interactions with jobs for ML training data collection';

