// types/database.ts
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
