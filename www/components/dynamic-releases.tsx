"use client";

import { useEffect, useState } from "react";
import {
  RiDownloadCloud2Fill,
  RiCalendarLine,
  RiGithubFill,
} from "@remixicon/react";
import { motion } from "framer-motion";

interface Asset {
  name: string;
  download_count: number;
  browser_download_url: string;
  size: number;
}

interface Release {
  id: number;
  tag_name: string;
  name: string;
  body: string;
  published_at: string;
  assets: Asset[];
  prerelease: boolean;
  draft: boolean;
}

export function DynamicReleases() {
  const [releases, setReleases] = useState<Release[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReleases = async () => {
      try {
        const response = await fetch(
          "https://api.github.com/repos/ellaboevans/vidgrab/releases",
        );
        if (!response.ok) throw new Error("Failed to fetch releases");
        const data = await response.json();
        setReleases(data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch releases:", err);
        setError("Unable to load releases. Please check GitHub directly.");
      } finally {
        setLoading(false);
      }
    };

    fetchReleases();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  };

  const parseMarkdown = (text: string) => {
    return text.split("\n").map((line, idx) => {
      if (line.startsWith("## ")) {
        return (
          <h3 key={idx + 1} className="text-lg font-bold mt-4 mb-2">
            {line.replace("## ", "")}
          </h3>
        );
      }
      if (line.startsWith("- ")) {
        return (
          <li key={idx + 1} className="ml-4">
            {line.replace("- ", "")}
          </li>
        );
      }
      if (line.trim() === "") {
        return <div key={idx + 1} className="h-2" />;
      }
      return (
        <p key={idx + 1} className="text-foreground/70">
          {line}
        </p>
      );
    });
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="p-6 rounded-xl border border-border bg-card/30 animate-pulse">
            <div className="h-6 bg-border rounded w-1/4 mb-4" />
            <div className="h-4 bg-border rounded w-1/2 mb-2" />
            <div className="h-4 bg-border rounded w-3/4" />
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 rounded-xl border border-accent/30 bg-accent/5">
        <p className="text-accent font-semibold mb-4">{error}</p>
        <a
          href="https://github.com/ellaboevans/vidgrab/releases"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent/10 text-accent font-semibold border border-accent/30 hover:border-accent/60 transition-all">
          <RiGithubFill className="w-5 h-5" />
          View on GitHub
          <span>→</span>
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {releases.map((release, idx) => (
        <motion.div
          key={release.id}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: idx * 0.1 }}
          viewport={{ once: true }}
          className={`relative p-8 rounded-xl border transition-all ${
            release.prerelease
              ? "border-amber-500/30 bg-amber-500/5"
              : "border-primary/30 bg-primary/5"
          }`}>
          {/* Header */}
          <div className="flex items-start justify-between gap-4 mb-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h3 className="text-2xl font-bold font-mono-display">
                  {release.name || release.tag_name}
                </h3>
                {release.prerelease && (
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-600 border border-amber-500/30">
                    Pre-release
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 text-sm text-foreground/60">
                <RiCalendarLine className="w-4 h-4" />
                <time dateTime={release.published_at}>
                  {formatDate(release.published_at)}
                </time>
              </div>
            </div>
          </div>

          {/* Release Notes */}
          {release.body && (
            <div className="mb-6 prose prose-sm max-w-none dark:prose-invert text-foreground/70 space-y-2">
              {parseMarkdown(release.body)}
            </div>
          )}

          {/* Assets/Downloads */}
          {release.assets.length > 0 && (
            <div className="mt-6 pt-6 border-t border-border">
              <h4 className="font-semibold mb-4 flex items-center gap-2">
                <RiDownloadCloud2Fill className="w-4 h-4" />
                Downloads
              </h4>
              <div className="space-y-2">
                {release.assets.map((asset) => (
                  <a
                    key={asset.name}
                    href={asset.browser_download_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between p-3 rounded-lg border border-border bg-card/40 hover:border-primary/50 hover:bg-primary/5 transition-all group">
                    <div className="flex items-center gap-3 flex-1">
                      <RiDownloadCloud2Fill className="w-4 h-4 text-primary group-hover:text-primary/70 transition-colors" />
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-sm truncate">
                          {asset.name}
                        </p>
                        <p className="text-xs text-foreground/50">
                          {formatBytes(asset.size)} •{" "}
                          {asset.download_count.toLocaleString()} download
                          {asset.download_count !== 1 ? "s" : ""}
                        </p>
                      </div>
                    </div>
                    <span className="text-primary group-hover:translate-x-1 transition-transform ml-2">
                      ↓
                    </span>
                  </a>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      ))}

      {/* No releases fallback */}
      {releases.length === 0 && (
        <div className="p-6 rounded-xl border border-border bg-card/40 text-center">
          <p className="text-foreground/60">No releases found.</p>
          <a
            href="https://github.com/ellaboevans/vidgrab/releases"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-lg bg-primary/10 text-primary font-semibold border border-primary/30 hover:border-primary/60 transition-all">
            <RiGithubFill className="w-5 h-5" />
            View on GitHub
          </a>
        </div>
      )}
    </div>
  );
}
