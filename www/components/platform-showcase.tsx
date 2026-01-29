"use client";

import {
  RiAppleFill,
  RiWindowsFill,
  RiTerminalBoxLine,
} from "@remixicon/react";
import { motion } from "framer-motion";
import Link from "next/link";

const PLATFORMS = [
  {
    name: "macOS",
    icon: RiAppleFill,
    description: "Universal binary for Intel & Apple Silicon",
    features: [
      "Native Performance",
      "Gatekeeper Compatible",
      "Sign & Notarized",
    ],
    status: "ready",
  },
  {
    name: "Windows",
    icon: RiWindowsFill,
    description: "64-bit executable, standalone install",
    features: ["No Dependencies", "Quick Start", "Update Ready"],
    status: "coming-soon",
  },
  {
    name: "Linux",
    icon: RiTerminalBoxLine,
    description: "Universal binary, works on most distros",
    features: ["Lightweight", "Open Source", "Terminal Ready"],
    status: "coming-soon",
  },
];

export function PlatformShowcase() {
  return (
    <section className="py-24 px-6 relative overflow-hidden">
      {/* Background accent */}
      <div className="absolute -top-32 -right-32 w-64 h-64 bg-secondary/10 rounded-full filter blur-3xl opacity-20 pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="mb-12 md:mb-16 text-center px-4">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold font-mono-display mb-4 md:mb-6 tracking-tight">
            Works Everywhere
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Download VidGrab for your operating system and start downloading in
            seconds.
          </p>
        </div>

        <motion.div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 px-4">
          {PLATFORMS.map((platform, idx) => {
            const Icon = platform.icon;
            return (
              <motion.div
                key={platform.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                viewport={{ once: true }}
                className="group relative p-8 rounded-xl border border-border bg-linear-to-br from-card/80 hover:from-card to-card/60 transition-all duration-300 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10">
                {/* Accent linear top-right */}
                <div className="absolute -top-px -right-px w-32 h-32 bg-linear-to-br from-primary/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-full filter blur-2xl" />

                <div className="relative z-10">
                  {/* Icon */}
                  <div className="w-16 h-16 rounded-lg bg-primary/10 flex items-center justify-center mb-6 group-hover:from-primary/50 group-hover:to-secondary/40 transition-all">
                    <Icon className="w-8 h-8 text-primary" />
                  </div>

                  {/* Name */}
                  <h3 className="text-2xl font-bold mb-2 group-hover:text-primary transition-colors">
                    {platform.name}
                  </h3>

                  {/* Description */}
                  <p className="text-foreground/60 text-sm mb-6">
                    {platform.description}
                  </p>

                  {/* Features list */}
                  <ul className="space-y-2">
                    {platform.features.map((feature) => (
                      <li
                        key={feature}
                        className="text-sm text-foreground/70 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  {/* Download button */}
                  {platform.status === "ready" ? (
                    <Link href="/download">
                      <button className="mt-8 w-full py-3 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary font-semibold transition-all border border-primary/30 hover:border-primary/50 group/btn relative overflow-hidden">
                        <div className="absolute inset-0 bg-linear-to-r from-primary/0 via-primary/20 to-primary/0 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
                        <span className="relative">Available Now</span>
                      </button>
                    </Link>
                  ) : (
                    <button
                      disabled
                      className="mt-8 w-full py-3 rounded-lg bg-primary/5 text-primary font-semibold transition-all border border-primary/20 group/btn relative overflow-hidden opacity-50 cursor-not-allowed">
                      <span className="relative">Coming Soon</span>
                    </button>
                  )}
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
