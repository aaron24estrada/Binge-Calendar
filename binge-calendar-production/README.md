# Binge Calendar

> Never miss your favorite shows, movies, and sports events

A smart calendar application for tracking entertainment content across all platforms. Built with Next.js 14, Supabase, and Stripe.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- GitHub account
- Supabase account (free)
- Stripe account (test mode)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/binge-calendar.git
   cd binge-calendar
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Fill in your keys (see DEPLOYMENT_GUIDE.md for details)
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open [http://localhost:3000](http://localhost:3000)**

## 📋 Complete Deployment Guide

**👉 See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions**

The deployment guide covers:
- GitHub repository setup
- Supabase backend configuration
- Stripe billing integration
- Vercel deployment
- Domain setup and monitoring

## 🏗️ Tech Stack

- **Frontend**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + shadcn/ui
- **Backend**: Supabase (PostgreSQL + Auth + Real-time)
- **Payments**: Stripe (Subscriptions + Webhooks)
- **Deployment**: Vercel
- **Language**: TypeScript

## 📁 Project Structure

```
binge-calendar/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── api/               # API routes
│   │   │   └── stripe/        # Stripe integration
│   │   ├── auth/              # Authentication
│   │   ├── dashboard/         # Protected pages
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Homepage
│   ├── components/            # React components
│   │   ├── ui/               # Base UI components
│   │   └── landing-page.tsx   # Marketing page
│   ├── contexts/             # React contexts
│   ├── lib/                  # Utilities
│   └── types/                # TypeScript types
├── supabase/
│   └── schema.sql            # Database schema
├── design/                   # Design assets (separate from code)
├── package.json
├── tailwind.config.js
└── next.config.js
```

## 🎯 Features

### Free Tier
- ✅ Track up to 25 events
- ✅ Basic calendar view
- ✅ Email reminders
- ✅ Calendar sync

### Pro Tier ($4.99/month)
- ✅ Unlimited events
- ✅ AI recommendations
- ✅ Advanced filtering
- ✅ Custom notifications
- ✅ Priority support

## 🔧 Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run test         # Run tests
npm run type-check   # TypeScript checking
```

### Database Operations

```bash
npm run db:generate  # Generate TypeScript types from Supabase
npm run db:reset     # Reset local database
npm run db:migrate   # Run migrations
```

### Stripe Development

```bash
npm run stripe:listen  # Listen for webhook events locally
```

## 🌐 Environment Variables

Required environment variables (see `.env.example`):

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRO_MONTHLY_PRICE_ID=
STRIPE_PRO_YEARLY_PRICE_ID=

# App
NEXTAUTH_URL=
NEXTAUTH_SECRET=
```

## 📊 Database Schema

The application uses PostgreSQL with the following main tables:

- **profiles** - User profiles and subscription info
- **events** - Entertainment events (shows, movies, sports)
- **user_calendar_events** - User's personal event tracking
- **subscriptions** - Stripe subscription management
- **notifications** - User notifications

Full schema available in `supabase/schema.sql`.

## 🔒 Security

- Row Level Security (RLS) enabled on all user tables
- Server-side API key validation
- Stripe webhook signature verification
- Input validation with Zod schemas
- CSRF protection via Next.js

## 🚢 Deployment

### Production Checklist

- [ ] Environment variables configured in Vercel
- [ ] Supabase production database set up
- [ ] Stripe webhooks configured
- [ ] Domain connected (optional)
- [ ] Analytics configured (optional)

### Monitoring

- **Vercel**: Built-in performance monitoring
- **Supabase**: Database and API monitoring
- **Stripe**: Payment and webhook monitoring

## 🛠️ Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

- [Documentation](./DEPLOYMENT_GUIDE.md)
- [Issues](https://github.com/yourusername/binge-calendar/issues)
- Email: support@bingecalendar.com

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Social features and sharing
- [ ] AI-powered recommendations
- [ ] Platform integrations (Netflix, etc.)
- [ ] Advanced analytics
- [ ] Team/family calendars

---

Built with ❤️ for entertainment enthusiasts
