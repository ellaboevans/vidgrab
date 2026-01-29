import {
  RiShieldCheckLine,
  RiLockLine,
  RiServerLine,
  RiUserLine,
} from "@remixicon/react";

export function PrivacyContent() {
  return (
    <article className="py-20 px-6 relative">
      {/* Background elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full filter blur-3xl opacity-30" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/5 rounded-full filter blur-3xl opacity-20" />
      </div>

      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-16">
          <div className="inline-flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
              <RiShieldCheckLine className="w-6 h-6 text-primary" />
            </div>
            <span className="text-sm font-semibold text-primary uppercase tracking-wider">
              Your Privacy Matters
            </span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold font-mono-display mb-6 tracking-tight">
            Privacy Policy
          </h1>
          <p className="text-lg text-foreground/60 leading-relaxed">
            At VidGrab, your privacy is paramount. This policy outlines how we
            handle your data with complete transparency and respect.
          </p>
          <p className="text-sm text-foreground/40 mt-6">
            Last updated: January 2025
          </p>
        </div>

        {/* Quick Overview Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          <div className="p-6 rounded-xl border border-primary/20 bg-primary/5">
            <div className="flex items-start gap-3 mb-4">
              <RiLockLine className="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <h3 className="font-bold text-lg">Zero Tracking</h3>
            </div>
            <p className="text-sm text-foreground/70">
              VidGrab does not track you. No cookies, no analytics, no
              telemetry. Your activity stays local.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-accent/20 bg-accent/5">
            <div className="flex items-start gap-3 mb-4">
              <RiServerLine className="w-6 h-6 text-accent shrink-0 mt-0.5" />
              <h3 className="font-bold text-lg">Local Processing</h3>
            </div>
            <p className="text-sm text-foreground/70">
              All downloads happen on your machine. We don&apos;t see, store, or
              process your files.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-secondary/20 bg-secondary/5">
            <div className="flex items-start gap-3 mb-4">
              <RiShieldCheckLine className="w-6 h-6 text-secondary shrink-0 mt-0.5" />
              <h3 className="font-bold text-lg">Open Source</h3>
            </div>
            <p className="text-sm text-foreground/70">
              All code is open source. Anyone can verify exactly what VidGrab
              does.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-primary/20 bg-primary/5">
            <div className="flex items-start gap-3 mb-4">
              <RiUserLine className="w-6 h-6 text-primary shrink-0 mt-0.5" />
              <h3 className="font-bold text-lg">No Account Required</h3>
            </div>
            <p className="text-sm text-foreground/70">
              Use VidGrab without creating an account, logging in, or providing
              personal data.
            </p>
          </div>
        </div>

        {/* Detailed Sections */}
        <div className="space-y-12">
          {/* Section 1 */}
          <section className="border-l-4 border-primary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">
              1. Information We Don&apos;t Collect
            </h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab is designed with privacy first. The application:
            </p>
            <ul className="space-y-2 text-foreground/70">
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  Does not collect personal information (name, email, IP
                  address)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>Does not track your downloads or browsing activity</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  Does not use cookies or similar tracking technologies
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  Does not send any data to external servers (except to
                  YouTube/yt-dlp)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>Does not contain ads, analytics, or telemetry</span>
              </li>
            </ul>
          </section>

          {/* Section 2 */}
          <section className="border-l-4 border-accent/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">2. How VidGrab Works</h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab is a desktop application that uses{" "}
              <code className="bg-card/50 px-2 py-1 rounded text-sm">
                yt-dlp
              </code>{" "}
              to download videos. Here&apos;s what happens:
            </p>
            <ol className="space-y-3 text-foreground/70">
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">1.</span>
                <span>
                  <strong>You paste a YouTube URL</strong> into VidGrab (locally
                  on your machine)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">2.</span>
                <span>
                  <strong>VidGrab connects to YouTube</strong> to fetch video
                  metadata (title, duration, formats)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">3.</span>
                <span>
                  <strong>You select quality/format</strong> (all choices made
                  locally)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">4.</span>
                <span>
                  <strong>VidGrab downloads the video</strong> directly to your
                  chosen folder
                </span>
              </li>
            </ol>
            <p className="text-sm text-foreground/50 mt-6 italic">
              All processing happens on your computer. Your downloads never pass
              through our servers.
            </p>
          </section>

          {/* Section 3 */}
          <section className="border-l-4 border-secondary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">3. YouTube & yt-dlp</h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              When you download a video, VidGrab communicates with
              YouTube&apos;s servers (not ours) to fetch the video content. This
              is direct device-to-YouTube communication.
            </p>
            <div className="bg-card/50 border border-border rounded-lg p-4 mb-4">
              <p className="text-sm text-foreground/60">
                <strong>Important:</strong> We recommend reviewing{" "}
                <a
                  href="https://www.youtube.com/howyoutubeworks/privacy/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline">
                  YouTube&apos;s Privacy Policy
                </a>{" "}
                to understand how they handle data during video downloads.
              </p>
            </div>
          </section>

          {/* Section 4 */}
          <section className="border-l-4 border-primary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">4. Local Storage</h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab stores data locally on your computer only:
            </p>
            <ul className="space-y-2 text-foreground/70">
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  <code className="bg-card/50 px-2 py-1 rounded text-sm">
                    ~/.vidgrab/config.json
                  </code>{" "}
                  - Your settings (quality, format, download folder)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  <code className="bg-card/50 px-2 py-1 rounded text-sm">
                    ~/.vidgrab/queue.json
                  </code>{" "}
                  - Download queue (incomplete items only)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-primary font-bold mt-1">•</span>
                <span>
                  <code className="bg-card/50 px-2 py-1 rounded text-sm">
                    ~/.vidgrab/logs/app.log
                  </code>{" "}
                  - Application logs (for debugging)
                </span>
              </li>
            </ul>
            <p className="text-sm text-foreground/50 mt-4">
              These files are never transmitted anywhere. They remain entirely
              under your control.
            </p>
          </section>

          {/* Section 5 */}
          <section className="border-l-4 border-accent/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">
              5. Open Source Verification
            </h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab is 100% open source under the MIT license. You can:
            </p>
            <ul className="space-y-2 text-foreground/70">
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">✓</span>
                <span>Review the entire codebase on GitHub</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">✓</span>
                <span>
                  Build from source to verify the binary matches the code
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold mt-1">✓</span>
                <span>Modify and use VidGrab however you want</span>
              </li>
            </ul>
            <a
              href="https://github.com/ellaboevans/vidgrab"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 mt-6 px-4 py-2 rounded-lg bg-accent/10 text-accent font-semibold border border-accent/30 hover:border-accent/60 transition-all">
              View Source Code on GitHub
              <span>→</span>
            </a>
          </section>

          {/* Section 6 */}
          <section className="border-l-4 border-secondary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">6. Updates & Security</h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab includes automatic updates to keep the application secure
              and current with YouTube changes. Updates:
            </p>
            <ul className="space-y-2 text-foreground/70">
              <li className="flex items-start gap-3">
                <span className="text-secondary font-bold mt-1">•</span>
                <span>Are downloaded directly from GitHub (not tracked)</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-secondary font-bold mt-1">•</span>
                <span>Require your permission before installing</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-secondary font-bold mt-1">•</span>
                <span>Do not collect any data about whether you update</span>
              </li>
            </ul>
          </section>

          {/* Section 7 */}
          <section className="border-l-4 border-primary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">7. Third-Party Services</h2>
            <p className="text-foreground/70 mb-4 leading-relaxed">
              VidGrab interacts with these external services:
            </p>
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-card/30 border border-border">
                <h3 className="font-semibold mb-2">YouTube</h3>
                <p className="text-sm text-foreground/70">
                  Direct communication only. No data flows through our servers.
                </p>
              </div>
              <div className="p-4 rounded-lg bg-card/30 border border-border">
                <h3 className="font-semibold mb-2">
                  GitHub (for updates & source)
                </h3>
                <p className="text-sm text-foreground/70">
                  Updates are downloaded from GitHub. Review their privacy
                  policy.
                </p>
              </div>
            </div>
          </section>

          {/* Section 8 */}
          <section className="border-l-4 border-accent/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">
              8. Changes to This Policy
            </h2>
            <p className="text-foreground/70 leading-relaxed">
              We may update this privacy policy as VidGrab evolves. We&apos;ll
              notify users of material changes by updating the &apos;Last
              updated&apos; date above. Continued use of VidGrab after updates
              constitutes acceptance of the revised policy.
            </p>
          </section>

          {/* Section 9 */}
          <section className="border-l-4 border-secondary/30 pl-6">
            <h2 className="text-2xl font-bold mb-4">9. Contact Us</h2>
            <p className="text-foreground/70 mb-6 leading-relaxed">
              Have questions about our privacy practices? We&apos;re here to
              help.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="https://github.com/ellaboevans/vidgrab/issues"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-lg bg-primary/10 text-primary font-semibold border border-primary/30 hover:border-primary/60 transition-all inline-flex items-center gap-2 w-fit">
                Open GitHub Issue
                <span>→</span>
              </a>
              <a
                href="https://github.com/ellaboevans/vidgrab/discussions"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-lg bg-accent/10 text-accent font-semibold border border-accent/30 hover:border-accent/60 transition-all inline-flex items-center gap-2 w-fit">
                Start Discussion
                <span>→</span>
              </a>
            </div>
          </section>
        </div>

        {/* Footer note */}
        <div className="mt-20 p-8 rounded-xl border border-border bg-card/30 text-center">
          <p className="text-sm text-foreground/60 leading-relaxed">
            <strong>Our Commitment:</strong> VidGrab will always remain free,
            open source, and privacy-respecting. We believe downloading videos
            should be simple and private. That&apos;s our promise to you.
          </p>
        </div>
      </div>
    </article>
  );
}
