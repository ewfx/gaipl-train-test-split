
import React from 'react';
import { useDashboardData } from '@/services/api';
import StatusMetricsGroup from './StatusMetricsGroup';
import IncidentsTable from './IncidentsTable';
import ChangesTable from './ChangesTable';
import TasksPanel from './TasksPanel';
import AutomationsSection from './AutomationsSection';
import LoadingState from './LoadingState';

const Dashboard: React.FC = () => {
  const { data, isLoading, error, refetch } = useDashboardData();

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="text-lg font-medium text-red-600">Error loading dashboard data</div>
        <button 
          onClick={() => refetch()} 
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!data) {
    return <div>No data available</div>;
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="bg-white border rounded-md p-4 shadow-sm">
        <h1 className="text-xl font-semibold text-gray-800">Operations Dashboard</h1>
        <p className="text-sm text-gray-500">Real-time monitoring and management</p>
      </div>

      {/* Metrics Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatusMetricsGroup title="Synthetic Monitors" metrics={data.metrics.group1} />
        <StatusMetricsGroup title="Autosys Jobs" metrics={data.metrics.group2} />
        <StatusMetricsGroup title="Big Panda Alerts" metrics={data.metrics.group3} />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 grid grid-cols-1 gap-4">
          <IncidentsTable incidents={data.incidents} />
          <ChangesTable changes={data.changes} />
        </div>
        <div>
          <TasksPanel tasks={data.tasks} />
        </div>
      </div>

      {/* Automations Section */}
      <AutomationsSection automations={data.automations} />

      {/* Last Updated */}
      <div className="text-xs text-gray-500 text-right">
        Last updated: {new Date().toLocaleString()}
        <button 
          onClick={() => refetch()} 
          className="ml-2 text-blue-600 hover:underline"
        >
          Refresh
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
