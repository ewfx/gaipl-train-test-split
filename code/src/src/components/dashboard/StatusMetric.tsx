
import React from 'react';
import { cn } from '@/lib/utils';
import { MetricData } from '@/types/dashboard';

interface StatusMetricProps {
  metric: MetricData;
  className?: string;
}

const StatusMetric: React.FC<StatusMetricProps> = ({ metric, className }) => {
  return (
    <div 
      className={cn(
        'status-card flex flex-col items-center w-full animate-fade-in',
        className
      )}
    >
      <div className="text-xs font-medium text-gray-600 mb-1 text-center">
        {metric.label}
      </div>
      <div 
        className={cn(
          'metric-card w-full h-12 text-white font-bold text-xl flex items-center justify-center',
          metric.color
        )}
      >
        {metric.value}
      </div>
    </div>
  );
};

export default StatusMetric;
