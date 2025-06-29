#!/usr/bin/env python3
"""
Binge Calendar - Project Setup and Architecture Generation
Creates complete technical architecture, database schema, and code samples
"""

import os
import json
from pathlib import Path

class BingeCalendarArchitect:
    def __init__(self, workspace_dir="/workspace"):
        self.workspace = Path(workspace_dir)
        self.tech_dir = self.workspace / "tech_architecture"
        self.code_dir = self.workspace / "code" / "binge_calendar"
        
    def create_directory_structure(self):
        """Create complete Next.js project structure"""
        directories = [
            "tech_architecture",
            "code/binge_calendar",
            "code/binge_calendar/src/app",
            "code/binge_calendar/src/app/api",
            "code/binge_calendar/src/app/api/auth",
            "code/binge_calendar/src/app/api/events",
            "code/binge_calendar/src/app/api/calendar",
            "code/binge_calendar/src/app/api/stripe",
            "code/binge_calendar/src/app/(auth)",
            "code/binge_calendar/src/app/(dashboard)",
            "code/binge_calendar/src/app/(dashboard)/calendar",
            "code/binge_calendar/src/app/(dashboard)/discover",
            "code/binge_calendar/src/app/(dashboard)/settings",
            "code/binge_calendar/src/components",
            "code/binge_calendar/src/components/ui",
            "code/binge_calendar/src/components/calendar",
            "code/binge_calendar/src/components/events",
            "code/binge_calendar/src/components/auth",
            "code/binge_calendar/src/lib",
            "code/binge_calendar/src/hooks",
            "code/binge_calendar/src/types",
            "code/binge_calendar/src/styles",
            "code/binge_calendar/public",
            "code/binge_calendar/supabase",
            "code/binge_calendar/supabase/migrations",
            "code/binge_calendar/tests",
            "code/binge_calendar/tests/components",
            "code/binge_calendar/tests/api",
        ]
        
        for directory in directories:
            (self.workspace / directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ Directory structure created")
    
    def generate_database_schema(self):
        """Generate complete PostgreSQL schema for Supabase"""
        schema_sql = """-- Binge Calendar Database Schema
-- Supabase PostgreSQL Schema with RLS

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    timezone TEXT DEFAULT 'UTC',
    preferences JSONB DEFAULT '{}',
    subscription_tier TEXT DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro')),
    subscription_id TEXT,
    trial_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Event types and categories
CREATE TABLE public.event_categories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    color TEXT DEFAULT '#6366f1',
    icon TEXT,
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
    
    -- Movie specific fields
    release_type TEXT CHECK (release_type IN ('theatrical', 'streaming', 'digital', 'dvd')),
    
    -- Sports specific fields
    sport_type TEXT,
    teams JSONB,
    league TEXT,
    
    -- Common fields
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    end_datetime TIMESTAMP WITH TIME ZONE,
    timezone TEXT DEFAULT 'UTC',
    platforms JSONB DEFAULT '[]', -- streaming platforms, channels
    external_ids JSONB DEFAULT '{}', -- TMDB, IMDB, ESPN IDs
    poster_url TEXT,
    trailer_url TEXT,
    rating TEXT,
    status TEXT DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'tentative', 'cancelled')),
    
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
    watch_status TEXT DEFAULT 'planning' CHECK (watch_status IN ('planning', 'watching', 'completed', 'dropped')),
    user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 5),
    is_favorite BOOLEAN DEFAULT FALSE,
    
    -- Notification preferences
    notify_before_minutes INTEGER[] DEFAULT '{60, 15}',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, event_id)
);

-- User notification history
CREATE TABLE public.notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    event_id UUID REFERENCES public.events(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('reminder', 'new_episode', 'schedule_change')),
    title TEXT NOT NULL,
    message TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE,
    delivery_method TEXT DEFAULT 'in_app' CHECK (delivery_method IN ('in_app', 'email', 'push'))
);

-- Subscription tracking
CREATE TABLE public.subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE UNIQUE,
    stripe_customer_id TEXT UNIQUE,
    stripe_subscription_id TEXT UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('active', 'canceled', 'past_due', 'unpaid', 'incomplete')),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_events_start_datetime ON public.events(start_datetime);
CREATE INDEX idx_events_category_type ON public.events(category_id, event_type);
CREATE INDEX idx_events_platforms ON public.events USING GIN(platforms);
CREATE INDEX idx_user_calendar_events_user_date ON public.user_calendar_events(user_id, event_id);
CREATE INDEX idx_notifications_user_unread ON public.notifications(user_id, read_at) WHERE read_at IS NULL;

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

-- Add updated_at triggers
CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.events
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.user_calendar_events
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at BEFORE UPDATE ON public.subscriptions
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Seed data for event categories
INSERT INTO public.event_categories (name, slug, color, icon) VALUES
    ('TV Shows', 'tv-shows', '#8b5cf6', 'tv'),
    ('Movies', 'movies', '#ef4444', 'film'),
    ('Sports', 'sports', '#22c55e', 'sports'),
    ('Specials', 'specials', '#f59e0b', 'star');
"""
        
        schema_path = self.tech_dir / "database_schema.sql"
        schema_path.write_text(schema_sql)
        print(f"✅ Database schema created: {schema_path}")
    
    def generate_package_json(self):
        """Generate package.json with all dependencies"""
        package_json = {
            "name": "binge-calendar",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "test": "jest",
                "test:watch": "jest --watch",
                "supabase:start": "supabase start",
                "supabase:reset": "supabase db reset",
                "stripe:listen": "stripe listen --forward-to localhost:3000/api/stripe/webhook"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@supabase/supabase-js": "^2.38.0",
                "@supabase/auth-helpers-nextjs": "^0.8.7",
                "stripe": "^14.0.0",
                "@stripe/stripe-js": "^2.1.0",
                "lucide-react": "^0.290.0",
                "date-fns": "^2.30.0",
                "react-big-calendar": "^1.8.5",
                "react-hook-form": "^7.47.0",
                "@hookform/resolvers": "^3.3.2",
                "zod": "^3.22.4",
                "clsx": "^2.0.0",
                "tailwind-merge": "^2.0.0",
                "class-variance-authority": "^0.7.0",
                "@radix-ui/react-dialog": "^1.0.5",
                "@radix-ui/react-dropdown-menu": "^2.0.6",
                "@radix-ui/react-select": "^2.0.0",
                "@radix-ui/react-switch": "^1.0.3",
                "@radix-ui/react-toast": "^1.1.5",
                "react-query": "^3.39.3",
                "axios": "^1.5.0"
            },
            "devDependencies": {
                "typescript": "^5.2.2",
                "@types/node": "^20.8.0",
                "@types/react": "^18.2.25",
                "@types/react-dom": "^18.2.11",
                "@types/react-big-calendar": "^1.6.6",
                "eslint": "^8.51.0",
                "eslint-config-next": "14.0.0",
                "tailwindcss": "^3.3.5",
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.31",
                "@tailwindcss/forms": "^0.5.6",
                "jest": "^29.7.0",
                "@testing-library/react": "^13.4.0",
                "@testing-library/jest-dom": "^6.1.4",
                "supabase": "^1.100.0"
            }
        }
        
        package_path = self.code_dir / "package.json"
        package_path.write_text(json.dumps(package_json, indent=2))
        print(f"✅ Package.json created: {package_path}")
    
    def generate_env_example(self):
        """Generate environment variables template"""
        env_content = """# Binge Calendar Environment Variables

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Price IDs
STRIPE_PRO_MONTHLY_PRICE_ID=price_your_pro_monthly_price_id

# App Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# External APIs (optional)
TMDB_API_KEY=your_themoviedb_api_key
ESPN_API_KEY=your_espn_api_key

# Email (for notifications)
RESEND_API_KEY=your_resend_api_key
"""
        
        env_path = self.code_dir / ".env.example"
        env_path.write_text(env_content)
        print(f"✅ Environment template created: {env_path}")

def main():
    """Generate complete technical architecture"""
    print("🚀 Generating Binge Calendar Technical Architecture...")
    
    architect = BingeCalendarArchitect()
    
    # Create directory structure
    architect.create_directory_structure()
    
    # Generate database schema
    architect.generate_database_schema()
    
    # Generate package.json
    architect.generate_package_json()
    
    # Generate environment template
    architect.generate_env_example()
    
    print("\n✅ Technical architecture foundation complete!")
    print("📁 Check /workspace/tech_architecture/ and /workspace/code/binge_calendar/")

if __name__ == "__main__":
    main()
