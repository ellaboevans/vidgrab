"use client";

import {
  RiAppleFill,
  RiWindowsFill,
  RiTerminalBoxLine,
  RiDownloadCloud2Fill,
  RemixiconComponentType,
} from "@remixicon/react";
import { useEffect, useState } from "react";

interface DownloadAsset {
  name: string;
  icon: RemixiconComponentType;
  description: string;
  specs: string[];
  downloadLink?: string;
  theme: "primary" | "accent" | "secondary";
  status: "ready" | "coming-soon";
  downloadCount?: number;
  assetName?: string;
}

const DOWNLOADS: DownloadAsset[] = [
  {
    name: "macOS (Apple Silicon)",
    icon: RiAppleFill,
    description: "For Apple Silicon (M1, M2, M3, etc.)",
    specs: ["macOS 10.14+", "Apple Silicon processor", "~100 MB"],
    downloadLink: "#",
    theme: "primary",
    status: "ready",
    assetName: "VidGrab-arm64.dmg",
  },
  {
    name: "macOS (Intel)",
    icon: RiAppleFill,
    description: "For Intel-based Macs",
    specs: ["macOS 10.14+", "Intel processor", "~100 MB"],
    downloadLink: "#",
    theme: "primary",
    status: "ready",
    assetName: "VidGrab-intel.dmg",
  },
  {
    name: "Windows",
    icon: RiWindowsFill,
    description: "64-bit executable, standalone install",
    specs: ["Windows 10/11", "64-bit processor", "~100 MB"],
    downloadLink: "#",
    theme: "accent",
    status: "coming-soon",
    assetName: "VidGrab.exe",
  },
  {
    name: "Linux",
    icon: RiTerminalBoxLine,
    description: "Universal binary, works on most distros",
    specs: ["Any modern distro", "glibc 2.29+", "~50 MB"],
    downloadLink: "#",
    theme: "secondary",
    status: "coming-soon",
    assetName: "VidGrab",
  },
];

