import { TopNav } from "@/components/top-nav";
import { Footer } from "@/components/footer";
import { ChangelogEntry, type ChangelogVersion } from "@/components/changelog-entry";
import { RiHistoryLine } from "@remixicon/react";

export const metadata = {
  title: "Changelog - VidGrab",
  description:
    "View the complete history of VidGrab updates, features, and improvements.",
};

const CHANGELOG: ChangelogVersion[] = [
  {
    version: "1.0.0",
    date: "January 27, 2025",
    description:
      "Initial public release of VidGrab with full feature set and cross-platform support.",
    isLatest: true,
    changes: [
      {
        type: "feature",
        text: "Complete YouTube downloader with playlist support",
      },
      {
        type: "feature",
        text: "Queue management system with persistence",
      },
      {
        type: "feature",
        text: "Multiple quality levels: best, 1080p, 720p, 480p, audio-only",
      },
      {
        type: "feature",
        text: "Multiple format support: MP4, MKV, WebM",
      },
      {
        type: "feature",
        text: "Settings dialog with customizable download folder",
      },
      {
        type: "feature",
        text: "Real-time progress tracking for downloads",
      },
      {
        type: "feature",
        text: "Automatic retry mechanism (up to 3 attempts)",
      },
      {
        type: "feature",
        text: "Detailed error handling and logging system",
      },
      {
        type: "feature",
        text: "Cross-platform support: macOS, Windows, Linux",
      },
      {
        type: "improvement",
        text: "Beautiful PyQt6 user interface",
      },
      {
        type: "improvement",
        text: "Thread-safe multi-threaded download processing",
      },
    ],
  },
  {
    version: "0.9.0",
    date: "January 20, 2025",
    description: "Beta release with core functionality complete.",
    changes: [
      {
        type: "feature",
        text: "Basic download functionality with yt-dlp integration",
      },
      {
        type: "feature",
        text: "Queue management system",
      },
      {
        type: "feature",
        text: "Quality and format selection",
      },
      {
        type: "improvement",
        text: "Initial PyQt6 interface implementation",
      },
      {
        type: "fix",
        text: "Fixed multi-threading issues",
      },
    ],
  },
];

export default function ChangelogPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />

      <section className="py-24 px-6 pt-32 overflow-hidden">
        {/* Background accent */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full filter blur-3xl opacity-20 pointer-events-none" />

        <div className="max-w-4xl mx-auto relative z-10">
          {/* Header */}
          <div className="mb-16 text-center px-4">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                <RiHistoryLine className="w-6 h-6 text-primary" />
              </div>
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold font-mono-display tracking-tight">
                Changelog
              </h1>
            </div>
            <p className="text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
              Track all updates, features, and improvements to VidGrab.
            </p>
          </div>

          {/* Timeline */}
          <div className="relative pl-8 space-y-16">
            {/* Vertical line */}
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-primary via-secondary to-accent opacity-30" />

            {/* Entries */}
            {CHANGELOG.map((version, idx) => (
              <ChangelogEntry key={idx} version={version} />
            ))}
          </div>

          {/* Footer note */}
          <div className="mt-20 p-6 rounded-lg border border-border bg-card/40">
            <p className="text-sm text-foreground/60">
              <strong>Note:</strong> VidGrab follows semantic versioning. Check
              our{" "}
              <a
                href="https://github.com/ellaboevans/vidgrab/releases"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                GitHub Releases page
              </a>{" "}
              for detailed release notes and download links for all versions.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
