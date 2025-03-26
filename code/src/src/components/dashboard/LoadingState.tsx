
import React from 'react';

const LoadingState: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
      <div className="animate-pulse w-12 h-12 rounded-full bg-gray-200"></div>
      <div className="text-lg font-medium text-gray-700">Loading dashboard data...</div>
      <div className="text-sm text-gray-500">Fetching the latest metrics and statuses</div>
    </div>
  );
};

export default LoadingState;
