'use client';

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  RiCodeLine,
  RiTerminalLine,
  RiCheckLine,
  RiExternalLinkLine,
} from "@remixicon/react";

const BUILD_STEPS = [
  {
    title: "Clone the Repository",
    description: "Get the latest source code from GitHub",
    command: "git clone https://github.com/ellaboevans/vidgrab.git\ncd vidgrab",
  },
  {
    title: "Set Up Virtual Environment",
    description: "Create an isolated Python environment",
    command: "python3 -m venv .venv\nsource .venv/bin/activate  # On Windows: .venv\\Scripts\\activate",
  },
  {
    title: "Install Dependencies",
    description: "Install required Python packages",
    command: "pip install -r requirements.txt",
  },
  {
    title: "Build Executable",
    description: "Create the standalone application",
    command: "# macOS/Linux\nchmod +x build.sh && ./build.sh\n\n# Windows\nbuild.bat",
  },
];

interface BuildDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export function BuildDialog({ isOpen, onClose }: BuildDialogProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyCommand = (command: string, index: number) => {
    navigator.clipboard.writeText(command);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-card border-border">
        {/* Header */}
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
              <RiCodeLine className="w-5 h-5 text-primary" />
            </div>
            <div>
              <DialogTitle className="text-2xl">Build from Source</DialogTitle>
              <DialogDescription className="text-foreground/50">
                For developers and contributors
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        {/* Content */}
        <div className="space-y-6 py-6">
          <p className="text-foreground/70">
            Follow these steps to build VidGrab from source. You'll need Git,
            Python 3.8+, and a C compiler.
          </p>

          {/* Steps */}
          <div className="space-y-6">
            {BUILD_STEPS.map((step, index) => (
              <div key={index} className="relative">
                {/* Step indicator */}
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-primary-foreground font-bold text-sm mt-1">
                    {index + 1}
                  </div>

                  <div className="flex-1 min-w-0">
                    {/* Title */}
                    <h3 className="font-bold text-lg mb-1">{step.title}</h3>

                    {/* Description */}
                    <p className="text-sm text-foreground/60 mb-3">
                      {step.description}
                    </p>

                    {/* Command block */}
                    <div className="bg-black/60 border border-primary/20 rounded-lg p-4 overflow-x-auto">
                      <div className="flex items-center gap-2 mb-3">
                        <RiTerminalLine className="w-4 h-4 text-primary flex-shrink-0" />
                        <span className="text-xs font-medium text-primary uppercase tracking-widest">
                          Terminal
                        </span>
                      </div>
                      <code className="font-mono text-sm text-foreground/80 whitespace-pre-wrap break-words">
                        {step.command}
                      </code>

                      {/* Copy button */}
                      <button
                        onClick={() => copyCommand(step.command, index)}
                        className="mt-3 px-3 py-1.5 rounded bg-primary/20 hover:bg-primary/30 text-primary text-xs font-medium transition-all inline-flex items-center gap-2"
                      >
                        {copiedIndex === index ? (
                          <>
                            <RiCheckLine className="w-3 h-3" />
                            Copied!
                          </>
                        ) : (
                          <>
                            <RiTerminalLine className="w-3 h-3" />
                            Copy
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Divider */}
                {index < BUILD_STEPS.length - 1 && (
                  <div className="mt-6 ml-4 h-8 border-l border-border/50" />
                )}
              </div>
            ))}
          </div>

          {/* Info box */}
          <div className="p-4 rounded-lg bg-accent/5 border border-accent/20">
            <p className="text-sm text-foreground/70">
              <strong>Need help?</strong> Visit the{" "}
              <a
                href="https://github.com/ellaboevans/vidgrab"
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent hover:underline inline-flex items-center gap-1"
              >
                GitHub repository
                <RiExternalLinkLine className="w-3 h-3" />
              </a>{" "}
              for detailed documentation and issue support.
            </p>
          </div>
        </div>

        {/* Footer */}
        <DialogFooter className="gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-lg bg-accent/10 hover:bg-accent/20 text-accent font-medium transition-colors"
          >
            Close
          </button>
          <a
            href="https://github.com/ellaboevans/vidgrab"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2.5 rounded-lg bg-primary/20 hover:bg-primary/30 text-primary font-medium transition-colors inline-flex items-center gap-2"
          >
            View GitHub
            <RiExternalLinkLine className="w-4 h-4" />
          </a>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
