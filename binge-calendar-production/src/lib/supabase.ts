import { createClientComponentClient, createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { Database } from '@/types/database'

export const createServerSupabase = () => createServerComponentClient<Database>({ cookies })

export const createClientSupabase = () => createClientComponentClient<Database>()

export const supabase = createClientSupabase()
