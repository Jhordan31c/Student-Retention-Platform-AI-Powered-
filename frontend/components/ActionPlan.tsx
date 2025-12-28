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
      className="bg-white text-zinc-900 rounded-xl p-8 max-w-2xl mx-auto shadow-2xl relative"
    >
      {/* Header Documento */}
      <div className="border-b border-zinc-200 pb-4 mb-6 flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold font-serif text-zinc-800">Plan de Éxito Estudiantil</h2>
          <p className="text-sm text-zinc-500 uppercase tracking-widest mt-1">Generado por AI Assistant • Confidencial</p>
        </div>
        <Brain className="w-10 h-10 text-blue-600 opacity-20" />
      </div>

      {/* Cuerpo */}
      <div className="space-y-6 font-serif">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
          <h3 className="font-bold text-blue-800 text-sm uppercase mb-2">Diagnóstico Automático</h3>
          <p className="text-zinc-700 text-sm leading-relaxed">
            Se ha detectado un perfil de riesgo basado en {riskFactors.length} factores críticos. 
            El sistema recomienda una intervención inmediata enfocada en la estabilidad 
            {riskFactors.some(r => r.includes('Financiero')) ? ' financiera y académica' : ' académica'}.
          </p>
        </div>

        <div>
          <h3 className="font-bold text-zinc-900 text-sm uppercase border-b border-zinc-200 pb-2 mb-4">Hoja de Ruta Sugerida</h3>
          <div className="space-y-4">
            {strategies.map((item, i) => (
              <div key={i} className="flex gap-4 items-start">
                <div className="flex-none w-16 pt-1">
                  <span className="bg-zinc-900 text-white text-xs font-bold px-2 py-1 rounded">SEM {item.week}</span>
                </div>
                <div className="border-l-2 border-zinc-200 pl-4 py-1">
                  <p className="text-zinc-800">{item.action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer / Acciones */}
      <div className="mt-8 pt-6 border-t border-zinc-200 flex justify-end gap-3 font-sans">
        <button 
          onClick={onClose}
          className="px-4 py-2 text-zinc-500 hover:bg-zinc-100 rounded-lg text-sm font-medium transition-colors"
        >
          Cancelar
        </button>
        <button 
          onClick={onApprove}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium shadow-lg hover:shadow-blue-500/30 transition-all flex items-center gap-2"
        >
          <CheckCircle className="w-4 h-4" />
          Aprobar e Iniciar Seguimiento
        </button>
      </div>
    </motion.div>
  );
}
