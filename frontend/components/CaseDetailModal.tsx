'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import { CheckCircle, AlertTriangle, Brain, History } from '@/components/icons';
import { InterventionCase } from './InterventionBoard';

interface CaseDetailModalProps {
  caseData: InterventionCase;
  onClose: () => void;
  onUpdateStatus: (newStatus: 'pending' | 'active' | 'resolved') => void;
  onAddNote: (note: string) => void;
}

export function CaseDetailModal({ caseData, onClose, onUpdateStatus, onAddNote }: CaseDetailModalProps) {
  const [newNote, setNewNote] = useState("");

  const handleSubmitNote = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    onAddNote(newNote);
    setNewNote("");
  };

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="bg-gradient-to-b from-[#fafaf9] to-[#fff1f2] w-full max-w-3xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
    >
      {/* Header */}
      <div className="p-6 border-b border-stone-200/60 flex justify-between items-start bg-white/50 backdrop-blur-sm">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h2 className="text-2xl font-serif font-bold text-slate-900">Expediente {caseData.studentId}</h2>
            <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full border ${
              caseData.riskLevel === 'ALTO' 
                ? 'bg-rose-100 text-rose-600 border-rose-200' 
                : 'bg-amber-100 text-amber-600 border-amber-200'
            }`}>
              RIESGO {caseData.riskLevel}
            </span>
          </div>
          <p className="text-slate-500 text-sm">Fecha de apertura: {new Date(caseData.createdAt).toLocaleDateString()}</p>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 18 12"/></svg>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Columna Izquierda: Detalles */}
        <div className="md:col-span-2 space-y-6">
          {/* Plan IA */}
          <div className="bg-white/60 p-5 rounded-xl border border-stone-100 shadow-sm">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
              <Brain className="w-4 h-4 text-cyan-500" /> Estrategia Activa
            </h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              {caseData.planSummary}
            </p>
          </div>

          {/* Notas / Bitácora */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
              <History className="w-4 h-4 text-stone-400" /> Bitácora de Seguimiento
            </h3>
            
            <div className="space-y-3">
              {caseData.notes?.map((note, i) => (
                <div key={i} className="bg-white p-3 rounded-lg border border-stone-100 text-sm text-slate-700 shadow-sm">
                  <span className="text-[10px] text-stone-400 block mb-1">{note.date}</span>
                  {note.content}
                </div>
              ))}
              {(!caseData.notes || caseData.notes.length === 0) && (
                <p className="text-stone-400 text-sm italic text-center py-4">No hay notas registradas.</p>
              )}
            </div>

            <form onSubmit={handleSubmitNote} className="flex gap-2 mt-4">
              <input 
                type="text" 
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                placeholder="Agregar nota de seguimiento..." 
                className="flex-1 bg-white border border-stone-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-rose-200 text-slate-800 placeholder:text-stone-400"
              />
              <button 
                type="submit"
                className="bg-slate-900 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-slate-800 transition-colors"
              >
                Agregar
              </button>
            </form>
          </div>
        </div>

        {/* Columna Derecha: Acciones */}
        <div className="space-y-6">
          <div className="bg-rose-50 p-4 rounded-xl border border-rose-100">
            <h3 className="text-xs font-bold text-rose-800 uppercase mb-3">Estado del Caso</h3>
            <div className="space-y-2">
              <button 
                onClick={() => onUpdateStatus('pending')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                  caseData.status === 'pending' ? 'bg-white shadow-sm font-bold text-rose-600' : 'text-stone-500 hover:bg-white/50'
                }`}
              >
                <AlertTriangle className="w-4 h-4" /> Pendiente
              </button>
              <button 
                onClick={() => onUpdateStatus('active')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                  caseData.status === 'active' ? 'bg-white shadow-sm font-bold text-cyan-600' : 'text-stone-500 hover:bg-white/50'
                }`}
              >
                <Brain className="w-4 h-4" /> En Progreso
              </button>
              <button 
                onClick={() => onUpdateStatus('resolved')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                  caseData.status === 'resolved' ? 'bg-white shadow-sm font-bold text-emerald-600' : 'text-stone-500 hover:bg-white/50'
                }`}
              >
                <CheckCircle className="w-4 h-4" /> Resuelto
              </button>
            </div>
          </div>
        </div>

      </div>
    </motion.div>
  );
}
