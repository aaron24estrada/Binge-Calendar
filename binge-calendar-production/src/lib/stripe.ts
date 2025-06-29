import Stripe from 'stripe'

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is not defined')
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2023-10-16',
  appInfo: {
    name: 'Binge Calendar',
    version: '1.0.0',
  },
})

// Stripe Price IDs - Update these with your actual price IDs
export const STRIPE_PRICES = {
  PRO_MONTHLY: process.env.STRIPE_PRO_MONTHLY_PRICE_ID!,
  PRO_YEARLY: process.env.STRIPE_PRO_YEARLY_PRICE_ID!,
} as const

export const SUBSCRIPTION_TIERS = {
  FREE: 'free',
  PRO: 'pro',
} as const

export const TIER_LIMITS = {
  [SUBSCRIPTION_TIERS.FREE]: {
    maxEvents: 25,
    maxReminders: 5,
    platforms: ['basic'],
  },
  [SUBSCRIPTION_TIERS.PRO]: {
    maxEvents: Infinity,
    maxReminders: Infinity,
    platforms: ['all'],
  },
} as const
