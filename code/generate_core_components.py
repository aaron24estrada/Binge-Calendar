#!/usr/bin/env python3
"""
Generate core application components for Binge Calendar
"""

import os
from pathlib import Path

def create_supabase_client():
    """Create Supabase client configuration"""
    content = """// lib/supabase.ts
import { createClientComponentClient, createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { Database } from '@/types/database'

export const createClientSupabase = () => createClientComponentClient<Database>()

export const createServerSupabase = () => createServerComponentClient<Database>({ cookies })

export const supabase = createClientSupabase()
"""
    return content

def create_database_types():
    """Create TypeScript types for database"""
    content = """// types/database.ts
export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string
          username: string | null
          full_name: string | null
          avatar_url: string | null
          timezone: string
          preferences: any
          subscription_tier: 'free' | 'pro'
          subscription_id: string | null
          trial_end: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          username?: string | null
          full_name?: string | null
          avatar_url?: string | null
          timezone?: string
          preferences?: any
          subscription_tier?: 'free' | 'pro'
          subscription_id?: string | null
          trial_end?: string | null
        }
        Update: {
          username?: string | null
          full_name?: string | null
          avatar_url?: string | null
          timezone?: string
          preferences?: any
          subscription_tier?: 'free' | 'pro'
          subscription_id?: string | null
          trial_end?: string | null
        }
      }
      events: {
        Row: {
          id: string
          title: string
          description: string | null
          category_id: string | null
          event_type: 'tv_show' | 'movie' | 'sports' | 'special'
          season_number: number | null
          episode_number: number | null
          series_name: string | null
          release_type: string | null
          sport_type: string | null
          teams: any | null
          league: string | null
          start_datetime: string
          end_datetime: string | null
          timezone: string
          platforms: any
          external_ids: any
          poster_url: string | null
          trailer_url: string | null
          rating: string | null
          status: 'confirmed' | 'tentative' | 'cancelled'
          created_at: string
          updated_at: string
        }
      }
      user_calendar_events: {
        Row: {
          id: string
          user_id: string
          event_id: string
          custom_title: string | null
          custom_notes: string | null
          reminder_settings: any
          watch_status: 'planning' | 'watching' | 'completed' | 'dropped'
          user_rating: number | null
          is_favorite: boolean
          notify_before_minutes: number[]
          notifications_enabled: boolean
          added_at: string
          updated_at: string
        }
      }
      event_categories: {
        Row: {
          id: string
          name: string
          slug: string
          color: string
          icon: string | null
          created_at: string
        }
      }
    }
  }
}

export type Event = Database['public']['Tables']['events']['Row']
export type UserCalendarEvent = Database['public']['Tables']['user_calendar_events']['Row']
export type Profile = Database['public']['Tables']['profiles']['Row']
export type EventCategory = Database['public']['Tables']['event_categories']['Row']
"""
    return content

def create_auth_component():
    """Create authentication component"""
    content = """// components/auth/AuthForm.tsx
'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'

export default function AuthForm() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: `${location.origin}/auth/callback`
        }
      })

      if (error) throw error
      setMessage('Check your email for the magic link!')
    } catch (error: any) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6">Welcome to Binge Calendar</h2>
      
      <form onSubmit={handleAuth} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address
          </label>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            disabled={loading}
          />
        </div>
        
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Sending Magic Link...' : 'Send Magic Link'}
        </Button>
      </form>
      
      {message && (
        <p className={`mt-4 text-sm text-center ${
          message.includes('Check your email') ? 'text-green-600' : 'text-red-600'
        }`}>
          {message}
        </p>
      )}
    </div>
  )
}
"""
    return content

