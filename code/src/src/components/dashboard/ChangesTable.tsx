
import React from 'react';
import { ChangeData } from '@/types/dashboard';

interface ChangesTableProps {
  changes: ChangeData[];
}

const ChangesTable: React.FC<ChangesTableProps> = ({ changes }) => {
  // Split changes by status
  const scheduledChanges = changes.filter(change => change.status === 'Scheduled');
  const pendingChanges = changes.filter(change => change.status === 'Pending Approvals');

  return (
    <div className="border rounded-md overflow-hidden shadow-sm animate-fade-in">
      <div className="bg-yellow-500 text-white font-medium py-1 px-3 text-sm">
        Changes
      </div>
      <div className="grid grid-cols-2 gap-px bg-gray-200">
        <div className="bg-white">
          <div className="bg-gray-100 text-gray-800 font-medium py-1 px-2 text-sm">
            Scheduled
          </div>
          <table className="min-w-full">
            <tbody className="text-sm">
              {scheduledChanges.map((change) => (
                <tr key={change.id} className="border-t border-gray-200 hover:bg-gray-50 transition-colors">
                  <td className="px-2 py-1 text-blue-600">{change.title}</td>
                  <td className="px-2 py-1 text-xs text-gray-500">{change.date}</td>
                </tr>
              ))}
              {scheduledChanges.length === 0 && (
                <tr>
                  <td className="px-2 py-3 text-gray-500 text-center" colSpan={2}>No scheduled changes</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="bg-white">
          <div className="bg-gray-100 text-gray-800 font-medium py-1 px-2 text-sm">
            Pending Approvals
          </div>
          <table className="min-w-full">
            <tbody className="text-sm">
              {pendingChanges.map((change) => (
                <tr key={change.id} className="border-t border-gray-200 hover:bg-gray-50 transition-colors">
                  <td className="px-2 py-1 text-blue-600">{change.title}</td>
                  <td className="px-2 py-1 text-xs text-gray-500">{change.date}</td>
                </tr>
              ))}
              {pendingChanges.length === 0 && (
                <tr>
                  <td className="px-2 py-3 text-gray-500 text-center" colSpan={2}>No pending approvals</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ChangesTable;
