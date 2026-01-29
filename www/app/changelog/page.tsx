import { TopNav } from "@/components/top-nav";
import { Footer } from "@/components/footer";
import { DynamicReleases } from "@/components/dynamic-releases";
import { RiHistoryLine } from "@remixicon/react";

export const metadata = {
  title: "Changelog - VidGrab",
  description:
    "View the complete history of VidGrab updates, features, and improvements.",
};

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
              Track all updates, features, and improvements to VidGrab. Releases
              are pulled directly from GitHub.
            </p>
          </div>

          {/* Dynamic Releases */}
          <DynamicReleases />

          {/* Footer note */}
          <div className="mt-16 p-6 rounded-lg border border-border bg-card/40">
            <p className="text-sm text-foreground/60">
              <strong>How it works:</strong> This changelog is automatically
              generated from our{" "}
              <a
                href="https://github.com/ellaboevans/vidgrab/releases"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline">
                GitHub Releases
              </a>
              . Create a release on GitHub, write your changelog once, and it
              appears here automatically.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
