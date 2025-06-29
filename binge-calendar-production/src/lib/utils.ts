import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string) {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function formatTime(date: Date | string) {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDateTime(date: Date | string) {
  const d = new Date(date)
  return {
    date: formatDate(d),
    time: formatTime(d),
  }
}

export function getEventTypeColor(eventType: string) {
  const colors = {
    tv_show: '#8b5cf6',
    movie: '#ef4444',
    sports: '#22c55e',
    special: '#f59e0b',
  }
  return colors[eventType as keyof typeof colors] || '#6366f1'
}

export function truncate(str: string, length: number) {
  if (str.length <= length) return str
  return str.slice(0, length) + '...'
}
