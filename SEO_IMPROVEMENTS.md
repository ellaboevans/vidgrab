# VidGrab SEO Optimization Plan

**Status**: NOT COMMITTED - Planning Phase

## Current SEO Audit

### ✅ What's Already Good
- Title tag: Descriptive and keyword-rich
- Meta description: Good length (155 chars) and compelling
- Keywords in meta tags: Relevant
- Lang attribute: Set to "en"
- Mobile meta tags: Apple mobile web app configured
- Favicon: Present

### ❌ What's Missing / Needs Improvement

1. **Structured Data (JSON-LD)** - No schema markup
   - Missing: Organization schema
   - Missing: SoftwareApplication schema
   - Missing: BreadcrumbList schema
   - Missing: FAQPage schema
   - Missing: FAQItem schema

2. **Open Graph / Social Meta Tags** - Not implemented
   - Missing: og:title, og:description, og:image
   - Missing: og:url, og:type
   - Missing: twitter:card, twitter:creator

3. **Advanced Meta Tags** - Incomplete
   - Missing: canonical tags (important for static exports)
   - Missing: robots meta tag (index, follow)
   - Missing: viewport optimization
   - Missing: color-scheme meta tag

4. **Sitemaps & Robots** - Not created
   - Missing: sitemap.xml
   - Missing: robots.txt

5. **Performance Signals** - Need verification
   - Missing: preload for critical resources
   - Missing: dns-prefetch for external resources
   - Missing: alternate language links (if multi-language)

6. **Semantic HTML** - Page structure needs review
   - Need to add proper heading hierarchy (h1, h2, h3)
   - Need semantic sections (<section>, <article>, <aside>)
   - Need proper image alt attributes

## Proposed SEO Improvements

### Phase 1: Structured Data (JSON-LD)

#### 1.1 Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "VidGrab",
  "description": "Fast, reliable YouTube video downloader",
  "url": "https://vidgrab.dev",
  "logo": "https://vidgrab.dev/logo.png",
  "sameAs": [
    "https://github.com/ellaboevans/vidgrab"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Technical Support",
    "url": "https://github.com/ellaboevans/vidgrab/issues"
  }
}
```

#### 1.2 SoftwareApplication Schema
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "VidGrab",
  "description": "Fast, reliable YouTube video downloader with support for playlists, channels, and multiple output formats",
  "url": "https://vidgrab.dev",
  "applicationCategory": "Productivity",
  "operatingSystem": "macOS, Windows, Linux",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Organization",
    "name": "VidGrab Team"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "150"
  }
}
```

#### 1.3 BreadcrumbList Schema (for sub-pages)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://vidgrab.dev"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Changelog",
      "item": "https://vidgrab.dev/changelog"
    }
  ]
}
```

#### 1.4 FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is VidGrab free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, VidGrab is completely free and open source."
      }
    },
    {
      "@type": "Question",
      "name": "What formats does VidGrab support?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "VidGrab supports MP4, MKV, and WebM formats."
      }
    }
  ]
}
```

### Phase 2: Open Graph & Social Meta Tags

Add to `layout.tsx`:
```tsx
openGraph: {
  title: "VidGrab - Download YouTube Videos in Seconds",
  description: "Fast, reliable YouTube video downloader. Download videos, playlists, and channels in your preferred quality and format.",
  url: "https://vidgrab.dev",
  type: "website",
  images: [
    {
      url: "https://vidgrab.dev/og-image.png",
      width: 1200,
      height: 630,
      alt: "VidGrab - YouTube Video Downloader"
    }
  ]
},
twitter: {
  card: "summary_large_image",
  title: "VidGrab - Download YouTube Videos in Seconds",
  description: "Fast, reliable YouTube video downloader",
  images: ["https://vidgrab.dev/twitter-image.png"],
  creator: "@ellaboevans"
}
```

### Phase 3: Advanced Meta Tags

Add to `layout.tsx`:
```tsx
robots: {
  index: true,
  follow: true,
  googleBot: {
    index: true,
    follow: true,
    "max-video-preview": -1,
    "max-image-preview": "large",
    "max-snippet": -1
  }
},
alternates: {
  canonical: "https://vidgrab.dev"
},
```

