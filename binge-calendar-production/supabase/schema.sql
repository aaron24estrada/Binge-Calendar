-- Binge Calendar Database Schema
-- Production Schema for Supabase PostgreSQL

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_cron";

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS public.notifications CASCADE;
DROP TABLE IF EXISTS public.user_calendar_events CASCADE;
DROP TABLE IF EXISTS public.subscriptions CASCADE;
DROP TABLE IF EXISTS public.events CASCADE;
DROP TABLE IF EXISTS public.event_categories CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;

-- Profiles table (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    timezone TEXT DEFAULT 'UTC',
    preferences JSONB DEFAULT '{}',
    subscription_tier TEXT DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro')),
    subscription_status TEXT DEFAULT 'inactive' CHECK (subscription_status IN ('active', 'inactive', 'canceled', 'past_due')),
    stripe_customer_id TEXT UNIQUE,
    trial_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Event categories table
CREATE TABLE public.event_categories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    color TEXT DEFAULT '#6366f1',
    icon TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Master events table (TV shows, movies, sports)
CREATE TABLE public.events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category_id UUID REFERENCES public.event_categories(id),
    event_type TEXT NOT NULL CHECK (event_type IN ('tv_show', 'movie', 'sports', 'special')),
    
    -- TV Show specific fields
    season_number INTEGER,
    episode_number INTEGER,
    series_name TEXT,
    episode_title TEXT,
    
    -- Movie specific fields
    release_type TEXT CHECK (release_type IN ('theatrical', 'streaming', 'digital', 'dvd', 'bluray')),
    director TEXT,
    runtime_minutes INTEGER,
    
    -- Sports specific fields
    sport_type TEXT,
    teams JSONB,
    league TEXT,
    venue TEXT,
    
    -- Common fields
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    end_datetime TIMESTAMP WITH TIME ZONE,
    timezone TEXT DEFAULT 'UTC',
    platforms JSONB DEFAULT '[]',
    external_ids JSONB DEFAULT '{}', -- TMDB, IMDB, ESPN IDs
    poster_url TEXT,
    backdrop_url TEXT,
    trailer_url TEXT,
    rating TEXT,
    imdb_rating DECIMAL(3,1),
    genres TEXT[],
    status TEXT DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'tentative', 'cancelled', 'postponed')),
    
    -- SEO and search
    search_vector tsvector,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User's personal calendar entries
CREATE TABLE public.user_calendar_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    event_id UUID REFERENCES public.events(id) ON DELETE CASCADE,
    
    -- User customizations
    custom_title TEXT,
    custom_notes TEXT,
    reminder_settings JSONB DEFAULT '{}',
    watch_status TEXT DEFAULT 'planning' CHECK (watch_status IN ('planning', 'watching', 'completed', 'dropped', 'on_hold')),
    user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 10),
    is_favorite BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    
    -- Notification preferences
    notify_before_minutes INTEGER[] DEFAULT '{60, 15}',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    
    -- Watch tracking
    watch_progress INTEGER DEFAULT 0, -- percentage for movies, episodes for TV
    last_watched_at TIMESTAMP WITH TIME ZONE,
    
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, event_id)
);

-- Subscriptions tracking
CREATE TABLE public.subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE UNIQUE,
    stripe_customer_id TEXT NOT NULL,
    stripe_subscription_id TEXT UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('active', 'canceled', 'incomplete', 'incomplete_expired', 'past_due', 'trialing', 'unpaid')),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMP WITH TIME ZONE,
    trial_start TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User notification history
CREATE TABLE public.notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    event_id UUID REFERENCES public.events(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('reminder', 'new_episode', 'schedule_change', 'recommendation')),
    title TEXT NOT NULL,
    message TEXT,
    data JSONB DEFAULT '{}',
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE,
    clicked_at TIMESTAMP WITH TIME ZONE,
    delivery_method TEXT DEFAULT 'in_app' CHECK (delivery_method IN ('in_app', 'email', 'push', 'webhook'))
);

-- Create indexes for performance
CREATE INDEX idx_events_start_datetime ON public.events(start_datetime);
CREATE INDEX idx_events_category_type ON public.events(category_id, event_type);
CREATE INDEX idx_events_platforms ON public.events USING GIN(platforms);
CREATE INDEX idx_events_search ON public.events USING GIN(search_vector);
CREATE INDEX idx_events_upcoming ON public.events(start_datetime) WHERE start_datetime > NOW();
CREATE INDEX idx_user_calendar_events_user ON public.user_calendar_events(user_id);
CREATE INDEX idx_user_calendar_events_event ON public.user_calendar_events(event_id);
CREATE INDEX idx_user_calendar_events_status ON public.user_calendar_events(user_id, watch_status);
CREATE INDEX idx_notifications_user_unread ON public.notifications(user_id, read_at) WHERE read_at IS NULL;
CREATE INDEX idx_subscriptions_customer ON public.subscriptions(stripe_customer_id);
CREATE INDEX idx_profiles_customer ON public.profiles(stripe_customer_id);

-- Full text search index
CREATE INDEX idx_events_full_text ON public.events USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '') || ' ' || COALESCE(series_name, '')));

-- Row Level Security (RLS) Policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_calendar_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- User calendar events policies
CREATE POLICY "Users can manage own calendar events" ON public.user_calendar_events
    FOR ALL USING (auth.uid() = user_id);

-- Notifications policies
CREATE POLICY "Users can view own notifications" ON public.notifications
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own notifications" ON public.notifications
    FOR UPDATE USING (auth.uid() = user_id);

-- Subscriptions policies
CREATE POLICY "Users can view own subscription" ON public.subscriptions
    FOR SELECT USING (auth.uid() = user_id);

-- Events and categories are public read-only
CREATE POLICY "Events are public readable" ON public.events
    FOR SELECT USING (true);

CREATE POLICY "Event categories are public readable" ON public.event_categories
    FOR SELECT USING (true);

-- Functions for updated_at triggers
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create updated_at triggers
CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.events
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.user_calendar_events
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.subscriptions
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Function to create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, full_name, avatar_url)
    VALUES (
        new.id,
        new.raw_user_meta_data->>'full_name',
        new.raw_user_meta_data->>'avatar_url'
    );
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- Function to update search vector
CREATE OR REPLACE FUNCTION public.update_event_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', 
        NEW.title || ' ' || 
        COALESCE(NEW.description, '') || ' ' || 
        COALESCE(NEW.series_name, '') || ' ' ||
        COALESCE(NEW.episode_title, '') || ' ' ||
        COALESCE(array_to_string(NEW.genres, ' '), '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update search vector
CREATE TRIGGER update_event_search_vector
    BEFORE INSERT OR UPDATE ON public.events
    FOR EACH ROW EXECUTE FUNCTION public.update_event_search_vector();

-- Seed data for event categories
INSERT INTO public.event_categories (name, slug, color, icon, description) VALUES
    ('TV Shows', 'tv-shows', '#8b5cf6', 'tv', 'Television series and episodes'),
    ('Movies', 'movies', '#ef4444', 'film', 'Feature films and documentaries'),
    ('Sports', 'sports', '#22c55e', 'trophy', 'Live sports events and competitions'),
    ('Specials', 'specials', '#f59e0b', 'star', 'Award shows, live events, and specials');

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Additional grants for specific tables
GRANT SELECT ON public.events TO anon;
GRANT SELECT ON public.event_categories TO anon;
