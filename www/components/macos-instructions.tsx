"use client";

import { useState } from "react";
import { RiAppleFill, RiCheckLine, RiTerminalLine } from "@remixicon/react";

const STEPS = [
  {
    title: "Drag to Applications",
    description:
      "After downloading VidGrab.dmg, open the disk image and drag VidGrab.app to your Applications folder.",
    terminal: false,
  },
  {
    title: "Remove Quarantine Flag (Terminal Method)",
    description:
      "Open Terminal and run this command. This is the fastest way to bypass Gatekeeper.",
    command: "xattr -dr com.apple.quarantine /Applications/VidGrab.app",
    terminal: true,
  },
  {
    title: "Open VidGrab",
    description: "Open Applications → VidGrab and launch it normally.",
    terminal: false,
  },
  {
    title: "Done!",
    description: "VidGrab is now ready to use. You only need to do this once.",
    terminal: false,
  },
];

export function MacOSInstructions() {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyCommand = (command: string, index: number) => {
    navigator.clipboard.writeText(command);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <section className="py-24 px-6 relative overflow-hidden bg-linear-to-b from-transparent via-primary/5 to-transparent">
      {/* Background accent */}
      <div className="absolute top-1/2 left-1/4 w-72 h-72 bg-primary/10 rounded-full filter blur-3xl opacity-20 pointer-events-none" />

      <div className="max-w-4xl mx-auto relative z-10 px-4">
        {/* Header */}
        <div className="mb-12 md:mb-16">
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-4 md:mb-6">
            <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center shrink-0">
              <RiAppleFill className="w-6 h-6 text-primary" />
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold font-mono-display">
              macOS Installation
            </h2>
          </div>
          <p className="text-base sm:text-lg text-foreground/60 mb-6 md:mb-8">
            macOS Gatekeeper may block VidGrab on first launch since it&apos;s
            not notarized. This is normal and doesn&apos;t indicate a security
            issue. Follow these steps to get started:
          </p>
        </div>

        {/* Steps */}
        <div className="space-y-4 mb-12 md:mb-16">
          {STEPS.map((step, index) => (
            <div
              key={step.title}
              className="group relative p-6 rounded-lg border border-border bg-card/40 hover:bg-card/80 transition-all hover:border-primary/50">
              {/* Step number */}
              <div className="absolute -left-6 top-6 w-12 h-12 rounded-full bg-linear-to-br from-primary to-secondary flex items-center justify-center text-primary-foreground font-bold">
                {index + 1}
              </div>

              <div className="ml-6">
                {/* Title */}
                <h3 className="text-xl font-bold mb-2">{step.title}</h3>

                {/* Description */}
                <p className="text-foreground/70 mb-4">{step.description}</p>

                {/* Terminal command */}
                {step.terminal && step.command && (
                  <div className="mt-4 p-4 rounded-lg bg-black/60 border border-primary/20">
                    <div className="flex items-center gap-2 mb-3">
                      <RiTerminalLine className="w-4 h-4 text-primary" />
                      <span className="text-xs font-medium text-primary uppercase tracking-widest">
                        Terminal
                      </span>
                    </div>
                    <div className="flex items-start gap-3">
                      <code className="flex-1 font-mono text-sm text-foreground/80">
                        {step.command}
                      </code>
                      <button
                        onClick={() => copyCommand(step.command, index)}
                        className="shrink-0 px-3 py-1 rounded bg-primary/20 hover:bg-primary/30 text-primary text-xs font-medium transition-all">
                        {copiedIndex === index ? "Copied!" : "Copy"}
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Checkmark animation */}
              <div className="absolute right-6 top-6 w-6 h-6 rounded-full border-2 border-primary opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <RiCheckLine className="w-4 h-4 text-primary" />
              </div>
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="mt-16 space-y-6">
          <h3 className="text-2xl font-bold">Common Questions</h3>

          <div className="space-y-4">
            <div className="p-6 rounded-lg border border-border bg-card/40">
              <h4 className="font-bold mb-2">
                Why does macOS show this warning?
              </h4>
              <p className="text-foreground/70">
                Apple requires all distributed apps to be notarized using a paid
                Developer ID ($99/year). Since VidGrab is a free, open-source
                project, it&apos;s distributed without notarization. The warning
                is about <strong>verification</strong>, not malware. You can
                always review the{" "}
                <a
                  href="https://github.com/ellaboevans/vidgrab"
                  className="text-primary hover:underline">
                  full source code on GitHub
                </a>
              </p>
            </div>

            <div className="p-6 rounded-lg border border-border bg-card/40">
              <h4 className="font-bold mb-2">Is VidGrab safe?</h4>
              <p className="text-foreground/70 mb-3">Absolutely. VidGrab is:</p>
              <ul className="space-y-2 text-foreground/70">
                <li className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                  100% open source
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                  No background services
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                  No system modifications
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                  No bundled installers
                </li>
              </ul>
            </div>

            <div className="p-6 rounded-lg border border-border bg-card/40">
              <h4 className="font-bold mb-2">
                What if the app doesn&apos;t open?
              </h4>
              <p className="text-foreground/70 mb-3">
                Run VidGrab from Terminal to see error output:
              </p>
              <div className="p-3 rounded bg-black/60 border border-border">
                <code className="font-mono text-sm text-foreground/80">
                  /Applications/VidGrab.app/Contents/MacOS/VidGrab
                </code>
              </div>
              <p className="text-foreground/70 mt-3">
                If you encounter issues, please{" "}
                <a
                  href="https://github.com/ellaboevans/vidgrab/issues"
                  className="text-primary hover:underline">
                  open an issue on GitHub
                </a>{" "}
                with the output.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
