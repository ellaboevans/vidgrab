'use client';

import { RiDownloadCloud2Fill, RiLightbulbFlashLine, RiShieldCheckLine, RiCpuLine } from "@remixicon/react";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BackgroundPattern } from "./background-pattern";

const FEATURED_STATS = [
  { label: "Downloads", value: "1M+", icon: RiDownloadCloud2Fill },
  { label: "Speed", value: "100 Mbps", icon: RiLightbulbFlashLine },
  { label: "Privacy", value: "100%", icon: RiShieldCheckLine },
  { label: "Zero CPU", value: "Idle", icon: RiCpuLine },
];

export function HeroSection() {
  const [activeStatIndex, setActiveStatIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStatIndex((prev) => (prev + 1) % FEATURED_STATS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20 pb-20">
      {/* Background pattern */}
      <BackgroundPattern variant="grid" position="top-left" intensity="light" />

      {/* Animated background gradient */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full filter blur-3xl opacity-20 animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full filter blur-3xl opacity-20 animate-pulse delay-500" />
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-secondary/15 rounded-full filter blur-3xl opacity-15" />
      </div>

      <div className="max-w-5xl mx-auto px-6 relative z-10">
        {/* Floating badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0 }}
          className="mb-6 md:mb-8 inline-flex items-center gap-2 px-3 md:px-4 py-2 rounded-full border border-primary/30 bg-primary/5 backdrop-blur-sm"
        >
          <RiLightbulbFlashLine className="w-3 md:w-4 h-3 md:h-4 text-primary" />
          <span className="text-xs md:text-sm font-medium text-primary">
            Now with Playlist Support
          </span>
        </motion.div>

        {/* Main headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className="font-mono-display text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-4 md:mb-6 leading-tight"
        >
          Download YouTube
          <br />
          <span className="gradient-text">at Lightning Speed</span>
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-base sm:text-lg md:text-xl text-foreground/70 max-w-2xl mb-8 md:mb-12 leading-relaxed"
        >
          VidGrab brings the power of yt-dlp to your desktop. No ads, no
          tracking, no nonsense. Just pure speed and reliability.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-3 md:gap-4 mb-16 md:mb-20"
        >
          <a
            href="/download"
            className="group relative px-8 py-4 rounded-lg bg-gradient-to-r from-primary to-secondary text-primary-foreground font-semibold overflow-hidden transition-all hover:shadow-lg hover:shadow-primary/50 hover:scale-105"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-secondary to-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            <span className="relative flex items-center justify-center gap-2">
              <RiDownloadCloud2Fill className="w-5 h-5" />
              Download Now
            </span>
          </a>

          <a
            href="https://github.com/ellaboevans/vidgrab"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 rounded-lg border-2 border-accent text-accent font-semibold hover:bg-accent/10 transition-all hover:shadow-lg hover:shadow-accent/20"
          >
            View on GitHub
          </a>
        </motion.div>

        {/* Rotating stats carousel */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4"
        >
          {FEATURED_STATS.map((stat, idx) => {
            const Icon = stat.icon;
            const isActive = idx === activeStatIndex;
            return (
              <div
                key={idx}
                className={`p-6 rounded-lg border transition-all duration-500 ${
                  isActive
                    ? "glass-effect border-primary/50 bg-primary/10"
                    : "border-border bg-card/50"
                }`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <Icon
                    className={`w-5 h-5 transition-colors ${
                      isActive ? "text-primary" : "text-muted-foreground"
                    }`}
                  />
                  <span className="text-xs text-muted-foreground uppercase tracking-widest">
                    {stat.label}
                  </span>
                </div>
                <div
                  className={`text-2xl font-bold transition-all ${
                    isActive ? "text-primary scale-105" : "text-foreground"
                  }`}
                >
                  {stat.value}
                </div>
              </div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
