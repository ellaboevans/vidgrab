# VidGrab Landing Page Architecture

## Overview

The VidGrab landing page is built with **Next.js 16**, **Tailwind CSS 4**, and **Remix Icons**, following modern frontend best practices with a focus on **server components first** and **snake_case component naming**.

## Design System

### Color Palette (Dark Theme)
- **Primary**: `#ff6b35` (Vibrant Orange) - Primary actions and accents
- **Secondary**: `#f7931e` (Golden Orange) - Supporting highlights
- **Accent**: `#00d4ff` (Cyan) - Secondary CTA and interactive states
- **Background**: `#0a0a0a` (Deep Black) - Main background
- **Foreground**: `#f5f5f5` (Off-White) - Primary text
- **Muted**: `#262626` (Dark Gray) - Secondary surfaces

### Typography
- **Display Font**: Space Mono (monospace, bold headlines)
- **Body Font**: IBM Plex Sans (readable, professional)
- **CSS Variable**: `--font-mono-display` for display text

### Custom Animations
- `float-up`: Staggered entrance animation (0.8s)
- `glow-pulse`: Subtle opacity pulse (3s)
- `slide-in-left/right`: Directional entrance animations
- `gradient-shift`: Animated gradient background shift (8s)

## Component Structure

```
www/
├── app/
│   ├── layout.tsx          # Root layout with font setup
│   ├── page.tsx            # Main landing page (server)
│   └── globals.css         # Global styles & theme variables
├── components/
│   ├── top-nav.tsx         # Sticky header with logo & navigation
│   ├── hero-section.tsx    # Hero with animated stats carousel
│   ├── features-section.tsx # 6-feature grid with hover effects
│   ├── quality-options.tsx # Quality & format selector cards
│   ├── platform-showcase.tsx # macOS, Windows, Linux cards
│   ├── download-section.tsx # Dual-column download & source
│   └── footer.tsx          # Footer with links & social
└── public/                 # Static assets
```

## Component Details

### top-nav.tsx (Server)
- Sticky navigation bar with glass-effect styling
- Logo with gradient icon
- Navigation links: Features, Download, GitHub
- No client-side interactivity

### hero-section.tsx (Client)
- Full-screen hero with animated background gradients
- Floating "Playlist Support" badge
- Primary CTA: "Download Now" with gradient
- Rotating stats carousel (cycles every 3s)
- Staggered animations on mount

### features-section.tsx (Server)
- 6-column grid (responsive: 2 on mobile, 3 on desktop)
- Each feature card has:
  - Gradient icon background
  - Hover scale & border effects
  - Animated accent line on hover
  - Icon + Title + Description

### quality-options.tsx (Client)
- Split into two columns: Quality & Format
- Interactive radio-style selectors
- Quality options: Best, 1080p, 720p, 480p, Audio-only
- Format options: MP4 (popular), MKV, WebM
- Checkbox animation on hover

### platform-showcase.tsx (Server)
- 3-column grid for macOS, Windows, Linux
- Each card includes:
  - OS icon with gradient background
  - Feature list (3 items)
  - Download button with gradient hover effect
- Hover effects with gradient overlay

### download-section.tsx (Server)
- Dual-column layout: Binary vs. Source
- Left column (Primary theme): Pre-built downloads
- Right column (Accent theme): Build from source
- System requirements table (3 columns)
- External links with icons

### footer.tsx (Server)
- 4-column navigation grid
- Social links (GitHub)
- Bottom copyright section
- Heart icon with brand color

## Next.js Best Practices

✅ **Server Components by Default**
- Most components are server components (no 'use client')
- Only stateful components use 'use client' directive
- Reduces JavaScript bundle size

✅ **Page-Level Routing**
- Single page app structure: `/`
- No nested routes yet (can add `/docs`, `/blog` later)

✅ **Tailwind CSS 4 Integration**
- Modern `@import "tailwindcss"` syntax
- CSS variable theme support via `:root`
- Custom animations in globals.css
- No build config needed with built-in support

✅ **Image Optimization**
- Uses Next.js fonts: Space Mono, IBM Plex Sans
- Font subsetting for Latin only
- System fonts as fallback

## Styling Architecture

### Utility-First with Custom Layers

```css
@layer base { /* Reset & global styles */ }
@layer components { /* Reusable component classes */ }
@layer utilities { /* Animation delays, glass effects */ }
```

### Glass Morphism Effect
```css
.glass-effect {
  background: rgba(18, 18, 18, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 107, 53, 0.1);
}
```

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(135deg, #ff6b35, #f7931e, #00d4ff);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## Performance Optimizations

- **Static Generation**: All pages pre-rendered at build time
- **Zero JS on Nav**: Top nav is pure server-rendered HTML
- **Lazy Client Components**: Hero, Quality selector load only when needed
- **CSS-Only Animations**: No Motion library, pure Tailwind + CSS
- **Responsive Images**: SVG icons from Remix Icon

## Development Workflow

### Setup
```bash
cd www
npm install
npm run dev  # http://localhost:3000
```

### Build & Deploy
```bash
npm run build  # Creates optimized bundle
npm start      # Production server
```

### File Naming Convention
- Components: `snake-case.tsx` (e.g., `top-nav.tsx`)
- Pages: lowercase (e.g., `page.tsx`, `layout.tsx`)
- Imports: destructured components
- No barrel exports (import directly from files)

## Accessibility & SEO

✅ **Semantic HTML**
- Proper heading hierarchy (h1, h2, h3)
- `<nav>`, `<section>`, `<footer>` landmarks
- Link relationships defined

✅ **Metadata**
- Descriptive title & meta description
- Open Graph support ready
- Proper `lang="en"` attribute

✅ **Keyboard Navigation**
- All interactive elements are keyboard-accessible
- Focus states via Tailwind classes
- Links have hover/focus states

## Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Pricing page for pro features
- [ ] Blog section for updates
- [ ] Documentation page
- [ ] Interactive feature demo
- [ ] User testimonials section
- [ ] Newsletter signup
- [ ] Analytics integration

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16.1.5 |
| Styling | Tailwind CSS 4 |
| Icons | Remix Icon 4.8.0 |
| UI | shadcn (optional) |
| Typography | Space Mono, IBM Plex Sans |
| Runtime | Node.js 18+ |

---

**Last Updated**: January 27, 2025
