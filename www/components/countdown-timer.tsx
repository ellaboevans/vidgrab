"use client";

import { useEffect, useState } from "react";

interface TimeUnit {
  label: string;
  value: number;
}

export function CountdownTimer() {
  const [timeUnits, setTimeUnits] = useState<TimeUnit[]>([
    { label: "Days", value: 0 },
    { label: "Hours", value: 0 },
    { label: "Minutes", value: 0 },
    { label: "Seconds", value: 0 },
  ]);

  useEffect(() => {
    const calculateCountdown = () => {
      const launchDate = new Date("2026-02-7").getTime();
      const now = Date.now();
      const difference = launchDate - now;

      if (difference > 0) {
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor(
          (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60),
        );
        const minutes = Math.floor(
          (difference % (1000 * 60 * 60)) / (1000 * 60),
        );
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        setTimeUnits([
          { label: "Days", value: days },
          { label: "Hours", value: hours },
          { label: "Minutes", value: minutes },
          { label: "Seconds", value: seconds },
        ]);
      }
    };

    calculateCountdown();
    const timer = setInterval(calculateCountdown, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex justify-center gap-4 md:gap-8">
      {timeUnits.map((unit) => (
        <div key={unit.label} className="flex flex-col items-center">
          {/* Animated digit box */}
          <div className="relative w-16 h-20 md:w-24 md:h-28 mb-3">
            {/* Background glow effect */}
            <div className="absolute inset-0 bg-linear-to-b from-primary/20 to-primary/5 rounded-lg" />

            {/* Border with accent */}
            <div className="absolute inset-0 rounded-lg border-2 border-primary/30" />

            {/* Center divider line for visual interest */}
            <div className="absolute inset-x-0 top-1/2 h-px bg-primary/10 -translate-y-1/2" />

            {/* Animated digit */}
            <div
              key={unit.value}
              className="relative w-full h-full flex items-center justify-center overflow-hidden">
              <span className="text-2xl md:text-4xl font-bold text-primary font-mono-display tabular-nums">
                {String(unit.value).padStart(2, "0")}
              </span>
            </div>
          </div>

          {/* Label */}
          <span className="text-xs md:text-sm font-semibold text-foreground/70 uppercase tracking-wider">
            {unit.label}
          </span>
        </div>
      ))}
    </div>
  );
}
