
import React from 'react';
import { cn } from '@/lib/utils';
import StatusMetric from './StatusMetric';
import { MetricData } from '@/types/dashboard';

interface StatusMetricsGroupProps {
  title?: string;
  metrics: MetricData[];
  className?: string;
}

const StatusMetricsGroup: React.FC<StatusMetricsGroupProps> = ({ 
  title, 
  metrics,
  className 
}) => {
  return (
    <div className={cn('flex flex-col bg-white rounded-md shadow-sm border overflow-hidden', className)}>
      {title && (
        <div className="text-sm font-semibold text-gray-800 px-3 py-2 border-b bg-gray-50">
          {title}
        </div>
      )}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-2 p-3">
        {metrics.map((metric) => (
          <StatusMetric key={metric.id} metric={metric} />
        ))}
      </div>
    </div>
  );
};

export default StatusMetricsGroup;
