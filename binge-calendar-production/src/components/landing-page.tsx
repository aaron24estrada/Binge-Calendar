'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Check, Calendar, Bell, Star, Zap } from 'lucide-react'
import { useAuth } from '@/contexts/auth-context'

export function LandingPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const { signIn } = useAuth()

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return

    setLoading(true)
    setMessage('')

    const { error } = await signIn(email)

    if (error) {
      setMessage(error.message)
    } else {
      setMessage('Check your email for the magic link!')
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Calendar className="h-8 w-8 text-indigo-600" />
            <span className="text-2xl font-bold text-gray-900">Binge Calendar</span>
          </div>
          <Button variant="outline">Sign In</Button>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <Badge variant="secondary" className="mb-4">
          🎬 Never Miss What Matters
        </Badge>
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Your Entertainment
          <span className="text-indigo-600"> Calendar</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Track TV shows, movie releases, and sports events in one smart calendar. 
          Get personalized reminders and never miss your favorite content.
        </p>

        {/* Sign Up Form */}
        <Card className="max-w-md mx-auto">
          <CardHeader>
            <CardTitle>Get Started Free</CardTitle>
            <CardDescription>Enter your email to create your calendar</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSignIn} className="space-y-4">
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Sending Magic Link...' : 'Start Tracking Free'}
              </Button>
              {message && (
                <p className={`text-sm ${message.includes('Check') ? 'text-green-600' : 'text-red-600'}`}>
                  {message}
                </p>
              )}
            </form>
          </CardContent>
        </Card>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Everything You Need</h2>
          <p className="text-lg text-gray-600">Powerful features to organize your entertainment</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <Calendar className="h-10 w-10 text-indigo-600 mb-2" />
              <CardTitle>Smart Calendar</CardTitle>
              <CardDescription>
                See all your entertainment in one calendar view with custom categories
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Bell className="h-10 w-10 text-indigo-600 mb-2" />
              <CardTitle>Smart Reminders</CardTitle>
              <CardDescription>
                Get notified before your shows start, with customizable timing
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Star className="h-10 w-10 text-indigo-600 mb-2" />
              <CardTitle>Track Everything</CardTitle>
              <CardDescription>
                TV shows, movies, sports, specials - all in one organized place
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Simple Pricing</h2>
          <p className="text-lg text-gray-600">Start free, upgrade when you need more</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Free</CardTitle>
              <CardDescription>Perfect for casual viewers</CardDescription>
              <div className="text-3xl font-bold">$0<span className="text-lg font-normal">/month</span></div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Up to 25 events</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Basic reminders</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Calendar sync</span>
                </div>
              </div>
              <Button variant="outline" className="w-full">Current Plan</Button>
            </CardContent>
          </Card>

          <Card className="border-indigo-200 bg-indigo-50">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Pro</CardTitle>
                  <CardDescription>For entertainment enthusiasts</CardDescription>
                </div>
                <Badge className="bg-indigo-600">Popular</Badge>
              </div>
              <div className="text-3xl font-bold">$4.99<span className="text-lg font-normal">/month</span></div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Unlimited events</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>AI recommendations</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Advanced reminders</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Platform filters</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Check className="h-4 w-4 text-green-600" />
                  <span>Priority support</span>
                </div>
              </div>
              <Button className="w-full">
                <Zap className="h-4 w-4 mr-2" />
                Upgrade to Pro
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Calendar className="h-6 w-6" />
            <span className="text-xl font-bold">Binge Calendar</span>
          </div>
          <p className="text-gray-400 mb-4">Never miss what matters to you</p>
          <p className="text-sm text-gray-500">© 2024 Binge Calendar. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
