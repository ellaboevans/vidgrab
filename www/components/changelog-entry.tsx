import { RiCheckLine, RiBugLine, RiGiftLine } from "@remixicon/react";

export interface ChangelogItem {
  type: "feature" | "fix" | "improvement";
  text: string;
}

export interface ChangelogVersion {
  version: string;
  date: string;
  description: string;
  changes: ChangelogItem[];
  isLatest?: boolean;
}

interface ChangelogEntryProps {
  version: ChangelogVersion;
}

export function ChangelogEntry({ version }: ChangelogEntryProps) {
  const getIcon = (type: string) => {
    switch (type) {
      case "feature":
        return <RiGiftLine className="w-4 h-4 text-primary" />;
      case "fix":
        return <RiBugLine className="w-4 h-4 text-destructive" />;
      case "improvement":
        return <RiCheckLine className="w-4 h-4 text-secondary" />;
      default:
        return <RiCheckLine className="w-4 h-4 text-accent" />;
    }
  };

  const getColor = (type: string) => {
    switch (type) {
      case "feature":
        return "border-primary/30 bg-primary/5";
      case "fix":
        return "border-destructive/30 bg-destructive/5";
      case "improvement":
        return "border-secondary/30 bg-secondary/5";
      default:
        return "border-accent/30 bg-accent/5";
    }
  };

  return (
    <div className="relative">
      {/* Timeline dot */}
      <div className="absolute -left-8 top-2 w-4 h-4 rounded-full bg-gradient-to-br from-primary to-secondary border-4 border-background" />

      <div className="pl-0">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-4">
          <div>
            <h3 className="text-xl md:text-2xl font-bold font-mono-display">
              v{version.version}
            </h3>
            <p className="text-sm text-foreground/50">{version.date}</p>
          </div>
          {version.isLatest && (
            <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/20 text-primary text-xs font-bold uppercase tracking-widest w-fit">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              Latest
            </span>
          )}
        </div>

        {/* Description */}
        <p className="text-foreground/70 mb-6">{version.description}</p>

        {/* Changes */}
        <div className="space-y-3">
          {version.changes.map((change, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-lg border flex gap-3 ${getColor(change.type)}`}
            >
              <div className="flex-shrink-0 mt-0.5">{getIcon(change.type)}</div>
              <div className="flex-1">
                <p className="text-sm text-foreground/80">{change.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
