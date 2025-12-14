import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { useNavigate } from 'react-router-dom';
import { Zap, Mail, Lock, User, Briefcase, UserCheck } from 'lucide-react';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'JOB_SEEKER',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Validation
    const newErrors: Record<string, string> = {};
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setIsLoading(false);
      return;
    }

    // TODO: Implement API call
    setTimeout(() => {
      setIsLoading(false);
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Left Side - Branding */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="hidden lg:block"
        >
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 rounded-xl gradient-primary flex items-center justify-center">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <span className="text-3xl font-bold font-display text-gradient">Khadamni</span>
            </div>
            <h1 className="text-4xl font-bold font-display">
              Start your
              <span className="text-gradient block mt-2">career journey</span>
            </h1>
            <p className="text-lg text-muted-foreground">
              Join thousands of job seekers and recruiters using AI-powered tools 
              to find the perfect match.
            </p>
          </div>
        </motion.div>

        {/* Right Side - Register Form */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full"
        >
          <Card glass className="max-w-md mx-auto">
            <CardHeader>
              <CardTitle className="text-3xl font-display">Create Account</CardTitle>
              <CardDescription>
                Choose your role and start your journey
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Role Selection */}
                <div>
                  <label className="block text-sm font-medium mb-3">I am a</label>
                  <div className="grid grid-cols-2 gap-3">
                    <motion.button
                      type="button"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setFormData({ ...formData, role: 'JOB_SEEKER' })}
                      className={`
                        p-4 rounded-xl border-2 transition-all
                        ${formData.role === 'JOB_SEEKER' 
                          ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                          : 'border-border hover:border-indigo-300'
                        }
                      `}
                    >
                      <UserCheck className={`w-6 h-6 mx-auto mb-2 ${formData.role === 'JOB_SEEKER' ? 'text-indigo-600' : 'text-muted-foreground'}`} />
                      <div className={`font-medium ${formData.role === 'JOB_SEEKER' ? 'text-indigo-600' : 'text-muted-foreground'}`}>
                        Job Seeker
                      </div>
                    </motion.button>
                    <motion.button
                      type="button"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setFormData({ ...formData, role: 'RECRUITER' })}
                      className={`
                        p-4 rounded-xl border-2 transition-all
                        ${formData.role === 'RECRUITER' 
                          ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                          : 'border-border hover:border-indigo-300'
                        }
                      `}
                    >
                      <Briefcase className={`w-6 h-6 mx-auto mb-2 ${formData.role === 'RECRUITER' ? 'text-indigo-600' : 'text-muted-foreground'}`} />
                      <div className={`font-medium ${formData.role === 'RECRUITER' ? 'text-indigo-600' : 'text-muted-foreground'}`}>
                        Recruiter
                      </div>
                    </motion.button>
                  </div>
                </div>

                <Input
                  label="Email"
                  type="email"
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  error={errors.email}
                  icon={Mail}
                />
                <Input
                  label="Password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  error={errors.password}
                  icon={Lock}
                />
                <Input
                  label="Confirm Password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  error={errors.confirmPassword}
                  icon={Lock}
                />
                <div className="flex items-center space-x-2">
                  <input type="checkbox" className="rounded border-border" />
                  <label className="text-sm text-muted-foreground">
                    I agree to the Terms of Service and Privacy Policy
                  </label>
                </div>
                <Button type="submit" className="w-full" isLoading={isLoading}>
                  Create Account
                </Button>
                <div className="text-center text-sm text-muted-foreground">
                  Already have an account?{' '}
                  <a href="/login" className="text-primary hover:underline font-medium">
                    Sign in
                  </a>
                </div>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

