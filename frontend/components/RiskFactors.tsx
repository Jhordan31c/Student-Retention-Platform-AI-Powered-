'use client';

import { motion } from 'framer-motion';
import { AlertTriangle, Brain, Search, CheckCircle } from '@/components/icons';

interface RiskFactorsProps {
  insights: string[];
}

export function RiskFactors({ insights }: RiskFactorsProps) {
  const getCategoryStyle = (text: string) => {
    const lower = text.toLowerCase();
    if (lower.includes('financiero') || lower.includes('deuda') || lower.includes('matrícula') || lower.includes('beca')) {
      return { color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', icon: '💰' };
    }
    if (lower.includes('rendimiento') || lower.includes('nota') || lower.includes('aprob') || lower.includes('académico')) {
      return { color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/20', icon: '📚' };
    }
    return { color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20', icon: '⚠️' };
  };

  return (
    <div className="bg-zinc-900/50 border border-white/10 rounded-2xl p-6">
      <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2">
        <Search className="w-4 h-4" /> Hallazgos Críticos
      </h3>
      <div className="space-y-3">
        {insights.map((insight, i) => {
          const style = getCategoryStyle(insight);
          return (
            <motion.div 
              key={i} 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`flex items-start gap-4 text-sm p-4 rounded-xl border ${style.bg} ${style.border}`}
            >
              <div className="text-xl">{style.icon}</div>
              <div className='flex flex-col'>
                <span className={`font-bold text-xs uppercase mb-1 ${style.color}`}>Factor Detectado</span>
                <p className="text-gray-200 leading-relaxed">{insight}</p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
