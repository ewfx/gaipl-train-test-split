
import React from 'react';
import { IncidentData } from '@/types/dashboard';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table';

interface IncidentsTableProps {
  incidents: IncidentData[];
}

const IncidentsTable: React.FC<IncidentsTableProps> = ({ incidents }) => {
  // Split incidents by status
  const openIncidents = incidents.filter(inc => inc.status === 'Open');
  const mimIncidents = incidents.filter(inc => inc.status === 'MIM');

  return (
    <div className="border rounded-md overflow-hidden shadow-sm animate-fade-in">
      <div className="bg-yellow-500 text-white font-medium py-1 px-3 text-sm">
        Incidents
      </div>
      <div className="grid grid-cols-2 gap-px bg-gray-200">
        <div className="bg-white">
          <div className="bg-gray-100 text-gray-800 font-medium py-1 px-2 text-sm">
            Open
          </div>
          <ScrollArea className="h-[200px]">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[100px]">ID</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {openIncidents.map((incident) => (
                  <TableRow key={incident.id} className="hover:bg-gray-50 transition-colors">
                    <TableCell className="text-blue-600">{incident.id}</TableCell>
                    <TableCell>{incident.status}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </ScrollArea>
        </div>
        <div className="bg-white">
          <div className="bg-gray-100 text-gray-800 font-medium py-1 px-2 text-sm">
            MIM
          </div>
          <ScrollArea className="h-[200px]">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[100px]">ID</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mimIncidents.map((incident) => (
                  <TableRow key={incident.id} className="hover:bg-gray-50 transition-colors">
                    <TableCell className="text-blue-600">{incident.id}</TableCell>
                    <TableCell>{incident.status}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </ScrollArea>
        </div>
      </div>
    </div>
  );
};

export default IncidentsTable;
