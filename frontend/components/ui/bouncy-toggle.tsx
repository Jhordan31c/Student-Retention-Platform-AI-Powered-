"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"

interface PremiumToggleProps {
  defaultChecked?: boolean
  onChange?: (checked: boolean) => void
  label?: string
}

export function PremiumToggle({ defaultChecked = false, onChange, label }: PremiumToggleProps) {
  const [isChecked, setIsChecked] = useState(defaultChecked)
  const [isPressed, setIsPressed] = useState(false)

  const handleToggle = () => {
    const newValue = !isChecked
    setIsChecked(newValue)
    onChange?.(newValue)
  }

  return (
    <div className="flex items-center gap-3">
      {label && (
        <span
          className={cn(
            "text-sm font-medium transition-colors duration-300",
            isChecked ? "text-white" : "text-gray-400",
          )}
        >
          {label}
        </span>
      )}
      <button
        type="button" // IMPORTANTE: Evita que envíe el formulario
        role="switch"
        aria-checked={isChecked}
        onClick={handleToggle}
        onMouseDown={() => setIsPressed(true)}
        onMouseUp={() => setIsPressed(false)}
        onMouseLeave={() => setIsPressed(false)}
        className={cn(
          "group relative h-8 w-14 rounded-full p-1 transition-all duration-500 ease-out border border-white/10",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-black",
          isChecked ? "bg-blue-600" : "bg-zinc-800", // Colores explícitos visibles
        )}
      >
        {/* Glow effect (Solo visible cuando activo) */}
        <div
          className={cn(
            "absolute inset-0 rounded-full transition-opacity duration-500",
            isChecked ? "opacity-50 shadow-[0_0_15px_rgba(37,99,235,0.5)]" : "opacity-0",
          )}
        />

        {/* Track inner gradient */}
        <div
          className={cn(
            "absolute inset-[2px] rounded-full transition-all duration-500",
            isChecked ? "bg-gradient-to-b from-blue-500 to-blue-600" : "bg-transparent",
          )}
        />

        {/* Thumb (El círculo que se mueve) */}
        <div
          className={cn(
            "relative h-5 w-5 rounded-full shadow-lg transition-all duration-500 ease-[cubic-bezier(0.68,-0.55,0.265,1.55)]",
            "bg-white",
            isChecked ? "translate-x-6" : "translate-x-0",
            isPressed && "scale-90 duration-150",
          )}
        >
          {/* Status indicator dot inside thumb */}
          <div
            className={cn(
              "absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full transition-all duration-500",
              isChecked
                ? "h-1.5 w-1.5 bg-blue-600 opacity-100 scale-100"
                : "h-1.5 w-1.5 bg-zinc-400 opacity-100 scale-100",
            )}
          />
        </div>
      </button>
    </div>
  )
}