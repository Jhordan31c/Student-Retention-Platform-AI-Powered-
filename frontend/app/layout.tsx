import type { Metadata } from 'next'
export const metadata: Metadata = {
  title: 'Predictor de Deserción',
  description: 'Sistema de predicción de deserción estudiantil',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
