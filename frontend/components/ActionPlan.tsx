'use client';

import { motion } from 'framer-motion';
import { CheckCircle, Brain, Copy } from '@/components/icons';

interface ActionPlanProps {
  studentName?: string; // Podríamos pedir nombre en el form futuro
  riskFactors: string[];
  onClose: () => void;
  onApprove: () => void;
}

export function ActionPlan({ riskFactors, onClose, onApprove }: ActionPlanProps) {
  // Simulamos la lógica de la IA basada en los factores de riesgo
  const generateStrategies = () => {
    const strategies = [
      { week: 1, action: "Sesión de diagnóstico inicial con consejería." }
    ];

    if (riskFactors.some(f => f.toLowerCase().includes('financiero') || f.toLowerCase().includes('deuda'))) {
      strategies.push({ week: 1, action: "Solicitar revisión de estado de cuenta y aplicar a refinanciamiento." });
      strategies.push({ week: 2, action: "Taller de gestión financiera estudiantil." });
    }
    
    if (riskFactors.some(f => f.toLowerCase().includes('nota') || f.toLowerCase().includes('académico'))) {
      strategies.push({ week: 1, action: "Inscripción obligatoria en programa de tutorías pares." });
      strategies.push({ week: 3, action: "Revisión de técnicas de estudio con psicopedagogo." });
    }

    strategies.push({ week: 4, action: "Evaluación de progreso mensual." });
    return strategies;
  };

  const strategies = generateStrategies();

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="bg-gradient-to-b from-[#fafaf9] to-[#fff1f2] text-slate-800 rounded-2xl p-8 max-w-2xl mx-auto shadow-[0_20px_50px_rgba(0,0,0,0.1)] border border-white/50 relative overflow-hidden"
    >
      {/* Decoración de fondo sutil */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-rose-100/30 rounded-full blur-3xl -z-10 transform translate-x-1/2 -translate-y-1/2" />

      {/* Header Documento */}
      <div className="border-b border-stone-200/60 pb-6 mb-8 flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold font-serif text-slate-900 tracking-tight">Plan de Éxito</h2>
          <p className="text-xs text-stone-500 font-medium uppercase tracking-widest mt-2 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-rose-400"></span>
            Generado por AI Assistant
          </p>
        </div>
        <div className="p-3 bg-white rounded-2xl shadow-sm border border-stone-100">
          <Brain className="w-8 h-8 text-rose-400/80" />
        </div>
      </div>

      {/* Cuerpo */}
      <div className="space-y-8 font-sans">
        {/* Sección Diagnóstico - Estilo "ATS Score" de la referencia */}
        <div className="bg-rose-500/5 p-6 rounded-2xl border border-rose-100/50">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-8 h-8 rounded-full bg-rose-100 flex items-center justify-center">
              <span className="text-rose-600 text-lg">!</span>
            </div>
            <h3 className="font-bold text-slate-800 text-base">Diagnóstico de Riesgo</h3>
          </div>
          <p className="text-slate-600 text-sm leading-relaxed pl-11">
            Se ha detectado un perfil de riesgo basado en <span className="font-semibold text-slate-800">{riskFactors.length} factores críticos</span>. 
            El sistema recomienda una intervención inmediata enfocada en la estabilidad 
            {riskFactors.some(r => r.includes('Financiero')) ? ' financiera y académica' : ' académica'}.
          </p>
        </div>

        {/* Sección Hoja de Ruta - Estilo Lista Limpia */}
        <div>
          <h3 className="font-bold text-slate-900 text-sm uppercase tracking-wider mb-5 flex items-center gap-2">
            <span className="text-stone-300">///</span> Hoja de Ruta Sugerida
          </h3>
          <div className="space-y-3">
            {strategies.map((item, i) => (
              <div key={i} className="group flex gap-4 items-center bg-white/60 hover:bg-white p-4 rounded-xl border border-stone-100 transition-all shadow-sm hover:shadow-md">
                <div className="flex-none">
                  <span className="bg-stone-100 text-stone-600 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider group-hover:bg-slate-800 group-hover:text-white transition-colors">
                    SEM {item.week}
                  </span>
                </div>
                <div className="flex-1">
                  <p className="text-slate-700 text-sm font-medium">{item.action}</p>
                </div>
                <div className="opacity-0 group-hover:opacity-100 text-stone-300 transition-opacity">
                  <CheckCircle className="w-4 h-4" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer / Acciones */}
      <div className="mt-10 pt-6 border-t border-stone-200/60 flex justify-end gap-4 font-sans">
        <button 
          onClick={onClose}
          className="px-6 py-2.5 text-stone-500 hover:text-stone-800 hover:bg-stone-100 rounded-xl text-sm font-medium transition-colors"
        >
          Cancelar
        </button>
        <button 
          onClick={onApprove}
          className="px-8 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-sm font-bold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center gap-2"
        >
          <CheckCircle className="w-4 h-4 text-emerald-400" />
          Aprobar Plan
        </button>
      </div>
    </motion.div>
  );
}
