import type { Metadata } from "next";
import { IBM_Plex_Sans } from "next/font/google";
import "./globals.css";

const ibmPlexSans = IBM_Plex_Sans({
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "VidGrab - Download YouTube Videos in Seconds",
  description:
    "Fast, reliable YouTube video downloader. Download videos, playlists, and channels in your preferred quality and format. Open source, no ads, pure speed.",
  keywords: [
    "VidGrab",
    "video downloader",
    "playlist downloader",
    "yt-dlp",
    "open source",
  ],
  authors: [{ name: "VidGrab Team" }],
  creator: "VidGrab",
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
      </head>
      <body className={`${ibmPlexSans.variable} antialiased overflow-x-hidden`}>
        {children}
      </body>
    </html>
  );
}
