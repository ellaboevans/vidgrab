import { TopNav } from "@/components/top-nav";
import { DownloadGrid } from "@/components/download-grid";
import { MacOSInstructions } from "@/components/macos-instructions";
import { Footer } from "@/components/footer";

export const metadata = {
  title: "Download VidGrab - YouTube Downloader for macOS, Windows & Linux",
  description:
    "Download VidGrab for macOS, Windows, or Linux. Free, open-source YouTube video downloader with step-by-step installation guides for all platforms.",
  keywords: [
    "download VidGrab",
    "YouTube downloader download",
    "free video downloader",
    "macOS downloader",
    "Windows downloader",
    "Linux downloader",
  ],
  openGraph: {
    title: "Download VidGrab - YouTube Downloader for All Platforms",
    description:
      "Download VidGrab for macOS, Windows, or Linux. Free, open-source YouTube video downloader.",
    url: `${process.env.NEXT_PUBLIC_SITE_URL as string}/download`,
    type: "website",
  },
};

export default function DownloadPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />
      <DownloadGrid />
      <MacOSInstructions />
      <Footer />
    </main>
  );
}