def create_calendar_component():
    """Create main calendar component"""
    content = """// components/calendar/CalendarView.tsx
'use client'

import { useState, useEffect } from 'react'
import { Calendar, dateFnsLocalizer, Views } from 'react-big-calendar'
import { format, parse, startOfWeek, getDay } from 'date-fns'
import { enUS } from 'date-fns/locale'
import { supabase } from '@/lib/supabase'
import { Event, UserCalendarEvent } from '@/types/database'
import EventModal from './EventModal'
import 'react-big-calendar/lib/css/react-big-calendar.css'

const locales = { 'en-US': enUS }
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
})

interface CalendarEvent extends Event {
  userEvent?: UserCalendarEvent
}

export default function CalendarView({ userId }: { userId: string }) {
  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null)
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState<string>(Views.MONTH)

  useEffect(() => {
    fetchUserEvents()
  }, [userId])

  const fetchUserEvents = async () => {
    try {
      const { data, error } = await supabase
        .from('user_calendar_events')
        .select(`
          *,
          events (*)
        `)
        .eq('user_id', userId)

      if (error) throw error

      const calendarEvents = data?.map(userEvent => ({
        ...userEvent.events,
        userEvent: {
          id: userEvent.id,
          user_id: userEvent.user_id,
          event_id: userEvent.event_id,
          custom_title: userEvent.custom_title,
          custom_notes: userEvent.custom_notes,
          reminder_settings: userEvent.reminder_settings,
          watch_status: userEvent.watch_status,
          user_rating: userEvent.user_rating,
          is_favorite: userEvent.is_favorite,
          notify_before_minutes: userEvent.notify_before_minutes,
          notifications_enabled: userEvent.notifications_enabled,
          added_at: userEvent.added_at,
          updated_at: userEvent.updated_at
        }
      })) || []

      setEvents(calendarEvents)
    } catch (error) {
      console.error('Error fetching events:', error)
    } finally {
      setLoading(false)
    }
  }

  const eventStyleGetter = (event: CalendarEvent) => {
    let backgroundColor = '#6366f1'
    
    if (event.event_type === 'movie') backgroundColor = '#ef4444'
    if (event.event_type === 'sports') backgroundColor = '#22c55e'
    if (event.event_type === 'special') backgroundColor = '#f59e0b'
    
    if (event.userEvent?.watch_status === 'completed') {
      backgroundColor = '#6b7280'
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '4px',
        opacity: 0.8,
        color: 'white',
        border: '0px',
        display: 'block'
      }
    }
  }

  const calendarEvents = events.map(event => ({
    ...event,
    title: event.userEvent?.custom_title || event.title,
    start: new Date(event.start_datetime),
    end: event.end_datetime ? new Date(event.end_datetime) : new Date(event.start_datetime),
  }))

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-lg">Loading your calendar...</div>
      </div>
    )
  }

  return (
    <div className="h-full">
      <Calendar
        localizer={localizer}
        events={calendarEvents}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 600 }}
        view={view as any}
        onView={(newView) => setView(newView)}
        eventPropGetter={eventStyleGetter}
        onSelectEvent={(event) => setSelectedEvent(event as CalendarEvent)}
        popup
        tooltipAccessor={(event) => `${event.title} - ${event.event_type}`}
        defaultDate={new Date()}
      />
      
      {selectedEvent && (
        <EventModal
          event={selectedEvent}
          onClose={() => setSelectedEvent(null)}
          onUpdate={fetchUserEvents}
        />
      )}
    </div>
  )
}
"""
    return content

def create_stripe_api():
    """Create Stripe API routes"""
    content = """// app/api/stripe/create-checkout/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createServerSupabase } from '@/lib/supabase'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16'
})

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase()
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { priceId } = await request.json()

    // Get or create Stripe customer
    const { data: profile } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single()

    let customerId = profile?.subscription_id

    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        metadata: {
          supabase_user_id: user.id
        }
      })
      customerId = customer.id

      await supabase
        .from('profiles')
        .update({ subscription_id: customerId })
        .eq('id', user.id)
    }

    // Create checkout session
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'subscription',
      success_url: `${request.nextUrl.origin}/dashboard?success=true`,
      cancel_url: `${request.nextUrl.origin}/pricing?canceled=true`,
      metadata: {
        user_id: user.id
      }
    })

    return NextResponse.json({ url: session.url })
  } catch (error: any) {
    console.error('Stripe checkout error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
"""
    return content

def create_event_api():
    """Create event API routes"""
    content = """// app/api/events/add-to-calendar/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createServerSupabase } from '@/lib/supabase'

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase()
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { eventId, reminderSettings } = await request.json()

    // Check if event is already in user's calendar
    const { data: existing } = await supabase
      .from('user_calendar_events')
      .select('id')
      .eq('user_id', user.id)
      .eq('event_id', eventId)
      .single()

    if (existing) {
      return NextResponse.json({ error: 'Event already in calendar' }, { status: 400 })
    }

    // Add event to user's calendar
    const { data, error } = await supabase
      .from('user_calendar_events')
      .insert({
        user_id: user.id,
        event_id: eventId,
        reminder_settings: reminderSettings || {},
        watch_status: 'planning'
      })
      .select()
      .single()

    if (error) throw error

    return NextResponse.json({ success: true, data })
  } catch (error: any) {
    console.error('Add to calendar error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
"""
    return content

