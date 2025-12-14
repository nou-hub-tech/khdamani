/**
 * Error Display Component
 * 
 * Reusable component for displaying API errors
 */

import React from 'react';
import { AlertCircle, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/Button';
import { getUserFriendlyError } from '@/utils/errorHandler';

interface ErrorDisplayProps {
  error: string | null;
  onDismiss?: () => void;
  className?: string;
}

export const ErrorDisplay: React.FC<ErrorDisplayProps> = ({
  error,
  onDismiss,
  className = '',
}) => {
  if (!error) return null;

  const friendlyMessage = getUserFriendlyError(error);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className={`rounded-xl bg-destructive/10 border border-destructive/20 p-4 ${className}`}
      >
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-destructive mb-1">Error</p>
            <p className="text-sm text-muted-foreground">{friendlyMessage}</p>
          </div>
          {onDismiss && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onDismiss}
              className="flex-shrink-0 h-6 w-6 p-0"
            >
              <X className="w-4 h-4" />
            </Button>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

