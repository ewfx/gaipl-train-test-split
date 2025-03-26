import { useQuery } from '@tanstack/react-query';
import { DashboardData } from '../types/dashboard';
import axios from 'axios';

// Simulated API response with a delay to mimic a real API call
const API_BASE = "http://localhost:8000";
const simulateApiCall = async <T>(data: T, delay = 1500): Promise<T> => {
  return new Promise((resolve) => {
    setTimeout(() => resolve(data), delay);
  });
};

// Mock data for the dashboard
const url = "https://dev305679.service-now.com/api/now/table/incident?sysparm_query=state=1^ORstate=2^ORstate=6";
const headers = { "Accept": "application/json" };
const auth = { username: "admin", password: "2jzx/UCkO2I@" };

const fetchIncidents = async () => {
  const response = await axios.get(API_BASE + '/api/proxy/incidents');
  return response.data.result.map((incident: any) => ({
    id: incident.number,
    appId: incident.app_id || 'APP ID',
    priority: incident.priority || 'P3',
    status: incident.priority === '1' ? 'MIM' : 'Open'
  }));
};


let mockDashboardData: DashboardData = {
  metrics: {
    group1: [
      { id: 'metric1', label: 'Total', value: 102, color: 'bg-status-darkgray' },
      { id: 'metric2', label: 'Success', value: 96, color: 'bg-status-green' },
      { id: 'metric3', label: 'Fail', value: 6, color: 'bg-status-red' },
    ],
    group2: [
      { id: 'metric5', label: 'Total', value: 850, color: 'bg-status-darkgray' },
      { id: 'metric6', label: 'Running', value: 179, color: 'bg-status-blue' },
      { id: 'metric7', label: 'Completed', value: 594, color: 'bg-status-green' },
      { id: 'metric8', label: 'Terminated', value: 21, color: 'bg-status-yellow' },
      { id: 'metric9', label: 'Failed', value: 56, color: 'bg-status-red' },
    ],
    group3: [
      { id: 'metric12', label: 'Active Alerts', value: 7, color: 'bg-status-orange' },
      { id: 'metric13', label: 'Active Pages', value: 2, color: 'bg-status-red' },
    ],
  },
  incidents: await fetchIncidents(),
  changes: [
    { id: 'CHG10001', title: 'Database Update', status: 'Scheduled', date: '2023-10-15' },
    { id: 'CHG10002', title: 'Network Maintenance', status: 'Scheduled', date: '2023-10-17' },
    { id: 'CHG10003', title: 'Software Deployment', status: 'Pending Approvals' },
    { id: 'CHG10004', title: 'Hardware Replacement', status: 'Pending Approvals' },
  ],
  tasks: [
    { id: 'TSK001', title: 'Server Outage', type: 'Emergency', date: '2023-10-14' },
    { id: 'TSK002', title: 'Database Backup', type: 'Expedited', date: '2023-10-15' },
    { id: 'TSK003', title: 'Security Patch', type: 'Completed Changes', date: '2023-10-12' },
    { id: 'TSK004', title: 'DNS Configuration', type: 'Completed Changes', date: '2023-10-10' },
  ],
  automations: [
    { 
      id: 'AUTO001', 
      title: 'File tracking automations', 
      description: 'Automated file tracking and reporting',
      status: 'active',
      lastRun: '2023-10-13'
    },
    { 
      id: 'AUTO002', 
      title: 'Service account password reset automation', 
      description: 'Automated password rotation for service accounts',
      status: 'active',
      lastRun: '2023-10-14'
    },
    { 
      id: 'AUTO003', 
      title: 'Cert Renewal Automations', 
      description: 'Automated certificate renewal',
      status: 'active',
      lastRun: '2023-10-12'
    },
    { 
      id: 'AUTO004', 
      title: 'Health check automation', 
      description: 'Automated system health checks',
      status: 'active',
      lastRun: '2023-10-14'
    },
    { 
      id: 'AUTO005', 
      title: 'Deployment automations', 
      description: 'Automated deployment process',
      status: 'active',
      lastRun: '2023-10-11'
    },
  ]
};

// Function to fetch dashboard data
export const fetchDashboardData = async (): Promise<DashboardData> => {
  // In a real application, this would be a fetch call to an API endpoint
  // For example: return fetch('/api/dashboard').then(res => res.json());
  return simulateApiCall(mockDashboardData, 1500);
};

// React Query hook for fetching dashboard data
export const useDashboardData = (refreshInterval = 30000) => {
  return useQuery({
    queryKey: ['dashboardData'],
    queryFn: fetchDashboardData,
    refetchInterval: refreshInterval, // Re-fetch every 30 seconds
    refetchOnWindowFocus: true,
    staleTime: refreshInterval / 2, // Consider data stale after half the refresh interval
  });
};
