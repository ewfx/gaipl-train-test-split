
import React from 'react';
import { AutomationData } from '@/types/dashboard';
import { cn } from '@/lib/utils';
import { Play, PauseCircle, AlertCircle } from 'lucide-react';

interface AutomationCardProps {
  automation: AutomationData;
  className?: string;
}

const statusIcon = {
  active: <Play size={16} className="text-green-500" />,
  inactive: <PauseCircle size={16} className="text-gray-500" />,
  error: <AlertCircle size={16} className="text-red-500" />
};

const AutomationCard: React.FC<AutomationCardProps> = ({ automation, className }) => {
  return (
    <div 
      className={cn(
        "border rounded bg-white p-2 transition-all duration-200 hover:shadow-md animate-fade-in",
        className
      )}
    >
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-sm font-medium truncate">{automation.title}</h3>
        <div>{statusIcon[automation.status]}</div>
      </div>
      {automation.lastRun && (
        <div className="text-xs text-gray-500">
          Last run: {automation.lastRun}
        </div>
      )}
    </div>
  );
};

export default AutomationCard;
