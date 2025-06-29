// app/(dashboard)/dashboard/page.tsx
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
