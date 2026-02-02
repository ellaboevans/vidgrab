import { CountdownTimer } from "@/components/countdown-timer";

export function ComingSoonView() {
  return (
    <div className="fixed inset-0 z-40 bg-background overflow-auto">
      {/* Animated background elements */}
      <div className="fixed inset-0 pointer-events-none">
        {/* Grid background */}
        <svg
          className="absolute inset-0 w-full h-full opacity-10"
          xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse">
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="currentColor"
                strokeWidth="0.5"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>

        {/* Top accent */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full filter blur-3xl opacity-20" />
        {/* Bottom accent */}
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent/10 rounded-full filter blur-3xl opacity-20" />
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 md:px-6">
        <div className="max-w-3xl mx-auto text-center space-y-12">
          {/* Header */}
          <div className="space-y-6">
            <div className="inline-block">
              <div className="px-4 py-2 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-semibold">
                This is still being cooked!
              </div>
            </div>

            <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold font-mono-display tracking-tight">
              Something Exciting is Coming Your Way
            </h1>

            <p className="text-lg md:text-xl text-foreground/70 max-w-2xl mx-auto leading-relaxed">
              We&apos;re working hard to bring you an enhanced VidGrab
              experience. Be among the first to access our new features and
              improvements.
            </p>
          </div>

          {/* Countdown Timer */}
          <div className="py-8 md:py-12">
            <CountdownTimer />
          </div>

          <div className="space-y-4">
            <p className="text-foreground/60 text-sm md:text-base">
              <a
                title="click me"
                href="https://x.com/dev_concept"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline italic hover:text-white duration-100 ease-in">
                Follow the creator on x for more updates
              </a>
            </p>
          </div>

          {/* Footer note */}
          <div className="pt-8 border-t border-border/40">
            <p className="text-foreground/50 text-xs md:text-sm">
              This countdown is a preview. Check back soon for official
              announcements.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
