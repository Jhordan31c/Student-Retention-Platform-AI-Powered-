import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './global.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Predictor de Deserción | IA Educativa',
  description: 'Sistema inteligente de predicción de deserción estudiantil',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="antialiased min-h-screen bg-[var(--background)] text-[var(--foreground)] selection:bg-[var(--primary)] selection:text-white">
        {children}
      </body>
    </html>
  );
}