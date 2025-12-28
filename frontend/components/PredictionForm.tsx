'use client';

import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { MagicButton } from '@/components/ui/magic-button';
import { Input } from '@/components/ui/input';
import { PremiumToggle } from '@/components/ui/bouncy-toggle';
import { cn } from '@/lib/utils';

// --- Zod Schema ---
const formSchema = z.object({
  age_at_enrollment: z.coerce.number().min(17, "Edad mínima 17").max(70, "Edad máxima 70"),
  gender: z.coerce.number(),
  marital_status: z.coerce.number(),
  course: z.coerce.number().min(1, "Curso requerido"),
  curricular_units_1st_sem_grade: z.coerce.number().min(0).max(20),
  curricular_units_2nd_sem_grade: z.coerce.number().min(0).max(20),
  curricular_units_1st_sem_approved: z.coerce.number().min(0),
  curricular_units_2nd_sem_approved: z.coerce.number().min(0),
  tuition_fees_up_to_date: z.coerce.number(),
  debtor: z.coerce.number(),
  scholarship_holder: z.coerce.number(),
  previous_qualification_grade: z.coerce.number().min(0).max(200),
  admission_grade: z.coerce.number().min(0).max(200),
});

type FormData = z.infer<typeof formSchema>;

// Valores fijos para campos que no pedimos al usuario
const HIDDEN_FIELDS = {
  application_mode: 1,
  application_order: 1,
  daytime_evening_attendance: 1,
  previous_qualification: 1,
  nationality: 1,
  mothers_qualification: 1,
  fathers_qualification: 1,
  mothers_occupation: 1,
  fathers_occupation: 1,
  displaced: 0,
  educational_special_needs: 0,
  international: 0,
  curricular_units_1st_sem_credited: 0,
  curricular_units_1st_sem_enrolled: 6,
  curricular_units_1st_sem_evaluations: 6,
  curricular_units_1st_sem_without_evaluations: 0,
  curricular_units_2nd_sem_credited: 0,
  curricular_units_2nd_sem_enrolled: 6,
  curricular_units_2nd_sem_evaluations: 6,
  curricular_units_2nd_sem_without_evaluations: 0,
  unemployment_rate: 10.8,
  inflation_rate: 1.4,
  gdp: 1.74
};

interface PredictionFormProps {
  onPredict: (result: any, data: any) => void;
  onError: (message: string) => void;
  onLoading: (isLoading: boolean) => void;
  isLoading: boolean;
  API_URL: string;
}

