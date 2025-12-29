'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import { CheckCircle, AlertTriangle, Brain } from '@/components/icons';

export interface InterventionCase {
  id: string;
  studentId: string;
  riskLevel: string;
  status: 'pending' | 'active' | 'resolved';
  planSummary: string;
  createdAt: string;
  notes?: { date: string; content: string }[];
}

interface InterventionBoardProps {
  cases: InterventionCase[];
  onSelectCase: (c: InterventionCase) => void;
}

export function InterventionBoard({ cases, onSelectCase }: InterventionBoardProps) {
  const columns = [
    { id: 'pending', title: '🔴 Riesgo Detectado', icon: AlertTriangle },
    { id: 'active', title: '🤖 Plan IA Activado', icon: Brain },
    { id: 'resolved', title: '🟢 En Seguimiento', icon: CheckCircle },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full min-h-[500px]">
      {columns.map((col) => {
        const colCases = cases.filter(c => c.status === col.id);
        const Icon = col.icon;
        
        return (
          <div key={col.id} className="bg-zinc-900/50 border border-white/5 rounded-2xl p-4 flex flex-col">
            <div className="flex items-center gap-2 mb-4 pb-2 border-b border-white/5">
              <Icon className="w-4 h-4 text-gray-400" />
              <h3 className="text-sm font-bold text-gray-300 uppercase tracking-wider">{col.title}</h3>
              <span className="ml-auto bg-white/10 text-xs px-2 py-0.5 rounded-full text-gray-400">
                {colCases.length}
              </span>
            </div>

            <div className="space-y-3 flex-1">
              {colCases.length === 0 ? (
                <div className="h-32 border border-dashed border-white/5 rounded-xl flex items-center justify-center text-xs text-gray-600 uppercase">
                  Sin Casos
                </div>
              ) : (
                colCases.map((c) => (
                  <motion.div
                    key={c.id}
                    layoutId={c.id}
                    onClick={() => onSelectCase(c)}
                    className="bg-zinc-800 border border-white/5 p-4 rounded-xl shadow-lg hover:border-white/20 cursor-pointer transition-colors group"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs font-mono text-gray-500">#{c.studentId}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded border ${
                        c.riskLevel === 'ALTO' ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-orange-500/10 border-orange-500/20 text-orange-400'
                      }`}>
                        {c.riskLevel}
                      </span>
                    </div>
                    <p className="text-xs text-gray-300 line-clamp-2 mb-3">{c.planSummary}</p>
                    <div className="text-[10px] text-gray-600 flex justify-between items-center">
                      <span>{new Date(c.createdAt).toLocaleDateString()}</span>
                      <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center text-[8px] font-bold text-white opacity-50 group-hover:opacity-100 transition-opacity">
                        AI
                      </div>
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