export function DownloadGrid() {
  const [downloads, setDownloads] = useState<DownloadAsset[]>(DOWNLOADS);

  useEffect(() => {
    const fetchDownloadCounts = async () => {
      try {
        const response = await fetch("/api/download-counts");
        const data = await response.json();
        if (!response.ok) throw new Error("Failed to fetch download counts");
        const totals = data.totals || {};
        const latestAssets = data.latestAssets || {};

        setDownloads((prev) =>
          prev.map((dl) => {
            if (!dl.assetName) return dl;
            const latest = latestAssets[dl.assetName];
            return {
              ...dl,
              downloadLink: latest?.url || dl.downloadLink,
              downloadCount: totals[dl.assetName],
            };
          }),
        );
      } catch (error) {
        console.error("Failed to fetch download counts:", error);
        // Fallback to releases page if API fails
        setDownloads((prev) =>
          prev.map((dl) =>
            dl.assetName
              ? {
                  ...dl,
                  downloadLink:
                    "https://github.com/ellaboevans/vidgrab/releases/latest",
                }
              : dl,
          ),
        );
      }
    };

    fetchDownloadCounts();
  }, []);

  return (
    <section className="py-24 px-6 pt-32 overflow-hidden">
      {/* Background accent */}

      <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full filter blur-3xl opacity-20 pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Header */}
        <div className="mb-12 md:mb-16 text-center px-4">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold font-mono-display mb-4 md:mb-6 tracking-tight">
            Download VidGrab
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Choose your operating system and download the latest version. All
            binaries are self-contained and ready to run.
          </p>
        </div>

        {/* Download Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mb-12 md:mb-16 px-4">
          {downloads.map((platform) => {
            const Icon = platform.icon;
            const themeColor =
              platform.theme === "primary"
                ? "primary"
                : platform.theme === "accent"
                  ? "accent"
                  : "secondary";

            return (
              <div
                key={platform.name}
                className="group relative p-8 rounded-xl border transition-all duration-300"
                style={{
                  borderColor:
                    themeColor === "primary"
                      ? "rgba(255, 107, 53, 0.3)"
                      : themeColor === "accent"
                        ? "rgba(0, 212, 255, 0.3)"
                        : "rgba(247, 147, 30, 0.3)",
                  backgroundColor:
                    themeColor === "primary"
                      ? "rgba(255, 107, 53, 0.05)"
                      : themeColor === "accent"
                        ? "rgba(0, 212, 255, 0.05)"
                        : "rgba(247, 147, 30, 0.05)",
                }}>
                <div className="relative z-10">
                  {/* Icon */}
                  <div
                    className="w-16 h-16 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform"
                    style={{
                      background:
                        themeColor === "primary"
                          ? "linear-gradient(135deg, #ff6b35, rgba(255,107,53,0.5))"
                          : themeColor === "accent"
                            ? "linear-gradient(135deg, #00d4ff, rgba(0,212,255,0.5))"
                            : "linear-gradient(135deg, #f7931e, rgba(247,147,30,0.5))",
                    }}>
                    <Icon className="w-8 h-8 text-foreground" />
                  </div>

                  {/* Name + Download Count */}
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-2xl font-bold group-hover:text-primary transition-colors">
                      {platform.name}
                    </h3>
                  </div>

                  {/* Description */}
                  <p className="text-foreground/60 text-sm mb-4">
                    {platform.description}
                  </p>

                  {/* Specs */}
                  <ul className="space-y-2 mb-6">
                    {platform.specs.map((spec) => (
                      <li
                        key={spec}
                        className="text-sm text-foreground/70 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                        {spec}
                      </li>
                    ))}
                  </ul>

                  {/* Download Button */}
                  {platform.status === "ready" ? (
                    <a
                      href={platform.downloadLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full py-3 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 border hover:opacity-80"
                      style={{
                        background:
                          themeColor === "primary"
                            ? "rgba(255, 107, 53, 0.2)"
                            : themeColor === "accent"
                              ? "rgba(0, 212, 255, 0.2)"
                              : "rgba(247, 147, 30, 0.2)",
                        borderColor:
                          themeColor === "primary"
                            ? "rgba(255, 107, 53, 0.5)"
                            : themeColor === "accent"
                              ? "rgba(0, 212, 255, 0.5)"
                              : "rgba(247, 147, 30, 0.5)",
                        color:
                          themeColor === "primary"
                            ? "#ff6b35"
                            : themeColor === "accent"
                              ? "#00d4ff"
                              : "#f7931e",
                      }}>
                      <RiDownloadCloud2Fill className="w-5 h-5" />
                      Download
                      {platform.downloadCount !== undefined && (
                        <span>({platform.downloadCount.toLocaleString()})</span>
                      )}
                    </a>
                  ) : (
                    <button
                      disabled
                      className="w-full py-3 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 border opacity-50 cursor-not-allowed"
                      style={{
                        background:
                          themeColor === "primary"
                            ? "rgba(255, 107, 53, 0.1)"
                            : themeColor === "accent"
                              ? "rgba(0, 212, 255, 0.1)"
                              : "rgba(247, 147, 30, 0.1)",
                        borderColor:
                          themeColor === "primary"
                            ? "rgba(255, 107, 53, 0.3)"
                            : themeColor === "accent"
                              ? "rgba(0, 212, 255, 0.3)"
                              : "rgba(247, 147, 30, 0.3)",
                        color:
                          themeColor === "primary"
                            ? "#ff6b35"
                            : themeColor === "accent"
                              ? "#00d4ff"
                              : "#f7931e",
                      }}>
                      Coming Soon
                      {platform.downloadCount !== undefined && (
                        <span>({platform.downloadCount.toLocaleString()})</span>
                      )}
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Alternative: From Source */}
        <div className="glass-effect border border-border rounded-xl p-6 md:p-8 mx-4">
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <div className="w-1 h-8 bg-linear-to-b from-primary to-secondary rounded-full" />
            Build from Source
          </h2>
          <p className="text-foreground/70 mb-6">
            For developers who want to build VidGrab themselves or contribute to
            the project:
          </p>
          <a
            href="https://github.com/ellaboevans/vidgrab#building-your-own-executable"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-accent/20 text-accent font-semibold border border-accent/50 hover:bg-accent/30 hover:border-accent transition-all">
            View Build Instructions
          </a>
        </div>
      </div>
    </section>
  );
}

function fetchLatestRelease() {
  throw new Error("Function not implemented.");
}
