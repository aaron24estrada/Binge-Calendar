// lib/supabase.ts
import { createClientComponentClient, createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { Database } from '@/types/database'

export const createClientSupabase = () => createClientComponentClient<Database>()

export const createServerSupabase = () => createServerComponentClient<Database>({ cookies })

export const supabase = createClientSupabase()
