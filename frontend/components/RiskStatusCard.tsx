'use client';

import { motion } from 'framer-motion';

interface RiskStatusCardProps {
  prediction: string;
  riskLevel: string;
  riskColor: string;
}

export function RiskStatusCard({ prediction, riskLevel, riskColor }: RiskStatusCardProps) {
  const isSafe = riskColor === 'green';

  return (
    <motion.div 
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="bg-zinc-900/80 border border-white/10 rounded-2xl p-6 backdrop-blur-sm shadow-xl relative overflow-hidden"
    >
      {isSafe && (
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 left-1/4 w-2 h-2 bg-yellow-500 rounded-full animate-ping" />
          <div className="absolute top-10 right-1/4 w-2 h-2 bg-blue-500 rounded-full animate-ping delay-75" />
          <div className="absolute bottom-10 left-10 w-2 h-2 bg-green-500 rounded-full animate-ping delay-150" />
        </div>
      )}
      
      <p className="text-xs text-gray-500 uppercase tracking-widest font-bold">Estado Académico</p>
      <h2 className={`text-4xl font-extrabold mt-2 ${
        prediction === 'Dropout' ? 'text-red-400' :
        prediction === 'Enrolled' ? 'text-orange-400' : 'text-green-400'
      }`}>
        {prediction}
      </h2>
      <div className="mt-6 flex items-center gap-2">
        <span className={`px-3 py-1 rounded-full text-[10px] font-bold border ${
          riskColor === 'red' ? 'bg-red-500/10 border-red-500/20 text-red-400' : 
          riskColor === 'orange' ? 'bg-orange-500/10 border-orange-500/20 text-orange-400' : 
          'bg-green-500/10 border-green-500/20 text-green-400'
        }`}>
          RIESGO {riskLevel}
        </span>
      </div>
    </motion.div>
  );
}
