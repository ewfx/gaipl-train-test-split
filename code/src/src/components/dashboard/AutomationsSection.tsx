
import React from 'react';
import { AutomationData } from '@/types/dashboard';
import AutomationCard from './AutomationCard';

interface AutomationsSectionProps {
  automations: AutomationData[];
}

const AutomationsSection: React.FC<AutomationsSectionProps> = ({ automations }) => {
  return (
    <div className="border rounded-md overflow-hidden shadow-sm animate-fade-in">
      <div className="bg-blue-600 text-white font-medium py-1 px-3 text-sm">
        Automations
      </div>
      <div className="bg-white p-2 grid grid-cols-1 sm:grid-cols-3 md:grid-cols-5 gap-2">
        {automations.map((automation) => (
          <AutomationCard 
            key={automation.id} 
            automation={automation} 
          />
        ))}
      </div>
    </div>
  );
};

export default AutomationsSection;
