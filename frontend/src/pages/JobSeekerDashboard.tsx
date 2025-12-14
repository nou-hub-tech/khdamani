import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { TrendingUp, MapPin, Briefcase, DollarSign, Sparkles, Globe } from 'lucide-react';

export const JobSeekerDashboard: React.FC = () => {
  const recommendedJobs = [
    {
      id: 1,
      title: "Senior Software Engineer",
      company: "Tech Corp",
      location: "New York, NY",
      salary: "$120k - $150k",
      matchScore: 0.95,
      skills: ["Python", "FastAPI", "PostgreSQL"],
    },
    {
      id: 2,
      title: "Full Stack Developer",
      company: "StartupXYZ",
      location: "San Francisco, CA",
      salary: "$100k - $130k",
      matchScore: 0.88,
      skills: ["React", "Node.js", "TypeScript"],
    },
  ];

  const countries = [
    { name: "United States", score: 0.95, opportunities: 15000, avgSalary: "$125k" },
    { name: "United Kingdom", score: 0.88, opportunities: 8500, avgSalary: "$95k" },
    { name: "Canada", score: 0.82, opportunities: 6000, avgSalary: "$105k" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/30 to-purple-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 p-4 md:p-8">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold font-display mb-2">
            Welcome back, <span className="text-gradient">Alex</span> 👋
          </h1>
          <p className="text-muted-foreground">
            Here are your personalized job recommendations and insights
          </p>
        </motion.div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Briefcase, label: "Applied Jobs", value: "12", color: "from-indigo-500 to-purple-500" },
            { icon: Sparkles, label: "Recommendations", value: "24", color: "from-purple-500 to-pink-500" },
            { icon: DollarSign, label: "Avg. Salary", value: "$125k", color: "from-teal-500 to-cyan-500" },
            { icon: Globe, label: "Countries", value: "5", color: "from-blue-500 to-indigo-500" },
          ].map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <Card glass hover>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center mb-4`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div className="text-2xl font-bold mb-1">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </Card>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Job Recommendations */}
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold font-display flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-purple-500" />
                  Recommended Jobs
                </h2>
                <Button variant="ghost" size="sm">View All</Button>
              </div>
              <div className="space-y-4">
                {recommendedJobs.map((job, i) => (
                  <motion.div
                    key={job.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.1 }}
                  >
                    <Card hover glass>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="text-xl font-semibold">{job.title}</h3>
                            <span className="px-3 py-1 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-medium">
                              {Math.round(job.matchScore * 100)}% Match
                            </span>
                          </div>
                          <p className="text-muted-foreground mb-3">{job.company} • {job.location}</p>
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
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <DollarSign className="w-4 h-4" />
                              {job.salary}
                            </span>
                            <span className="flex items-center gap-1">
                              <MapPin className="w-4 h-4" />
                              Remote
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2 mt-4">
                        <Button size="sm" className="flex-1">Apply Now</Button>
                        <Button size="sm" variant="outline">Save</Button>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Salary Prediction */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Card glass>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-teal-500" />
                    Salary Prediction
                  </CardTitle>
                  <CardDescription>Based on your profile</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-6">
                    <div className="text-4xl font-bold text-gradient mb-2">$125,000</div>
                    <div className="text-sm text-muted-foreground mb-4">
                      Estimated annual salary
                    </div>
                    <div className="text-xs text-muted-foreground mb-4">
                      Range: $100k - $150k
                    </div>
                    <Button variant="accent" size="sm" className="w-full">
                      Get Detailed Prediction
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Country Recommendations */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              <Card glass>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="w-5 h-5 text-blue-500" />
                    Top Countries
                  </CardTitle>
                  <CardDescription>Best opportunities for you</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {countries.map((country, i) => (
                      <motion.div
                        key={country.name}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 + i * 0.1 }}
                        className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50"
                      >
                        <div>
                          <div className="font-semibold">{country.name}</div>
                          <div className="text-xs text-muted-foreground">
                            {country.opportunities.toLocaleString()} opportunities
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-semibold">{country.avgSalary}</div>
                          <div className="text-xs text-muted-foreground">
                            {Math.round(country.score * 100)}% match
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                  <Button variant="outline" size="sm" className="w-full mt-4">
                    View All Countries
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

