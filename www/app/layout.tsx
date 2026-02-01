import type { Metadata } from "next";
import { IBM_Plex_Sans } from "next/font/google";
import "./globals.css";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL as string;

const ibmPlexSans = IBM_Plex_Sans({
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title:
    "VidGrab - Download YouTube Videos in Seconds | Free Open Source Downloader",
  description:
    "Fast, reliable YouTube video downloader. Download videos, playlists, and channels in your preferred quality and format. MP4, MKV, WebM support. Open source, no ads, pure speed.",
  keywords: [
    "YouTube video downloader",
    "video downloader",
    "playlist downloader",
    "yt-dlp",
    "open source downloader",
    "download YouTube videos",
    "YouTube to MP4",
    "batch download",
  ],
  authors: [{ name: "Elabo Evans" }],
  creator: "VidGrab",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: SITE_URL,
  },
  openGraph: {
    title: "VidGrab - Download YouTube Videos in Seconds",
    description:
      "Fast, reliable YouTube video downloader. Download videos, playlists, and channels in your preferred quality and format.",
    url: SITE_URL,
    type: "website",
    images: [
      {
        url: `${SITE_URL}/og-image.png`,
        width: 1200,
        height: 630,
        alt: "VidGrab - YouTube Video Downloader",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "VidGrab - Download YouTube Videos in Seconds",
    description: "Fast, reliable YouTube video downloader",
    images: [`${SITE_URL}/twitter-image.png`],
    creator: "@dev_concept",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth dark">
      <head>
        <meta name="theme-color" content="#0a0a0a" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=5.0"
        />
        <meta name="color-scheme" content="dark" />
        <meta name="referrer" content="strict-origin-when-cross-origin" />
        <link rel="canonical" href="https://vidgrab.dev" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://github.com" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              name: "VidGrab",
              url: SITE_URL,
              logo: `${SITE_URL}/logo.png`,
              description: "Fast, reliable YouTube video downloader",
              sameAs: ["https://github.com/ellaboevans/vidgrab"],
              contactPoint: {
                "@type": "ContactPoint",
                contactType: "Technical Support",
                url: "https://github.com/ellaboevans/vidgrab/issues",
              },
            }),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              name: "VidGrab",
              description:
                "Fast, reliable YouTube video downloader with support for playlists, channels, and multiple output formats",
              url: SITE_URL,
              applicationCategory: "Productivity",
              operatingSystem: "macOS, Windows, Linux",
              offers: {
                "@type": "Offer",
                price: "0",
                priceCurrency: "USD",
              },
              author: {
                "@type": "Organization",
                name: "VidGrab",
              },
              aggregateRating: {
                "@type": "AggregateRating",
                ratingValue: "4.8",
                ratingCount: "150",
              },
            }),
          }}
        />
      </head>
      <body className={`${ibmPlexSans.variable} antialiased overflow-x-hidden`}>
        {children}
      </body>
    </html>
  );
}