export function PredictionForm({ onPredict, onError, onLoading, isLoading, API_URL }: PredictionFormProps) {
  const { register, handleSubmit, control, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      age_at_enrollment: 20,
      gender: 1,
      marital_status: 1,
      course: 33,
      curricular_units_1st_sem_grade: 12.5,
      curricular_units_2nd_sem_grade: 13.0,
      curricular_units_1st_sem_approved: 5,
      curricular_units_2nd_sem_approved: 5,
      tuition_fees_up_to_date: 1,
      debtor: 0,
      scholarship_holder: 0,
      previous_qualification_grade: 130.0,
      admission_grade: 125.0,
    },
  });

  const onSubmit = async (data: any) => {
    onLoading(true);
    onError("");

    const payload = { ...HIDDEN_FIELDS, ...data };

    try {
      const response = await fetch(`${API_URL}/api/v1/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en el servidor');
      }

      const result = await response.json();
      onPredict(result, payload);
    } catch (err: any) {
      onError(err.message || 'Error de conexión');
    } finally {
      onLoading(false);
    }
  };

  const inputClass = "bg-zinc-900/50 border-white/10 text-white focus:border-blue-500 focus:ring-blue-500/20 placeholder:text-gray-600";
  const labelClass = "text-xs font-medium text-gray-400 uppercase tracking-wider mb-1.5 block";
  const selectClass = "w-full h-10 px-3 rounded-md border border-white/10 bg-zinc-900/50 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 appearance-none";

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

        {/* Grupo: Datos Personales */}
        <div className="md:col-span-2 pb-2 border-b border-white/5">
          <h3 className="text-sm font-bold text-blue-400 mb-4">Datos Personales</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className={labelClass}>Edad</label>
              <Input type="number" {...register("age_at_enrollment", { valueAsNumber: true })} className={inputClass} />
              {errors.age_at_enrollment && <span className="text-red-500 text-[10px]">{errors.age_at_enrollment.message}</span>}
            </div>
            <div>
              <label className={labelClass}>Género</label>
              <select {...register("gender")} className={selectClass}>
                <option value="1">Masculino</option>
                <option value="0">Femenino</option>
              </select>
            </div>
            <div>
              <label className={labelClass}>Estado Civil</label>
              <select {...register("marital_status")} className={selectClass}>
                <option value="1">Soltero</option>
                <option value="2">Casado</option>
                <option value="4">Divorciado</option>
              </select>
            </div>
            <div>
              <label className={labelClass}>Curso</label>
              <select {...register("course")} className={selectClass}>
                <option value="33">Ing. Bioinformática</option>
                <option value="171">Animación y Diseño</option>
                <option value="8014">Servicio Social</option>
                <option value="9003">Agronomía</option>
                <option value="9070">Diseño Comunicación</option>
                <option value="9085">Veterinaria</option>
                <option value="9119">Ing. Informática</option>
                <option value="9130">Gestión</option>
                <option value="9147">Gestión (Nocturno)</option>
                <option value="9238">Servicio Social (Noc)</option>
                <option value="9254">Turismo</option>
                <option value="9500">Enfermería</option>
                <option value="9556">Higiene Oral</option>
                <option value="9670">Gestión Publicidad</option>
                <option value="9773">Periodismo</option>
                <option value="9853">Educación Básica</option>
                <option value="9991">Gestión (Noc)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Grupo: Rendimiento Académico */}
        <div className="md:col-span-2 pb-2 border-b border-white/5">
          <h3 className="text-sm font-bold text-blue-400 mb-4">Rendimiento Académico</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className=' space-y-2 border-white/10 p-3 rounded-lg col-span-2 md:col-span-4'>
              <span className={cn(labelClass, "text-gray-200")}> Primer Semestre</span>
              <div>
                <label className={labelClass}>Nota</label>
                <Input type="number" step="0.1" {...register("curricular_units_1st_sem_grade", { valueAsNumber: true })} className={inputClass} />
              </div>
              <div>
                <label className={labelClass}>Aprobadas</label>
                <Input type="number" {...register("curricular_units_1st_sem_approved", { valueAsNumber: true })} className={inputClass} />
              </div>
            </div>
            <div className='space-y-2 border-white/10 p-3 rounded-lg col-span-2 md:col-span-4'>
              <span className={cn(labelClass, "text-gray-200")}> Segundo Semestre</span>
              <div>
                <label className={labelClass}>Nota</label>
                <Input type="number" step="0.1" {...register("curricular_units_2nd_sem_grade", { valueAsNumber: true })} className={inputClass} />
              </div>
              <div>
                <label className={labelClass}>Aprobadas</label>
                <Input type="number" {...register("curricular_units_2nd_sem_approved", { valueAsNumber: true })} className={inputClass} />
              </div>
            </div>
          </div>
        </div>

        {/* Grupo: Antecedentes */}
        <div>
          <label className={labelClass}>Nota Previa</label>
          <Input type="number" step="0.1" {...register("previous_qualification_grade", { valueAsNumber: true })} className={inputClass} />
        </div>
        <div>
          <label className={labelClass}>Nota Admisión</label>
          <Input type="number" step="0.1" {...register("admission_grade", { valueAsNumber: true })} className={inputClass} />
        </div>

        {/* Grupo: Financiero (CON EL NUEVO COMPONENTE) */}
        <div className="md:col-span-2 pt-2">
          <h3 className="text-sm font-bold text-blue-400 mb-4">Situación Financiera</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

            {/* Matrícula al Día */}
            <div className="flex items-center justify-between p-2 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
              <span className="text-sm text-gray-300">Matrícula al Día</span>
              <Controller
                name="tuition_fees_up_to_date"
                control={control}
                render={({ field: { value, onChange } }) => (
                  <PremiumToggle
                    defaultChecked={value === 1}
                    onChange={(checked) => onChange(checked ? 1 : 0)}
                  />
                )}
              />
            </div>

            {/* Tiene Beca */}
            <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
              <span className="text-sm text-gray-300">Tiene Beca</span>
              <Controller
                name="scholarship_holder"
                control={control}
                render={({ field: { value, onChange } }) => (
                  <PremiumToggle
                    defaultChecked={value === 1}
                    onChange={(checked) => onChange(checked ? 1 : 0)}
                  />
                )}
              />
            </div>

            {/* Tiene Deudas */}
            <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
              <span className="text-sm text-gray-300">Tiene Deudas</span>
              <Controller
                name="debtor"
                control={control}
                render={({ field: { value, onChange } }) => (
                  <PremiumToggle
                    defaultChecked={value === 1}
                    onChange={(checked) => onChange(checked ? 1 : 0)}
                  />
                )}
              />
            </div>

          </div>
        </div>

      </div>

      <div className="flex justify-center mt-8">
        <MagicButton
          type="submit"
          isLoading={isLoading}
          loadingText="Analizando Estudiante..."
          className="w-full max-w-md"
          gradientFrom="#E2CBFF"
          gradientTo="#393BB2"
        >
          Ejecutar Predicción
        </MagicButton>
      </div>
    </form>
  );
}
