
export interface MetricData {
  id: string;
  label: string;
  value: number;
  color: string;
}

export interface IncidentData {
  id: string;
  appId: string;
  priority: string;
  status: 'Open' | 'MIM';
}

export interface ChangeData {
  id: string;
  title: string;
  status: 'Scheduled' | 'Pending Approvals';
  date?: string;
}

export interface TaskData {
  id: string;
  title: string;
  type: 'Emergency' | 'Expedited' | 'Completed Changes';
  date?: string;
}

export interface AutomationData {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'inactive' | 'error';
  lastRun?: string;
}

export interface DashboardData {
  metrics: {
    group1: MetricData[];
    group2: MetricData[];
    group3: MetricData[];
  };
  incidents: IncidentData[];
  changes: ChangeData[];
  tasks: TaskData[];
  automations: AutomationData[];
}
