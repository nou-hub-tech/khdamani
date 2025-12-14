import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { TrendingUp, Sparkles } from 'lucide-react';

export const SalaryPredictionPage: React.FC = () => {
  const [formData, setFormData] = useState({
    work_year: 2024,
    experience_level: 'MID_LEVEL',
    employment_type: 'FULL_TIME',
    job_title: '',
    employee_residence: 'US',
    remote_ratio: 50,
    company_location: 'US',
    company_size: 'LARGE',
  });
  const [prediction, setPrediction] = useState<{
    predicted_salary_usd: number;
    salary_range_min: number;
    salary_range_max: number;
    confidence_score: number;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // TODO: API call
    setTimeout(() => {
      setPrediction({
        predicted_salary_usd: 125000,
        salary_range_min: 100000,
        salary_range_max: 150000,
        confidence_score: 0.85,
      });
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 p-4 md:p-8">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 text-center"
        >
          <h1 className="text-4xl font-bold font-display mb-2">
            AI-Powered <span className="text-gradient">Salary Prediction</span>
          </h1>
          <p className="text-muted-foreground">
            Get accurate salary estimates based on your profile and job details
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Card glass>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-indigo-500" />
                  Enter Job Details
                </CardTitle>
                <CardDescription>
                  Fill in the information below to get your salary prediction
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <Input
                    label="Job Title"
                    placeholder="e.g., Software Engineer"
                    value={formData.job_title}
                    onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                    required
                  />
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Experience Level</label>
                      <select
                        className="w-full px-4 py-3 rounded-xl border border-input bg-background"
                        value={formData.experience_level}
                        onChange={(e) => setFormData({ ...formData, experience_level: e.target.value })}
                      >
                        <option value="ENTRY_LEVEL">Entry Level</option>
                        <option value="JUNIOR">Junior</option>
                        <option value="MID_LEVEL">Mid Level</option>
                        <option value="SENIOR">Senior</option>
                        <option value="EXECUTIVE">Executive</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Employment Type</label>
                      <select
                        className="w-full px-4 py-3 rounded-xl border border-input bg-background"
                        value={formData.employment_type}
                        onChange={(e) => setFormData({ ...formData, employment_type: e.target.value })}
                      >
                        <option value="FULL_TIME">Full Time</option>
                        <option value="PART_TIME">Part Time</option>
                        <option value="CONTRACT">Contract</option>
                        <option value="FREELANCE">Freelance</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      label="Work Year"
                      type="number"
                      value={formData.work_year}
                      onChange={(e) => setFormData({ ...formData, work_year: parseInt(e.target.value) })}
                      required
                    />
                    <div>
                      <label className="block text-sm font-medium mb-2">Remote Ratio (%)</label>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={formData.remote_ratio}
                        onChange={(e) => setFormData({ ...formData, remote_ratio: parseInt(e.target.value) })}
                        className="w-full"
                      />
                      <div className="text-center text-sm text-muted-foreground mt-1">
                        {formData.remote_ratio}%
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      label="Employee Residence (Country Code)"
                      placeholder="US"
                      value={formData.employee_residence}
                      onChange={(e) => setFormData({ ...formData, employee_residence: e.target.value.toUpperCase() })}
                      maxLength={2}
                      required
                    />
                    <Input
                      label="Company Location (Country Code)"
                      placeholder="US"
                      value={formData.company_location}
                      onChange={(e) => setFormData({ ...formData, company_location: e.target.value.toUpperCase() })}
                      maxLength={2}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Company Size</label>
                    <select
                      className="w-full px-4 py-3 rounded-xl border border-input bg-background"
                      value={formData.company_size}
                      onChange={(e) => setFormData({ ...formData, company_size: e.target.value })}
                    >
                      <option value="STARTUP">Startup</option>
                      <option value="SMALL">Small</option>
                      <option value="MEDIUM">Medium</option>
                      <option value="LARGE">Large</option>
                      <option value="ENTERPRISE">Enterprise</option>
                    </select>
                  </div>
                  <Button type="submit" className="w-full" isLoading={isLoading}>
                    Predict Salary
                  </Button>
                </form>
              </CardContent>
            </Card>
          </motion.div>

          {/* Result */}
          <AnimatePresence>
            {prediction && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9, x: 20 }}
                animate={{ opacity: 1, scale: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              >
                <Card glass className="h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-purple-500" />
                      Prediction Result
                    </CardTitle>
                    <CardDescription>Your estimated salary range</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-8">
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: "spring" }}
                        className="text-6xl font-bold text-gradient mb-4"
                      >
                        ${prediction.predicted_salary_usd.toLocaleString()}
                      </motion.div>
                      <div className="text-muted-foreground mb-6">
                        Predicted Annual Salary (USD)
                      </div>
                      <div className="bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-xl p-6 mb-6">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm text-muted-foreground">Minimum</span>
                          <span className="text-sm text-muted-foreground">Maximum</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-2xl font-bold">${prediction.salary_range_min.toLocaleString()}</span>
                          <span className="text-2xl font-bold">${prediction.salary_range_max.toLocaleString()}</span>
                        </div>
                      </div>
                      <div className="flex items-center justify-center gap-2 mb-4">
                        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${prediction.confidence_score * 100}%` }}
                            transition={{ delay: 0.4, duration: 0.8 }}
                            className="bg-gradient-to-r from-teal-500 to-cyan-500 h-3 rounded-full"
                          />
                        </div>
                        <span className="text-sm font-medium">
                          {Math.round(prediction.confidence_score * 100)}% confidence
                        </span>
                      </div>
                      <Button variant="accent" className="w-full">
                        Save Prediction
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

