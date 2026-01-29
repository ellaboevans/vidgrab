"use client";

import {
  RiDownloadCloud2Fill,
  RiCodeLine,
  RiGithubFill,
  RiShieldCheckLine,
  RiTimerLine,
} from "@remixicon/react";
import { useEffect, useState } from "react";

export function DownloadSection() {
  const [stars, setStars] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStars = async () => {
    try {
      const response = await fetch(
        "https://api.github.com/repos/ellaboevans/vidgrab",
      );
      const data = await response.json();
      setStars(data.stargazers_count);
    } catch (error) {
      console.error("Failed to fetch GitHub stars:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStars();
  }, []);

  return (
    <section id="download" className="py-32 px-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full filter blur-3xl opacity-40" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/10 rounded-full filter blur-3xl opacity-30" />
      </div>

      <div className="max-w-6xl mx-auto">
        <div className="mb-20 text-center px-4">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-primary/30 bg-primary/5 backdrop-blur-sm mb-6">
            <RiGithubFill className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">
              100% Free & Open Source
            </span>
          </div>
          <h2 className="text-4xl sm:text-5xl md:text-6xl font-bold font-mono-display mb-6 tracking-tight">
            Get Started in <span className="linear-text">Seconds</span>
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Download VidGrab completely free and start downloading YouTube
            videos instantly. No account, no limits, no nonsense.
          </p>
        </div>

        {/* Two column layout: Download + Community */}
        <div className="grid lg:grid-cols-2 gap-8 md:gap-12 mb-16 px-4">
          {/* Main Download Card */}
          <div className="group relative">
            {/* Accent glow */}
            <div className="absolute -inset-0.5 bg-linear-to-r from-primary via-primary/50 to-accent opacity-0 group-hover:opacity-20 rounded-2xl filter blur-xl transition-opacity duration-500" />

            <div className="relative p-8 md:p-10 rounded-2xl border border-primary/30 bg-linear-to-br from-card/80 via-card/60 to-card/40 backdrop-blur-xl group-hover:border-primary/60 transition-all duration-300">
              {/* Header icon */}
              <div className="flex items-start gap-4 mb-8">
                <div className="w-16 h-16 rounded-xl bg-primary/10 flex items-center justify-center group-hover:from-primary/50 group-hover:to-primary/20 transition-all">
                  <RiDownloadCloud2Fill className="w-8 h-8 text-primary" />
                </div>
                <div>
                  <h3 className="text-3xl font-bold mb-1">Download</h3>
                  <p className="text-sm text-foreground/50">
                    Get your installer now
                  </p>
                </div>
              </div>

              {/* Description */}
              <p className="text-foreground/70 mb-8 leading-relaxed">
                Get the latest prebuilt installer for your OS. Just download and
                run, no installation wizards, no dependencies, no complications.
              </p>

              {/* Features grid */}
              <div className="space-y-4 mb-10">
                <div className="flex items-start gap-3">
                  <RiDownloadCloud2Fill className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-sm">macOS Ready</p>
                    <p className="text-xs text-foreground/50">
                      Windows & Linux coming soon
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <RiShieldCheckLine className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-sm">Signed & Notarized</p>
                    <p className="text-xs text-foreground/50">Coming Soon</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <RiTimerLine className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-sm">Auto Updates</p>
                    <p className="text-xs text-foreground/50">
                      One-click updates when available
                    </p>
                  </div>
                </div>
              </div>

              {/* CTA Button */}
              <a
                href="/download"
                className="w-full group/btn relative py-4 px-6 rounded-lg bg-linear-to-r from-primary to-primary/80 text-primary-foreground font-semibold overflow-hidden transition-all hover:shadow-xl hover:shadow-primary/30 hover:scale-105 flex items-center justify-center gap-2">
                <div className="absolute inset-0 bg-linear-to-r from-primary/0 via-white/10 to-primary/0 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
                <RiDownloadCloud2Fill className="w-5 h-5 relative" />
                <span className="relative">Get Installer</span>
              </a>
            </div>
          </div>

          {/* Community/Star Card */}
          <div className="group relative flex flex-col justify-center">
            {/* Accent glow */}
            <div className="absolute -inset-0.5 bg-linear-to-r from-accent/40 via-accent/20 to-primary/20 opacity-0 group-hover:opacity-20 rounded-2xl filter blur-xl transition-opacity duration-500" />

            <div className="relative p-8 md:p-10 rounded-2xl border border-accent/30 bg-linear-to-br from-card/80 via-card/60 to-card/40 backdrop-blur-xl group-hover:border-accent/60 transition-all duration-300">
              {/* Header */}
              <div className="flex items-start gap-4 mb-8">
                <div className="w-16 h-16 rounded-xl bg-accent/10 flex items-center justify-center group-hover:from-accent/50 group-hover:to-accent/20 transition-all">
                  <RiGithubFill className="w-8 h-8 text-accent" />
                </div>
                <div className="flex-1">
                  <h3 className="text-3xl font-bold mb-1">Love VidGrab?</h3>
                  <div className="flex items-center gap-2">
                    <p className="text-sm text-foreground/50">
                      Show your support
                    </p>
                    {!loading && stars !== null && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-accent/10 border border-accent/30 text-xs font-semibold text-accent">
                        ⭐ {stars?.toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Description */}
              <p className="text-foreground/70 mb-8 leading-relaxed">
                Every star on GitHub helps us grow and continue building amazing
                tools for the community. Your support means everything to us.
              </p>

              {/* Benefits */}
              <div className="space-y-3 mb-10 text-sm text-foreground/60">
                <p>✦ Help us reach more people</p>
                <p>✦ Show project viability to contributors</p>
                <p>✦ Motivate continued development</p>
              </div>

              {/* CTA Button */}
              <a
                href="https://github.com/ellaboevans/vidgrab"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full group/btn relative py-4 px-6 rounded-lg bg-linear-to-r from-accent/30 to-accent/20 text-accent font-semibold border border-accent/50 overflow-hidden transition-all hover:border-accent hover:shadow-xl hover:shadow-accent/20 hover:scale-105 flex items-center justify-center gap-2">
                <div className="absolute inset-0 bg-linear-to-r from-accent/0 via-accent/20 to-accent/0 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
                <RiCodeLine className="w-5 h-5 relative" />
                <span className="relative">Star on GitHub</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
