import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { JobSeekerDashboard } from './pages/JobSeekerDashboard';
import { SalaryPredictionPage } from './pages/SalaryPredictionPage';
import { JobRecommendationsPage } from './pages/JobRecommendationsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<JobSeekerDashboard />} />
        <Route path="/salary-prediction" element={<SalaryPredictionPage />} />
        <Route path="/job-recommendations" element={<JobRecommendationsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

