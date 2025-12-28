'use client';

import { useState, useEffect } from 'react';
import { 
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip
} from 'recharts';
import { PredictionForm } from '@/components/PredictionForm';
import { PredictionResult, ModelMetadata } from '@/types';
import { 
  Brain, AlertTriangle, CheckCircle, History, Info, Copy, Search 
} from '@/components/icons';
import { StatsTicker } from '@/components/StatsTicker';
import { RiskFactors } from '@/components/RiskFactors';
import { ScenarioSimulator } from '@/components/ScenarioSimulator';
import { RiskStatusCard } from '@/components/RiskStatusCard';
import { InterventionBoard, InterventionCase } from '@/components/InterventionBoard';
import { ActionPlan } from '@/components/ActionPlan';
import { AnimatePresence, motion } from 'framer-motion';
import { MagicButton } from '@/components/ui/magic-button';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'predictor' | 'board'>('predictor');
  const [cases, setCases] = useState<InterventionCase[]>([]);
  const [showActionPlan, setShowActionPlan] = useState(false);

  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [currentFormData, setCurrentFormData] = useState<any>(null);
  const [modelInfo, setModelInfo] = useState<ModelMetadata | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<PredictionResult[]>([]);
  const [showModelInfo, setShowModelInfo] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${API_URL}/api/v1/health`)
      .then(res => res.json())
      .then(data => {
        setModelInfo({
          model_name: "CatBoost (Optimized)",
          trained_date: "2025-10-08",
          metrics: { accuracy: 0.7446, f1_macro: 0.6917, dropout_recall: 0.8451 }
        });
      }).catch(() => {});
  }, [API_URL]);

  const chartData = predictionResult ? [
    { name: 'Dropout', value: predictionResult.probabilities.Dropout, color: '#ef4444' },
    { name: 'Enrolled', value: predictionResult.probabilities.Enrolled, color: '#f59e0b' },
    { name: 'Graduate', value: predictionResult.probabilities.Graduate, color: '#10b981' },
  ] : [];

  const handlePredict = (result: PredictionResult, data: any) => {
    setPredictionResult(result);
    setCurrentFormData(data);
    setHistory(prev => [result, ...prev].slice(0, 5));
    // Scroll to results on mobile
    if (window.innerWidth < 1024) {
      document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSimulation = async (newData: any) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newData),
      });

      if (!response.ok) throw new Error('Error en simulación');
      
      const result = await response.json();
      setPredictionResult(result);
      setCurrentFormData(newData);
    } catch (err) {
      setError("Falló la simulación del escenario");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateIntervention = () => {
    if (!predictionResult) return;
    setShowActionPlan(true);
  };

  const confirmIntervention = () => {
    if (!predictionResult) return;
    
    const newCase: InterventionCase = {
      id: Math.random().toString(36).substr(2, 9),
      studentId: "STD-" + Math.floor(Math.random() * 10000), // Simulado
      riskLevel: predictionResult.risk_level,
      status: 'active', // Pasa directo a activo con Plan IA
      planSummary: `Plan IA: ${predictionResult.insights[0] || "Intervención general"}`,
      createdAt: new Date().toISOString()
    };

    setCases(prev => [newCase, ...prev]);
    setShowActionPlan(false);
    setActiveTab('board');
  };

  const copyToClipboard = () => {
    if (!predictionResult) return;
    const text = `
