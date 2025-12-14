# API Services Documentation

## Overview

This document describes the React API services built with Axios for the Khadamni job search platform.

## Service Structure

```
src/services/api/
├── client.ts          # Axios instances and interceptors
├── auth.ts            # Authentication services
├── jobs.ts            # Job-related services
├── ml.ts              # ML-powered services
└── index.ts           # Central exports
```

## API Clients

### Main API Client (`apiClient`)
- Base URL: `http://localhost:8000/api/v1`
- Handles backend API calls
- Includes authentication token in headers
- Auto-redirects on 401 errors

### ML Service Client (`mlClient`)
- Base URL: `http://localhost:8001/api`
- Handles ML microservice calls
- No authentication required (internal service)

## Authentication Service

### `authApi.register(userData)`
Register a new user.

```typescript
const result = await authApi.register({
  email: 'user@example.com',
  password: 'password123',
  role: 'JOB_SEEKER'
});
```

### `authApi.login(credentials)`
Login and get tokens (automatically stored).

```typescript
const tokens = await authApi.login({
  email: 'user@example.com',
  password: 'password123'
});
```

### `authApi.logout()`
Clear authentication tokens.

### `authApi.getCurrentUser()`
Get current authenticated user.

### `authApi.isAuthenticated()`
Check if user is authenticated.

## Jobs Service

### `jobsApi.getJobs(params?)`
Get all jobs with optional filters.

```typescript
const jobs = await jobsApi.getJobs({
  location: 'New York',
  limit: 20,
  skip: 0
});
```

### `jobsApi.getJobById(id)`
Get a single job by ID.

### `jobsApi.createJob(jobData)`
Create a new job posting (recruiter only).

### `jobsApi.updateJob(id, jobData)`
Update a job posting (recruiter only).

### `jobsApi.deleteJob(id)`
Delete a job posting (recruiter only).

### `jobsApi.applyToJob(jobId, applicationData)`
Apply to a job.

### `jobsApi.getMyApplications(skip?, limit?)`
Get user's applications.

### `jobsApi.getJobApplications(jobId, skip?, limit?)`
Get applications for a job (recruiter only).

## ML Services

### `mlApi.predictSalary(request)`
Predict salary based on job and employee features.

```typescript
const prediction = await mlApi.predictSalary({
  work_year: 2024,
  experience_level: 'MID_LEVEL',
  employment_type: 'FULL_TIME',
  job_title: 'Software Engineer',
  employee_residence: 'US',
  remote_ratio: 50,
  company_location: 'US',
  company_size: 'LARGE'
});
```

### `mlApi.getJobRecommendations(profile)`
Get personalized job recommendations.

```typescript
const recommendations = await mlApi.getJobRecommendations({
  experience_level: 'MID_LEVEL',
  skills: ['Python', 'FastAPI', 'PostgreSQL'],
  preferred_location: 'US'
});
```

### `mlApi.getCountryRecommendations(request)`
Get country recommendations for job hunting.

```typescript
const countries = await mlApi.getCountryRecommendations({
  job_title: 'Software Engineer',
  experience_level: 'MID_LEVEL'
});
```

### `mlApi.detectFraud(request)`
Detect fraud in job posting.

## React Hooks

### `useAuth()`
Hook for authentication with loading and error states.

```typescript
const { login, register, logout, isLoading, error, isAuthenticated } = useAuth();

await login({ email: 'user@example.com', password: 'password' });
```

### `useJobs()`
Hook for job operations.

```typescript
const { 
  jobs, 
  isLoading, 
  error, 
  getJobs, 
  createJob, 
  applyToJob 
} = useJobs();

await getJobs({ location: 'New York' });
```

### `useML()`
Hook for ML-powered features.

```typescript
const { 
  predictSalary, 
  salaryPrediction, 
  isLoading, 
  error 
} = useML();

await predictSalary({ ... });
```

## Error Handling

### Error Interceptors
- Automatically handle 401 errors (redirect to login)
- Extract error messages from API responses
- Log errors to console for debugging

### Error Utilities
- `formatError(error)`: Format error for display
- `isNetworkError(error)`: Check if network error
- `isAuthError(error)`: Check if authentication error
- `getUserFriendlyError(error)`: Get user-friendly message

### ErrorDisplay Component
Reusable component for displaying errors:

```tsx
<ErrorDisplay 
  error={error} 
  onDismiss={() => setError(null)} 
/>
```

## Loading States

### LoadingSpinner Component
Reusable loading indicator:

```tsx
<LoadingSpinner size="md" text="Loading..." />
```

### Hook Loading States
All hooks provide `isLoading` state:

```tsx
const { isLoading, getJobs } = useJobs();

if (isLoading) {
  return <LoadingSpinner />;
}
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_ML_SERVICE_URL=http://localhost:8001
```

## Usage Examples

### Complete Authentication Flow

```typescript
import { useAuth } from '@/hooks/useAuth';

function LoginPage() {
  const { login, isLoading, error } = useAuth();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login({ email, password });
      // Redirect on success
    } catch (err) {
      // Error is already set in hook
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {error && <ErrorDisplay error={error} />}
      <button disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Login'}
      </button>
    </form>
  );
}
```

### Fetching Jobs with Filters

```typescript
import { useJobs } from '@/hooks/useJobs';

function JobsPage() {
  const { jobs, isLoading, error, getJobs } = useJobs();
  
  useEffect(() => {
    getJobs({ location: 'New York', limit: 20 });
  }, []);
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay error={error} />;
  
  return (
    <div>
      {jobs.map(job => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
```

### ML Salary Prediction

```typescript
import { useML } from '@/hooks/useML';

function SalaryPredictionPage() {
  const { predictSalary, salaryPrediction, isLoading, error } = useML();
  
  const handlePredict = async () => {
    try {
      await predictSalary({
        work_year: 2024,
        experience_level: 'MID_LEVEL',
        // ... other fields
      });
    } catch (err) {
      // Error handled
    }
  };
  
  return (
    <div>
      <button onClick={handlePredict} disabled={isLoading}>
        Predict Salary
      </button>
      {salaryPrediction && (
        <div>${salaryPrediction.predicted_salary_usd}</div>
      )}
    </div>
  );
}
```

## Best Practices

1. **Always use hooks** for state management
2. **Handle errors** with ErrorDisplay component
3. **Show loading states** with LoadingSpinner
4. **Clear errors** when retrying operations
5. **Use TypeScript** for type safety
6. **Handle edge cases** (network errors, timeouts)

## Type Safety

All services are fully typed with TypeScript:
- Request/response interfaces
- Error types
- Hook return types
- Component props

## Testing

Services can be tested by:
1. Mocking Axios instances
2. Testing error scenarios
3. Verifying loading states
4. Checking token storage

