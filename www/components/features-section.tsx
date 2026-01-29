"use client";

import {
  RiLightbulbFlashLine,
  RiDownloadCloud2Fill,
  RiSettings3Line,
  RiShieldCheckLine,
  RiRefreshLine,
  RiLineChartLine,
} from "@remixicon/react";
import { motion } from "framer-motion";
import { BackgroundPattern } from "./background-pattern";

const FEATURES = [
  {
    icon: RiLightbulbFlashLine,
    title: "Lightning Fast",
    description:
      "Download videos at maximum speed. Powered by yt-dlp, the industry standard for YouTube downloads.",
  },
  {
    icon: RiDownloadCloud2Fill,
    title: "Batch Downloads",
    description:
      "Download entire playlists, channels, or multiple videos at once. Your queue persists between sessions.",
  },
  {
    icon: RiSettings3Line,
    title: "Full Control",
    description:
      "Choose quality (720p, 1080p, 4K), format (MP4, MKV, WebM), and output folder. All configurable in seconds.",
  },
  {
    icon: RiShieldCheckLine,
    title: "Privacy First",
    description:
      "100% local processing. No data collection, no tracking, no accounts needed. Download anything privately.",
  },
  {
    icon: RiRefreshLine,
    title: "Auto Retry",
    description:
      "Downloads fail? VidGrab automatically retries up to 3 times with intelligent backoff.",
  },
  {
    icon: RiLineChartLine,
    title: "Real-time Insights",
    description:
      "Watch progress in real-time. See which videos are downloading, completed, or failed at a glance.",
  },
];

export function FeaturesSection() {
  return (
    <section
      id="features"
      className="relative py-24 px-6 overflow-hidden bg-linear-to-b from-transparent via-card/30 to-transparent">
      <BackgroundPattern
        variant="grid"
        position="bottom-right"
        intensity="heavy"
      />
      <div className="max-w-7xl mx-auto">
        {/* Section header */}
        <div className="mb-12 md:mb-20 text-center px-4">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold font-mono-display mb-4 md:mb-6 tracking-tight">
            Built for Power Users
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Everything you need to download, manage, and organize your YouTube
            content.
          </p>
        </div>

        {/* Features grid */}
        <motion.div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 px-4">
          {FEATURES.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={idx + 1}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                viewport={{ once: true }}
                className="group p-6 rounded-xl border border-border bg-card/40 hover:bg-card/80 transition-all duration-300 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10 hover:-translate-y-1">
                {/* Icon */}
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:from-primary/40 group-hover:to-secondary/40 transition-all">
                  <Icon className="w-6 h-6 text-primary" />
                </div>

                {/* Title */}
                <h3 className="text-lg font-bold mb-3 group-hover:text-primary transition-colors">
                  {feature.title}
                </h3>

                {/* Description */}
                <p className="text-foreground/60 leading-relaxed text-sm">
                  {feature.description}
                </p>

                {/* Accent line */}
                <div className="mt-4 h-1 w-0 bg-linear-to-r from-primary to-secondary rounded-full group-hover:w-8 transition-all duration-300" />
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
