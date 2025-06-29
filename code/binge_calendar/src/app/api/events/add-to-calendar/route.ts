// app/api/events/add-to-calendar/route.ts
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
