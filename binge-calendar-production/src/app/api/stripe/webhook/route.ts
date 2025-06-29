import { NextRequest, NextResponse } from 'next/server'
import { stripe } from '@/lib/stripe'
import { createServerSupabase } from '@/lib/supabase'
import { headers } from 'next/headers'

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = headers().get('stripe-signature')!

  let event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err: any) {
    console.error('Webhook signature verification failed:', err.message)
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  const supabase = createServerSupabase()

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object
        await handleCheckoutSessionCompleted(session, supabase)
        break

      case 'customer.subscription.updated':
        const updatedSubscription = event.data.object
        await handleSubscriptionUpdated(updatedSubscription, supabase)
        break

      case 'customer.subscription.deleted':
        const deletedSubscription = event.data.object
        await handleSubscriptionDeleted(deletedSubscription, supabase)
        break

      case 'invoice.payment_succeeded':
        const invoice = event.data.object
        await handleInvoicePaymentSucceeded(invoice, supabase)
        break

      case 'invoice.payment_failed':
        const failedInvoice = event.data.object
        await handleInvoicePaymentFailed(failedInvoice, supabase)
        break

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }
  } catch (error) {
    console.error('Webhook processing error:', error)
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    )
  }

  return NextResponse.json({ received: true })
}

async function handleCheckoutSessionCompleted(session: any, supabase: any) {
  const userId = session.metadata?.user_id
  
  if (!userId) {
    console.error('No user_id in session metadata')
    return
  }

  // Update user's subscription status
  await supabase
    .from('profiles')
    .update({
      subscription_tier: 'pro',
      stripe_customer_id: session.customer,
      subscription_status: 'active'
    })
    .eq('id', userId)

  // Create subscription record
  if (session.subscription) {
    const subscription = await stripe.subscriptions.retrieve(session.subscription)
    
    await supabase.from('subscriptions').upsert({
      user_id: userId,
      stripe_subscription_id: subscription.id,
      stripe_customer_id: subscription.customer,
      status: subscription.status,
      current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
      current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
      cancel_at_period_end: subscription.cancel_at_period_end,
    })
  }
}

async function handleSubscriptionUpdated(subscription: any, supabase: any) {
  const { data: profile } = await supabase
    .from('profiles')
    .select('id')
    .eq('stripe_customer_id', subscription.customer)
    .single()

  if (!profile) return

  await supabase.from('subscriptions').upsert({
    user_id: profile.id,
    stripe_subscription_id: subscription.id,
    stripe_customer_id: subscription.customer,
    status: subscription.status,
    current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
    current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
    cancel_at_period_end: subscription.cancel_at_period_end,
  })

  // Update profile subscription tier
  const tier = subscription.status === 'active' ? 'pro' : 'free'
  await supabase
    .from('profiles')
    .update({
      subscription_tier: tier,
      subscription_status: subscription.status
    })
    .eq('id', profile.id)
}

async function handleSubscriptionDeleted(subscription: any, supabase: any) {
  const { data: profile } = await supabase
    .from('profiles')
    .select('id')
    .eq('stripe_customer_id', subscription.customer)
    .single()

  if (!profile) return

  await supabase
    .from('profiles')
    .update({
      subscription_tier: 'free',
      subscription_status: 'canceled'
    })
    .eq('id', profile.id)

  await supabase
    .from('subscriptions')
    .update({ status: 'canceled' })
    .eq('user_id', profile.id)
}

async function handleInvoicePaymentSucceeded(invoice: any, supabase: any) {
  // Handle successful payment
  console.log('Invoice payment succeeded:', invoice.id)
}

async function handleInvoicePaymentFailed(invoice: any, supabase: any) {
  // Handle failed payment
  console.log('Invoice payment failed:', invoice.id)
}
