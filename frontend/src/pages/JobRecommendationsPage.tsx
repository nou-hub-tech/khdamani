import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Sparkles, MapPin, DollarSign, Filter, Bookmark, BookmarkCheck } from 'lucide-react';

export const JobRecommendationsPage: React.FC = () => {
  const [savedJobs, setSavedJobs] = useState<Set<number>>(new Set());
  const [filters, setFilters] = useState({
    location: '',
    salaryMin: '',
    employmentType: '',
  });

  const jobs = [
    {
      id: 1,
      title: "Senior Software Engineer",
      company: "Tech Corp",
      location: "New York, NY",
      salary: { min: 120000, max: 150000 },
      matchScore: 0.95,
      skills: ["Python", "FastAPI", "PostgreSQL", "Docker"],
      employmentType: "FULL_TIME",
      posted: "2 days ago",
    },
    {
      id: 2,
      title: "Full Stack Developer",
      company: "StartupXYZ",
      location: "San Francisco, CA",
      salary: { min: 100000, max: 130000 },
      matchScore: 0.88,
      skills: ["React", "Node.js", "TypeScript", "MongoDB"],
      employmentType: "FULL_TIME",
      posted: "5 days ago",
    },
    {
      id: 3,
      title: "Backend Engineer",
      company: "CloudSoft",
      location: "Remote",
      salary: { min: 95000, max: 125000 },
      matchScore: 0.82,
      skills: ["Python", "Django", "AWS", "Kubernetes"],
      employmentType: "FULL_TIME",
      posted: "1 week ago",
    },
  ];

  const toggleSave = (jobId: number) => {
    setSavedJobs(prev => {
      const newSet = new Set(prev);
      if (newSet.has(jobId)) {
        newSet.delete(jobId);
      } else {
        newSet.add(jobId);
      }
      return newSet;
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 p-4 md:p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold font-display mb-2 flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-purple-500" />
            <span>Job <span className="text-gradient">Recommendations</span></span>
          </h1>
          <p className="text-muted-foreground">
            AI-powered job matches tailored to your profile
          </p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card glass className="mb-6">
            <div className="flex items-center gap-2 mb-4">
              <Filter className="w-5 h-5 text-indigo-500" />
              <h2 className="text-lg font-semibold">Filters</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Location"
                placeholder="City or Country"
                value={filters.location}
                onChange={(e) => setFilters({ ...filters, location: e.target.value })}
              />
              <Input
                label="Min Salary (USD)"
                type="number"
                placeholder="80000"
                value={filters.salaryMin}
                onChange={(e) => setFilters({ ...filters, salaryMin: e.target.value })}
              />
              <div>
                <label className="block text-sm font-medium mb-2">Employment Type</label>
                <select
                  className="w-full px-4 py-3 rounded-xl border border-input bg-background"
                  value={filters.employmentType}
                  onChange={(e) => setFilters({ ...filters, employmentType: e.target.value })}
                >
                  <option value="">All Types</option>
                  <option value="FULL_TIME">Full Time</option>
                  <option value="PART_TIME">Part Time</option>
                  <option value="CONTRACT">Contract</option>
                  <option value="REMOTE">Remote</option>
                </select>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Job List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {jobs.map((job, i) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.1 }}
            >
              <Card hover glass>
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-semibold">{job.title}</h3>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => toggleSave(job.id)}
                        className="text-muted-foreground hover:text-indigo-500 transition-colors"
                      >
                        {savedJobs.has(job.id) ? (
                          <BookmarkCheck className="w-5 h-5 text-indigo-500" />
                        ) : (
                          <Bookmark className="w-5 h-5" />
                        )}
                      </motion.button>
                    </div>
                    <p className="text-muted-foreground mb-3">{job.company}</p>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-4 h-4" />
                        {job.location}
                      </span>
                      <span className="flex items-center gap-1">
                        <DollarSign className="w-4 h-4" />
                        ${job.salary.min.toLocaleString()} - ${job.salary.max.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {job.skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-sm"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${job.matchScore * 100}%` }}
                        transition={{ delay: 0.3 + i * 0.1, duration: 0.8 }}
                        className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                      />
                    </div>
                    <span className="text-sm font-medium">
                      {Math.round(job.matchScore * 100)}% Match
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">View Details</Button>
                    <Button size="sm">Apply Now</Button>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-3">Posted {job.posted}</p>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