REPORTE DE PREDICCIÓN DE DESERCIÓN
-----------------------------------
Resultado: ${predictionResult.prediction}
Probabilidad de Abandono: ${(predictionResult.dropout_probability * 100).toFixed(2)}%
Nivel de Riesgo: ${predictionResult.risk_level}
Recomendación: ${predictionResult.recommendation}
Insights: ${predictionResult.insights.join(' | ')}
Fecha: ${new Date(predictionResult.timestamp).toLocaleString()}
    `.trim();
    navigator.clipboard.writeText(text);
    alert("Reporte copiado al portapapeles");
  };

  return (
    <div className="min-h-screen bg-black text-gray-200 selection:bg-blue-500/30 font-sans">
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-black to-black -z-10" />
      
      {/* HEADER WITH NAV */}
      <header className="border-b border-white/5 bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="p-2 text-blue-400">
                <Brain />
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent hidden md:block">
                Predictor de Deserción
              </h1>
            </div>

            {/* NAVIGATION TABS */}
            <nav className="flex gap-1 bg-white/5 p-1 rounded-lg">
              <button 
                onClick={() => setActiveTab('predictor')}
                className={`px-4 py-1.5 text-xs font-medium rounded-md transition-all ${
                  activeTab === 'predictor' 
                  ? 'bg-zinc-800 text-white shadow-md' 
                  : 'text-gray-400 hover:text-white'
                }`}
              >
                Predictor
              </button>
              <button 
                onClick={() => setActiveTab('board')}
                className={`px-4 py-1.5 text-xs font-medium rounded-md transition-all flex items-center gap-2 ${
                  activeTab === 'board' 
                  ? 'bg-zinc-800 text-white shadow-md' 
                  : 'text-gray-400 hover:text-white'
                }`}
              >
                Gestión de Casos
                {cases.length > 0 && (
                  <span className="bg-blue-600 text-white text-[9px] px-1.5 rounded-full">{cases.length}</span>
                )}
              </button>
            </nav>
          </div>

          <button 
            onClick={() => setShowModelInfo(!showModelInfo)}
            className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition-colors bg-white/5 px-3 py-1.5 rounded-full border border-white/10"
          >
            <Info />
            <span className="hidden sm:inline">Info del Modelo</span>
          </button>
        </div>
      </header>

      <StatsTicker />

      {/* MODEL INFO DRAWER */}
      {showModelInfo && modelInfo && (
        <div className="max-w-7xl mx-auto px-6 mt-4">
          <div className="bg-blue-500/5 border border-blue-500/20 rounded-2xl p-4 grid grid-cols-2 md:grid-cols-4 gap-4 animate-in fade-in slide-in-from-top-2 duration-300">
            <div>
              <p className="text-[10px] text-gray-500 uppercase font-bold">Algoritmo</p>
              <p className="text-sm font-medium">{modelInfo.model_name}</p>
            </div>
            <div>
              <p className="text-[10px] text-gray-500 uppercase font-bold">Accuracy</p>
              <p className="text-sm font-medium">{(modelInfo.metrics.accuracy * 100).toFixed(2)}%</p>
            </div>
            <div>
              <p className="text-[10px] text-gray-500 uppercase font-bold">Recall (Dropout)</p>
              <p className="text-sm font-medium">{(modelInfo.metrics.dropout_recall * 100).toFixed(2)}%</p>
            </div>
            <div>
              <p className="text-[10px] text-gray-500 uppercase font-bold">Entrenado</p>
              <p className="text-sm font-medium">{modelInfo.trained_date}</p>
            </div>
          </div>
        </div>
      )}

      {/* ACTION PLAN MODAL */}
      <AnimatePresence>
        {showActionPlan && predictionResult && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
            <ActionPlan 
              riskFactors={predictionResult.insights} 
              onClose={() => setShowActionPlan(false)}
              onApprove={confirmIntervention}
            />
          </div>
        )}
      </AnimatePresence>

      <main className="max-w-7xl mx-auto px-6 py-8">
        
        {/* VIEW: PREDICTOR */}
        {activeTab === 'predictor' ? (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
            {/* LEFT COLUMN: FORM */}
            <div className="lg:col-span-5 space-y-6">
              <div className="bg-zinc-950 border border-white/10 rounded-2xl overflow-hidden shadow-2xl p-6">
                <h2 className="text-lg text-center font-bold text-white mb-2 border-b border-white/5 pb-4">
                  Configuración del Estudiante
                </h2>
                <PredictionForm 
                  onPredict={handlePredict}
                  onError={setError}
                  onLoading={setLoading}
                  isLoading={loading}
                  API_URL={API_URL}
                />
              </div>

              {error && (
                <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm flex items-start gap-3 animate-in fade-in slide-in-from-top-2">
                  <AlertTriangle />
                  <div>
                    <p className="font-bold">Error en la ejecución</p>
                    <p className="opacity-80">{error}</p>
                  </div>
                </div>
              )}
            </div>

            {/* RIGHT COLUMN: RESULTS */}
            <div className="lg:col-span-7 space-y-6" id="results-section">
              {!predictionResult ? (
                <div className="h-full min-h-[400px] border border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center text-gray-600 bg-white/5">
                  <Brain />
                  <p className="mt-4 text-sm font-medium">Esperando datos del formulario...</p>
                  <p className="text-xs text-gray-500 mt-2 max-w-xs text-center">
                    Completa los campos a la izquierda y presiona "Ejecutar Predicción" para ver el análisis de riesgo.
                  </p>
                </div>
              ) : (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  {/* Status & Pie */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <RiskStatusCard 
                      prediction={predictionResult.prediction}
                      riskLevel={predictionResult.risk_level}
                      riskColor={predictionResult.risk_color}
                    />
                    <div className="bg-zinc-900/80 border border-white/10 rounded-2xl p-6 flex flex-col items-center relative backdrop-blur-sm shadow-xl">
                      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div className="text-center z-10">
                          <span className="text-2xl font-bold text-white">{(predictionResult.dropout_probability * 100).toFixed(0)}%</span>
                          <p className="text-[9px] text-gray-500 uppercase tracking-tighter">Prob. Abandono</p>
                        </div>
                      </div>
                      <div className="w-full h-[120px]">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie data={chartData} innerRadius={40} outerRadius={55} paddingAngle={5} dataKey="value" stroke="none">
                              {chartData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                            </Pie>
                            <RechartsTooltip contentStyle={{ backgroundColor: '#18181b', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }} />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>

                  {/* ACTION BUTTON FOR HIGH RISK */}
                  {(predictionResult.risk_level === 'ALTO' || predictionResult.risk_level === 'MEDIO') && (
                    <motion.div 
                      initial={{ scale: 0.9, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className="flex justify-center"
                    >
                      <MagicButton
                        onClick={handleCreateIntervention}
                        className="w-full"
                        gradientFrom="#06b6d4" // Cyan
                        gradientTo="#3b82f6"   // Blue
                      >
                        <Brain className="w-5 h-5 text-cyan-300" />
                        ⚡ Generar Plan de Intervención con IA
                      </MagicButton>
                    </motion.div>
                  )}

                  <RiskFactors insights={predictionResult.insights} />

                  {currentFormData && (
                    <ScenarioSimulator 
                      currentData={currentFormData}
                      onSimulate={handleSimulation}
                      isLoading={loading}
                    />
                  )}

                  <div className="bg-gradient-to-br from-blue-900/20 to-indigo-900/20 border border-blue-500/20 rounded-2xl p-6 relative">
                    <button 
                      onClick={copyToClipboard}
                      className="absolute top-4 right-4 p-2 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-all"
                      title="Copiar Reporte"
                    >
                      <Copy />
                    </button>
                    <h3 className="text-lg font-bold text-blue-400 mb-2 flex items-center gap-2">
                      <CheckCircle /> Recomendación
                    </h3>
                    <p className="text-gray-300 text-sm leading-relaxed pr-10">{predictionResult.recommendation}</p>
                  </div>

                  {history.length > 1 && (
                    <div className="pt-4 border-t border-white/5">
                      <p className="text-[10px] text-gray-500 uppercase font-bold mb-3 flex items-center gap-2">
                        <History /> Historial de Sesión
                      </p>
                      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                        {history.slice(1).map((item, idx) => (
                          <div key={idx} className="flex-none bg-zinc-900 border border-white/10 px-3 py-2 rounded-lg text-[10px] min-w-[120px]">
                            <div className="flex justify-between items-center mb-1">
                              <span className={item.prediction === 'Dropout' ? 'text-red-400 font-bold' : 'text-green-400 font-bold'}>{item.prediction}</span>
                            </div>
                            <span className="text-gray-500">Riesgo: {(item.dropout_probability * 100).toFixed(0)}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ) : (
          /* VIEW: BOARD */
          <div className="h-full animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="mb-6 flex justify-between items-end">
              <div>
                <h2 className="text-2xl font-bold text-white">Tablero de Gestión</h2>
                <p className="text-gray-400 text-sm">Monitoreo de casos e intervenciones activas</p>
              </div>
            </div>
            <InterventionBoard cases={cases} />
          </div>
        )}
      </main>
    </div>
  );
}