'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Search } from '@/components/icons';
import { MagicButton } from '@/components/ui/magic-button';
import { PremiumToggle } from '@/components/ui/bouncy-toggle';

interface ScenarioSimulatorProps {
  currentData: any;
  onSimulate: (newData: any) => void;
  isLoading: boolean;
}

export function ScenarioSimulator({ currentData, onSimulate, isLoading }: ScenarioSimulatorProps) {
  const [fees, setFees] = useState(currentData.tuition_fees_up_to_date);
  const [scholarship, setScholarship] = useState(currentData.scholarship_holder);
  const [debt, setDebt] = useState(currentData.debtor);

  const handleSimulate = () => {
    onSimulate({
      ...currentData,
      tuition_fees_up_to_date: fees,
      scholarship_holder: scholarship,
      debtor: debt
    });
  };

  const hasChanges = 
    fees !== currentData.tuition_fees_up_to_date || 
    scholarship !== currentData.scholarship_holder || 
    debt !== currentData.debtor;

  return (
    <div className="bg-gradient-to-r from-zinc-900 to-zinc-900/50 border border-purple-500/20 rounded-2xl p-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10">
        <Brain className="w-24 h-24 text-purple-500" />
      </div>

      <h3 className="text-sm font-bold text-purple-400 uppercase tracking-wider mb-6 flex items-center gap-2">
        <Brain className="w-4 h-4" /> Simulador de Impacto
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="space-y-3">
          <span className="text-xs text-gray-400 block">Estado de Matrícula</span>
          <div className="flex items-center justify-between bg-black/20 p-3 rounded-lg border border-white/5">
            <span className={fees ? "text-green-400 font-medium" : "text-red-400 font-medium"}>
              {fees ? "Al Día" : "Atrasada"}
            </span>
            <PremiumToggle 
              defaultChecked={fees === 1} 
              onChange={(checked) => setFees(checked ? 1 : 0)} 
            />
          </div>
        </div>

        <div className="space-y-3">
          <span className="text-xs text-gray-400 block">Estado de Beca</span>
          <div className="flex items-center justify-between bg-black/20 p-3 rounded-lg border border-white/5">
            <span className={scholarship ? "text-green-400 font-medium" : "text-gray-500 font-medium"}>
              {scholarship ? "Becado" : "Sin Beca"}
            </span>
            <PremiumToggle 
              defaultChecked={scholarship === 1} 
              onChange={(checked) => setScholarship(checked ? 1 : 0)} 
            />
          </div>
        </div>

        <div className="space-y-3">
          <span className="text-xs text-gray-400 block">Deuda Financiera</span>
          <div className="flex items-center justify-between bg-black/20 p-3 rounded-lg border border-white/5">
            <span className={debt ? "text-red-400 font-medium" : "text-green-400 font-medium"}>
              {debt ? "Con Deuda" : "Sin Deuda"}
            </span>
            <PremiumToggle 
              defaultChecked={debt === 1} 
              onChange={(checked) => setDebt(checked ? 1 : 0)} 
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <MagicButton
          onClick={handleSimulate}
          disabled={!hasChanges || isLoading}
          isLoading={isLoading}
          loadingText="Simulando..."
          gradientFrom="#ec4899" // Pink
          gradientTo="#8b5cf6"   // Violet
          className={!hasChanges ? 'opacity-50 cursor-not-allowed' : ''}
        >
          Simular Nuevo Escenario
        </MagicButton>
      </div>
    </div>
  );
}
