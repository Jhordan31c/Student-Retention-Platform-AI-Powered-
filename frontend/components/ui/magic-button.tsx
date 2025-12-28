'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface MagicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  isLoading?: boolean;
  loadingText?: string;
  gradientFrom?: string; // Hex color or Tailwind color
  gradientTo?: string;   // Hex color or Tailwind color
}

export function MagicButton({ 
  children, 
  className, 
  isLoading, 
  loadingText = "Cargando...", 
  gradientFrom = "#E2CBFF", 
  gradientTo = "#393BB2",
  disabled,
  ...props 
}: MagicButtonProps) {
  
  // Construimos el gradiente cónico dinámicamente basado en los props
  const gradientStyle = {
    backgroundImage: `conic-gradient(from 90deg at 50% 50%, ${gradientFrom} 0%, ${gradientTo} 50%, ${gradientFrom} 100%)`
  };

  return (
    <button
      className={cn(
        "relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50 transition-all hover:scale-[1.02] active:scale-[0.98]",
        className,
        (isLoading || disabled) && "opacity-80 cursor-not-allowed"
      )}
      disabled={isLoading || disabled}
      {...props}
    >
      <span 
        className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite]" 
        style={gradientStyle}
      />
      <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-6 py-1 text-sm font-medium text-white backdrop-blur-3xl gap-2">
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {loadingText}
          </>
        ) : (
          children
        )}
      </span>
    </button>
  );
}
