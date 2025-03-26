
import React from 'react';
import { TaskData } from '@/types/dashboard';

interface TasksPanelProps {
  tasks: TaskData[];
}

const TasksPanel: React.FC<TasksPanelProps> = ({ tasks }) => {
  // Group tasks by type
  const emergencyTasks = tasks.filter(task => task.type === 'Emergency');
  const expeditedTasks = tasks.filter(task => task.type === 'Expedited');
  const completedTasks = tasks.filter(task => task.type === 'Completed Changes');

  return (
    <div className="border rounded-md overflow-hidden shadow-sm animate-fade-in">
      <div className="bg-green-600 text-white font-medium py-1 px-3 text-sm">
        Tasks Assigned to you
      </div>
      <div className="bg-white p-2 space-y-2">
        <div>
          <div className="text-sm font-medium text-red-600 mb-1">Emergency</div>
          {emergencyTasks.map((task) => (
            <div key={task.id} className="text-sm pl-2 py-0.5 border-l-2 border-red-500">
              {task.title}
              {task.date && <span className="text-xs text-gray-500 ml-2">{task.date}</span>}
            </div>
          ))}
          {emergencyTasks.length === 0 && <div className="text-sm text-gray-500 pl-2">No emergency tasks</div>}
        </div>
        
        <div>
          <div className="text-sm font-medium text-orange-500 mb-1">Expedited</div>
          {expeditedTasks.map((task) => (
            <div key={task.id} className="text-sm pl-2 py-0.5 border-l-2 border-orange-400">
              {task.title}
              {task.date && <span className="text-xs text-gray-500 ml-2">{task.date}</span>}
            </div>
          ))}
          {expeditedTasks.length === 0 && <div className="text-sm text-gray-500 pl-2">No expedited tasks</div>}
        </div>
        
        <div>
          <div className="text-sm font-medium text-green-600 mb-1">Completed Changes</div>
          {completedTasks.map((task) => (
            <div key={task.id} className="text-sm pl-2 py-0.5 border-l-2 border-green-500">
              {task.title}
              {task.date && <span className="text-xs text-gray-500 ml-2">{task.date}</span>}
            </div>
          ))}
          {completedTasks.length === 0 && <div className="text-sm text-gray-500 pl-2">No completed changes</div>}
        </div>
      </div>
    </div>
  );
};

export default TasksPanel;
