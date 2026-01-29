import {
  RiGithubFill,
  RiExternalLinkLine,
  RiHeartFill,
  RiTwitterXFill,
} from "@remixicon/react";

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-border bg-card/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-12 md:py-16">
        {/* Main content */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8 mb-8 md:mb-12">
          {/* About */}
          <div>
            <h4 className="font-bold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a
                  href="#features"
                  className="hover:text-foreground transition">
                  Features
                </a>
              </li>
              <li>
                <a
                  href="#download"
                  className="hover:text-foreground transition">
                  Downloads
                </a>
              </li>
              <li>
                <a
                  href="/changelog"
                  className="hover:text-foreground transition">
                  Changelog
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/ellaboevans/vidgrab"
                  className="hover:text-foreground transition flex items-center gap-1">
                  GitHub
                  <RiExternalLinkLine className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>

          {/* Documentation */}
          <div>
            <h4 className="font-bold mb-4">Learn</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a
                  href="https://github.com/ellaboevans/vidgrab#readme"
                  className="hover:text-foreground transition flex items-center gap-1">
                  Documentation
                  <RiExternalLinkLine className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/ellaboevans/vidgrab/issues"
                  className="hover:text-foreground transition flex items-center gap-1">
                  Report Issues
                  <RiExternalLinkLine className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/ellaboevans/vidgrab/discussions"
                  className="hover:text-foreground transition flex items-center gap-1">
                  Discussions
                  <RiExternalLinkLine className="w-3 h-3" />
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-bold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-foreground/70">
              <li>
                <a
                  href="https://github.com/ellaboevans/vidgrab/blob/main/LICENSE"
                  className="hover:text-foreground transition">
                  MIT License
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/yt-dlp/yt-dlp"
                  className="hover:text-foreground transition flex items-center gap-1">
                  yt-dlp
                  <RiExternalLinkLine className="w-3 h-3" />
                </a>
              </li>
              <li>
                <a href="/privacy" className="hover:text-foreground transition">
                  Privacy
                </a>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold mb-4">Connect</h4>
            <div className="flex gap-3">
              <a
                href="https://github.com/ellaboevans/vidgrab"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg border border-border hover:border-primary bg-card/50 hover:bg-primary/10 flex items-center justify-center transition-all">
                <RiGithubFill className="w-5 h-5" />
              </a>
              <a
                href="https://x.com/dev_concept"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg border border-border hover:border-accent bg-card/50 hover:bg-accent/10 flex items-center justify-center transition-all">
                <RiTwitterXFill className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-border my-6 md:my-8" />

        {/* Bottom section */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs sm:text-sm text-foreground/60">
          <p>
            Made with{" "}
            <RiHeartFill className="w-4 h-4 text-primary inline mx-1" />
            for the community
          </p>
          <p>VidGrab © {year}. Open Source. Forever Free.</p>
        </div>
      </div>
    </footer>
  );
}
