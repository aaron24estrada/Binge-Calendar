// components/calendar/CalendarView.tsx
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
