export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

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
          preferences: Json
          subscription_tier: 'free' | 'pro'
          subscription_status: 'active' | 'inactive' | 'canceled' | 'past_due'
          stripe_customer_id: string | null
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
          preferences?: Json
          subscription_tier?: 'free' | 'pro'
          subscription_status?: 'active' | 'inactive' | 'canceled' | 'past_due'
          stripe_customer_id?: string | null
          trial_end?: string | null
        }
        Update: {
          username?: string | null
          full_name?: string | null
          avatar_url?: string | null
          timezone?: string
          preferences?: Json
          subscription_tier?: 'free' | 'pro'
          subscription_status?: 'active' | 'inactive' | 'canceled' | 'past_due'
          stripe_customer_id?: string | null
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
          episode_title: string | null
          release_type: string | null
          director: string | null
          runtime_minutes: number | null
          sport_type: string | null
          teams: Json | null
          league: string | null
          venue: string | null
          start_datetime: string
          end_datetime: string | null
          timezone: string
          platforms: Json
          external_ids: Json
          poster_url: string | null
          backdrop_url: string | null
          trailer_url: string | null
          rating: string | null
          imdb_rating: number | null
          genres: string[] | null
          status: 'confirmed' | 'tentative' | 'cancelled' | 'postponed'
          search_vector: unknown | null
          created_at: string
          updated_at: string
        }
        Insert: {
          title: string
          description?: string | null
          category_id?: string | null
          event_type: 'tv_show' | 'movie' | 'sports' | 'special'
          season_number?: number | null
          episode_number?: number | null
          series_name?: string | null
          episode_title?: string | null
          release_type?: string | null
          director?: string | null
          runtime_minutes?: number | null
          sport_type?: string | null
          teams?: Json | null
          league?: string | null
          venue?: string | null
          start_datetime: string
          end_datetime?: string | null
          timezone?: string
          platforms?: Json
          external_ids?: Json
          poster_url?: string | null
          backdrop_url?: string | null
          trailer_url?: string | null
          rating?: string | null
          imdb_rating?: number | null
          genres?: string[] | null
          status?: 'confirmed' | 'tentative' | 'cancelled' | 'postponed'
        }
        Update: {
          title?: string
          description?: string | null
          category_id?: string | null
          event_type?: 'tv_show' | 'movie' | 'sports' | 'special'
          season_number?: number | null
          episode_number?: number | null
          series_name?: string | null
          episode_title?: string | null
          release_type?: string | null
          director?: string | null
          runtime_minutes?: number | null
          sport_type?: string | null
          teams?: Json | null
          league?: string | null
          venue?: string | null
          start_datetime?: string
          end_datetime?: string | null
          timezone?: string
          platforms?: Json
          external_ids?: Json
          poster_url?: string | null
          backdrop_url?: string | null
          trailer_url?: string | null
          rating?: string | null
          imdb_rating?: number | null
          genres?: string[] | null
          status?: 'confirmed' | 'tentative' | 'cancelled' | 'postponed'
        }
      }
      user_calendar_events: {
        Row: {
          id: string
          user_id: string
          event_id: string
          custom_title: string | null
          custom_notes: string | null
          reminder_settings: Json
          watch_status: 'planning' | 'watching' | 'completed' | 'dropped' | 'on_hold'
          user_rating: number | null
          is_favorite: boolean
          is_private: boolean
          notify_before_minutes: number[]
          notifications_enabled: boolean
          watch_progress: number
          last_watched_at: string | null
          added_at: string
          updated_at: string
        }
        Insert: {
          user_id: string
          event_id: string
          custom_title?: string | null
          custom_notes?: string | null
          reminder_settings?: Json
          watch_status?: 'planning' | 'watching' | 'completed' | 'dropped' | 'on_hold'
          user_rating?: number | null
          is_favorite?: boolean
          is_private?: boolean
          notify_before_minutes?: number[]
          notifications_enabled?: boolean
          watch_progress?: number
          last_watched_at?: string | null
        }
        Update: {
          custom_title?: string | null
          custom_notes?: string | null
          reminder_settings?: Json
          watch_status?: 'planning' | 'watching' | 'completed' | 'dropped' | 'on_hold'
          user_rating?: number | null
          is_favorite?: boolean
          is_private?: boolean
          notify_before_minutes?: number[]
          notifications_enabled?: boolean
          watch_progress?: number
          last_watched_at?: string | null
        }
      }
      event_categories: {
        Row: {
          id: string
          name: string
          slug: string
          color: string
          icon: string | null
          description: string | null
          created_at: string
        }
      }
      subscriptions: {
        Row: {
          id: string
          user_id: string
          stripe_customer_id: string
          stripe_subscription_id: string | null
          status: string
          current_period_start: string | null
          current_period_end: string | null
          cancel_at_period_end: boolean
          canceled_at: string | null
          trial_start: string | null
          trial_end: string | null
          created_at: string
          updated_at: string
        }
      }
      notifications: {
        Row: {
          id: string
          user_id: string
          event_id: string
          type: 'reminder' | 'new_episode' | 'schedule_change' | 'recommendation'
          title: string
          message: string | null
          data: Json
          sent_at: string
          read_at: string | null
          clicked_at: string | null
          delivery_method: 'in_app' | 'email' | 'push' | 'webhook'
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

// Helper types
export type Tables<T extends keyof Database['public']['Tables']> = Database['public']['Tables'][T]['Row']
export type Enums<T extends keyof Database['public']['Enums']> = Database['public']['Enums'][T]

// Specific table types
export type Profile = Tables<'profiles'>
export type Event = Tables<'events'>
export type UserCalendarEvent = Tables<'user_calendar_events'>
export type EventCategory = Tables<'event_categories'>
export type Subscription = Tables<'subscriptions'>
export type Notification = Tables<'notifications'>

// Extended types with relations
export type EventWithCategory = Event & {
  event_categories: EventCategory | null
}

export type UserEventWithEvent = UserCalendarEvent & {
  events: Event
}

export type ProfileWithSubscription = Profile & {
  subscriptions: Subscription | null
}
