import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Binge Calendar - Never Miss Your Shows',
  description: 'Track TV shows, movies, and sports events in one smart calendar',
  keywords: ['entertainment', 'calendar', 'TV shows', 'movies', 'sports', 'tracking'],
  authors: [{ name: 'MiniMax Agent' }],
  openGraph: {
    title: 'Binge Calendar - Never Miss Your Shows',
    description: 'Track TV shows, movies, and sports events in one smart calendar',
    url: 'https://binge-calendar.vercel.app',
    siteName: 'Binge Calendar',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Binge Calendar',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Binge Calendar - Never Miss Your Shows',
    description: 'Track TV shows, movies, and sports events in one smart calendar',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