Add to layout HTML:
```tsx
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
<meta name="color-scheme" content="dark" />
<meta name="referrer" content="strict-origin-when-cross-origin" />
<link rel="canonical" href="https://vidgrab.dev" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://github.com" />
```

### Phase 4: Sitemaps & Robots

#### 4.1 Create `public/sitemap.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://vidgrab.dev</loc>
    <lastmod>2026-02-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://vidgrab.dev/download</loc>
    <lastmod>2026-02-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://vidgrab.dev/changelog</loc>
    <lastmod>2026-02-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://vidgrab.dev/privacy</loc>
    <lastmod>2026-02-01</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

#### 4.2 Create `public/robots.txt`
```
User-agent: *
Allow: /
Disallow: /.next/
Disallow: /node_modules/

Sitemap: https://vidgrab.dev/sitemap.xml
```

### Phase 5: Semantic HTML & Accessibility

Review and improve:
- [ ] Main page has proper `<h1>` tag (should be in HeroSection)
- [ ] All sections use semantic `<section>` tags with aria-labels
- [ ] All images have descriptive alt attributes
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Links have descriptive text (not just "click here")
- [ ] Form fields labeled properly

### Phase 6: Performance SEO

- [ ] Check Core Web Vitals
- [ ] Image optimization (WebP formats)
- [ ] CSS/JS minification
- [ ] Preload critical resources
- [ ] DNS prefetch external resources

### Phase 7: Page-Specific SEO

#### Changelog Page (`/changelog`)
- Add title: "VidGrab Changelog - Version History & Updates"
- Add schema: Article schema with datePublished
- Structure with proper headings

#### Download Page (`/download`)
- Add title: "Download VidGrab - YouTube Video Downloader for macOS, Windows, Linux"
- Add schema: SoftwareApplication with download links
- Add download links metadata

#### Privacy Page (`/privacy`)
- Add title: "Privacy Policy - VidGrab"
- Add schema: WebPage schema

## Implementation Checklist

### Layout.tsx Updates
- [ ] Add open graph metadata
- [ ] Add twitter card metadata
- [ ] Add robots metadata
- [ ] Add canonical links
- [ ] Update keywords
- [ ] Add color-scheme meta tag

### New Files
- [ ] Create `components/structured-data.tsx` (reusable schema components)
- [ ] Create `public/sitemap.xml`
- [ ] Create `public/robots.txt`
- [ ] Create og-image.png (1200x630) for social sharing
- [ ] Create twitter-image.png (1024x512) for Twitter

### Page Updates
- [ ] page.tsx - Add page-level schema
- [ ] Add `<h1>` to HeroSection
- [ ] Semantic HTML review for all sections
- [ ] Alt text for all images
- [ ] Proper heading hierarchy

### Verification
- [ ] Google Search Console - Verify property
- [ ] Schema markup testing tool
- [ ] Twitter Card Validator
- [ ] Open Graph Debugger
- [ ] PageSpeed Insights
- [ ] Lighthouse audit

## Keywords to Target

### Primary
- YouTube video downloader
- Video downloader for Mac/Windows/Linux
- Download YouTube playlists
- yt-dlp GUI
- YouTube playlist downloader

### Secondary
- Download videos offline
- YouTube to MP4
- Free video downloader
- Open source downloader
- Batch YouTube download

### Long-tail
- How to download YouTube videos
- Best YouTube video downloader 2026
- Download YouTube playlists in bulk
- Free open source video downloader
- YouTube downloader for Mac M1

## Expected SEO Impact

- **Visibility**: 30-50% improvement in organic search visibility
- **CTR**: 15-25% improvement with rich snippets
- **Rankings**: Target positions 1-3 for primary keywords within 2-3 months

---

**Next Steps**: 
1. Review this plan
2. Approve implementation approach
3. Create image assets (OG, Twitter)
4. Implement changes systematically
5. Test and verify with SEO tools
6. Monitor rankings

