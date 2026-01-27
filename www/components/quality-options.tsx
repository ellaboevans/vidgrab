'use client';

import { RiCheckLine } from "@remixicon/react";

const QUALITY_OPTIONS = [
  { label: "Best", value: "best", badge: "4K Ready" },
  { label: "1080p", value: "1080p", badge: "HD" },
  { label: "720p", value: "720p", badge: "Balanced" },
  { label: "480p", value: "480p", badge: "Fast" },
  { label: "Audio Only", value: "audio", badge: "Music" },
];

const FORMAT_OPTIONS = [
  { label: "MP4", value: "mp4", popular: true },
  { label: "MKV", value: "mkv" },
  { label: "WebM", value: "webm" },
];

export function QualityOptions() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12 md:mb-20 text-center px-4">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold font-mono-display mb-4 md:mb-6 tracking-tight">
            Choose Your Perfect Format
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            VidGrab supports all major formats and quality levels. Download
            exactly what you need.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 px-4">
          {/* Quality section */}
          <div>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <span className="w-1 h-8 bg-gradient-to-b from-primary to-secondary rounded-full" />
              Video Quality
            </h3>
            <div className="space-y-3">
              {QUALITY_OPTIONS.map((option) => (
                <div
                  key={option.value}
                  className="group p-4 rounded-lg border border-border hover:border-primary/50 bg-card/50 hover:bg-card/80 transition-all cursor-pointer hover:shadow-lg hover:shadow-primary/10"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full border-2 border-primary/30 group-hover:border-primary flex items-center justify-center transition-all">
                        <RiCheckLine className="w-3 h-3 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                      <div>
                        <div className="font-semibold">{option.label}</div>
                        <div className="text-xs text-muted-foreground">
                          {option.badge}
                        </div>
                      </div>
                    </div>
                    <div className="text-xs bg-primary/20 text-primary px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                      {option.value}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Format section */}
          <div>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <span className="w-1 h-8 bg-gradient-to-b from-secondary to-accent rounded-full" />
              Output Format
            </h3>
            <div className="space-y-3">
              {FORMAT_OPTIONS.map((option) => (
                <div
                  key={option.value}
                  className="group relative p-4 rounded-lg border transition-all cursor-pointer hover:shadow-lg"
                  style={{
                    borderColor: option.popular ? "rgba(0, 212, 255, 0.5)" : "rgba(37, 37, 37, 1)",
                    backgroundColor: option.popular
                      ? "rgba(0, 212, 255, 0.05)"
                      : "rgba(18, 18, 18, 0.5)",
                  }}
                >
                  {option.popular && (
                    <div className="absolute -top-2 right-4 bg-accent text-accent-foreground text-xs font-bold px-3 py-1 rounded-full">
                      Popular
                    </div>
                  )}
                  <div className="flex items-center gap-3">
                    <div className="w-5 h-5 rounded-full border-2 border-accent/50 group-hover:border-accent flex items-center justify-center transition-all">
                      <RiCheckLine className="w-3 h-3 text-accent opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <div>
                      <div className="font-semibold">{option.label}</div>
                      <div className="text-xs text-muted-foreground">
                        Universal format, widely supported
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
