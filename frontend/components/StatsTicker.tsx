'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

const stats = [
  { label: 'Precisión del Modelo', value: '94.2%' },
  { label: 'Estudiantes Analizados', value: '1,240' },
  { label: 'Riesgos Detectados Hoy', value: '18' },
  { label: 'Tiempo Promedio Análisis', value: '0.4s' },
];

export function StatsTicker() {
  return (
    <div className="w-full bg-blue-900/10 border-b border-blue-500/10 overflow-hidden h-8 flex items-center">
      <motion.div 
        className="flex gap-12 whitespace-nowrap px-4"
        animate={{ x: [0, -400] }}
        transition={{ 
          repeat: Infinity, 
          ease: "linear", 
          duration: 20 
        }}
      >
        {[...stats, ...stats, ...stats].map((stat, i) => (
          <div key={i} className="flex items-center gap-2 text-[10px] uppercase tracking-wider font-medium text-blue-200/60">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500/50" />
            {stat.label}: <span className="text-blue-100 font-bold">{stat.value}</span>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
