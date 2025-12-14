import React from 'react';
import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular';
}

export const Skeleton: React.FC<SkeletonProps> = ({ 
  className, 
  variant = 'rectangular' 
}) => {
  const baseStyles = "animate-pulse bg-muted";
  
  const variants = {
    text: "h-4 rounded",
    circular: "rounded-full",
    rectangular: "rounded-xl",
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} />
  );
};

export const SkeletonCard: React.FC = () => (
  <div className="rounded-2xl p-6 bg-card border border-border shadow-md">
    <Skeleton className="h-6 w-3/4 mb-4" variant="text" />
    <Skeleton className="h-4 w-full mb-2" variant="text" />
    <Skeleton className="h-4 w-2/3" variant="text" />
  </div>
);