def create_ui_components():
    """Create basic UI components"""
    button_content = """// components/ui/Button.tsx
import React from 'react'
import { clsx } from 'clsx'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}) => {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        {
          'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-500': variant === 'primary',
          'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500': variant === 'secondary',
          'border border-gray-300 bg-transparent hover:bg-gray-50 focus-visible:ring-gray-500': variant === 'outline',
          'px-2.5 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-sm': size === 'md',
          'px-6 py-3 text-base': size === 'lg',
        },
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
"""
    
    input_content = """// components/ui/Input.tsx
import React from 'react'
import { clsx } from 'clsx'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <input
        className={clsx(
          'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
          'placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
          'disabled:bg-gray-50 disabled:text-gray-500',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
"""
    
    return button_content, input_content

def create_main_layout():
    """Create main layout component"""
    content = """// app/layout.tsx
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Binge Calendar - Never Miss Your Shows',
  description: 'Track TV shows, movies, and sports events in one smart calendar',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
      </body>
    </html>
  )
}
"""
    return content

def create_dashboard_page():
    """Create dashboard page"""
    content = """// app/(dashboard)/dashboard/page.tsx
import { createServerSupabase } from '@/lib/supabase'
import { redirect } from 'next/navigation'
import CalendarView from '@/components/calendar/CalendarView'

export default async function DashboardPage() {
  const supabase = createServerSupabase()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/auth')
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Your Binge Calendar</h1>
        <p className="text-gray-600 mt-2">Track your favorite shows, movies, and sports events</p>
      </header>
      
      <CalendarView userId={user.id} />
    </div>
  )
}
"""
    return content

def create_tailwind_config():
    """Create Tailwind CSS configuration"""
    content = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f4ff',
          100: '#e5edff',
          200: '#d0dcff',
          300: '#aab9ff',
          400: '#8994ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
"""
    return content

def main():
    """Generate all core components"""
    base_path = Path("/workspace/code/binge_calendar")
    
    print("🔧 Generating core application components...")
    
    # Create lib files
    lib_path = base_path / "src/lib"
    (lib_path / "supabase.ts").write_text(create_supabase_client())
    
    # Create type definitions
    types_path = base_path / "src/types"
    (types_path / "database.ts").write_text(create_database_types())
    
    # Create components
    auth_path = base_path / "src/components/auth"
    (auth_path / "AuthForm.tsx").write_text(create_auth_component())
    
    calendar_path = base_path / "src/components/calendar"
    (calendar_path / "CalendarView.tsx").write_text(create_calendar_component())
    
    # Create UI components
    ui_path = base_path / "src/components/ui"
    button_content, input_content = create_ui_components()
    (ui_path / "Button.tsx").write_text(button_content)
    (ui_path / "Input.tsx").write_text(input_content)
    
    # Create API routes
    stripe_api_path = base_path / "src/app/api/stripe/create-checkout"
    stripe_api_path.mkdir(parents=True, exist_ok=True)
    (stripe_api_path / "route.ts").write_text(create_stripe_api())
    
    events_api_path = base_path / "src/app/api/events/add-to-calendar"
    events_api_path.mkdir(parents=True, exist_ok=True)
    (events_api_path / "route.ts").write_text(create_event_api())
    
    # Create layout and pages
    (base_path / "src/app/layout.tsx").write_text(create_main_layout())
    
    dashboard_path = base_path / "src/app/(dashboard)/dashboard"
    dashboard_path.mkdir(parents=True, exist_ok=True)
    (dashboard_path / "page.tsx").write_text(create_dashboard_page())
    
    # Create configuration files
    (base_path / "tailwind.config.js").write_text(create_tailwind_config())
    
    # Create global CSS
    globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

.rbc-calendar {
  font-family: inherit;
}

.rbc-header {
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  color: #374151;
  font-weight: 600;
}

.rbc-event {
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 12px;
}

.rbc-today {
  background-color: #fef3c7;
}
"""
    
    styles_path = base_path / "src/app"
    (styles_path / "globals.css").write_text(globals_css)
    
    print("✅ Core components generated successfully!")
    print("📁 Check /workspace/code/binge_calendar/src/ for all components")

if __name__ == "__main__":
    main()
