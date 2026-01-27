import { RiDownloadCloud2Fill, RiExternalLinkLine, RiCodeLine } from "@remixicon/react";

export function DownloadSection() {
  return (
    <section
      id="download"
      className="py-24 px-6 relative overflow-hidden bg-gradient-to-b from-transparent via-primary/5 to-transparent"
    >
      {/* Animated background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/10 rounded-full filter blur-3xl opacity-30" />
      </div>

      <div className="max-w-5xl mx-auto">
        <div className="mb-12 md:mb-16 text-center px-4">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold font-mono-display mb-4 md:mb-6 tracking-tight">
            Get Started in Seconds
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Download the latest version or run from source. VidGrab works
            instantly.
          </p>
        </div>

        {/* Two column layout: Download vs Source */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 mb-12 px-4">
          {/* Download section */}
          <div className="p-8 rounded-xl border-2 border-primary/40 bg-gradient-to-br from-primary/10 to-transparent hover:border-primary/60 transition-all">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-lg bg-primary text-primary-foreground flex items-center justify-center">
                <RiDownloadCloud2Fill className="w-6 h-6" />
              </div>
              <h3 className="text-2xl font-bold">Download Binary</h3>
            </div>

            <p className="text-foreground/70 mb-6">
              Get the latest prebuilt executable for your OS. No installation
              required, just download and run.
            </p>

            <div className="space-y-3 mb-6">
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-primary" />
                <span>Available for macOS, Windows, Linux</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-primary" />
                <span>Automatically signed and notarized</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-primary" />
                <span>Updates with one click</span>
              </div>
            </div>

            <a
              href="https://github.com/ellaboevans/vidgrab/releases"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-primary text-primary-foreground font-semibold hover:shadow-lg hover:shadow-primary/50 transition-all hover:scale-105"
            >
              <RiDownloadCloud2Fill className="w-5 h-5" />
              Download Latest Release
              <RiExternalLinkLine className="w-4 h-4" />
            </a>
          </div>

          {/* Source section */}
          <div className="p-8 rounded-xl border-2 border-accent/40 bg-gradient-to-br from-accent/10 to-transparent hover:border-accent/60 transition-all">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-lg bg-accent text-accent-foreground flex items-center justify-center">
                <RiCodeLine className="w-6 h-6" />
              </div>
              <h3 className="text-2xl font-bold">Build from Source</h3>
            </div>

            <p className="text-foreground/70 mb-6">
              Clone the repository and build VidGrab yourself. Perfect for
              developers and contributors.
            </p>

            <div className="space-y-3 mb-6">
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-accent" />
                <span>100% open source on GitHub</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-accent" />
                <span>MIT licensed, modify freely</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-accent" />
                <span>Detailed build instructions included</span>
              </div>
            </div>

            <a
              href="https://github.com/ellaboevans/vidgrab"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-accent/20 text-accent font-semibold border border-accent/50 hover:bg-accent/30 hover:border-accent transition-all hover:shadow-lg hover:shadow-accent/30"
            >
              <RiCodeLine className="w-5 h-5" />
              View Source Code
              <RiExternalLinkLine className="w-4 h-4" />
            </a>
          </div>
        </div>

        {/* System requirements */}
        <div className="glass-effect border border-border rounded-xl p-8">
          <h4 className="font-semibold mb-6 text-lg">System Requirements</h4>
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <h5 className="font-mono-display font-bold mb-2">macOS</h5>
              <ul className="text-sm text-foreground/70 space-y-1">
                <li>• macOS 10.14+</li>
                <li>• Intel or Apple Silicon</li>
                <li>• ~50 MB disk space</li>
              </ul>
            </div>
            <div>
              <h5 className="font-mono-display font-bold mb-2">Windows</h5>
              <ul className="text-sm text-foreground/70 space-y-1">
                <li>• Windows 10/11</li>
                <li>• 64-bit processor</li>
                <li>• ~100 MB disk space</li>
              </ul>
            </div>
            <div>
              <h5 className="font-mono-display font-bold mb-2">Linux</h5>
              <ul className="text-sm text-foreground/70 space-y-1">
                <li>• Any modern distro</li>
                <li>• glibc 2.29+</li>
                <li>• ~50 MB disk space</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
