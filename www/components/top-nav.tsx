import Link from "next/link";
import { RiDownloadCloud2Fill } from "@remixicon/react";
import { GitHubButton } from "@/components/github-button";

export function TopNav() {
  return (
    <nav className="sticky top-0 z-50 glass-effect">
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-2 md:gap-3 group shrink-0">
          <div className="p-2 rounded-lg bg-primary">
            <RiDownloadCloud2Fill className="w-4 md:w-5 h-4 md:h-5 text-primary-foreground" />
          </div>
          <div className="md:flex flex-col hidden sm:flex">
            <span className="font-bold text-base md:text-lg font-mono-display tracking-tight">
              VidGrab
            </span>
          </div>
        </Link>

        {/* Right side links */}
        <div className="flex items-center gap-3 md:gap-6">
          <Link
            href="/#features"
            className="hidden sm:inline text-xs md:text-sm text-foreground/70 hover:text-foreground transition-colors">
            Features
          </Link>
          <a
            href="/download"
            className="hidden sm:inline text-xs md:text-sm text-foreground/70 hover:text-foreground transition-colors">
            Download
          </a>
          <GitHubButton />
        </div>
      </div>
    </nav>
  );
}
