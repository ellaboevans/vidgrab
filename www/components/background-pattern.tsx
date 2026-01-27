interface BackgroundPatternProps {
  variant?: "grid" | "dots" | "lines";
  position?: "top-left" | "top-right" | "bottom-left" | "bottom-right" | "center";
  intensity?: "light" | "medium" | "heavy";
}

export function BackgroundPattern({
  variant = "grid",
  position = "top-left",
  intensity = "light",
}: BackgroundPatternProps) {
  const getPositionStyle = () => {
    switch (position) {
      case "top-right":
        return `radial-gradient(ellipse 80% 80% at 100% 0%, #000 50%, transparent 90%)`;
      case "bottom-left":
        return `radial-gradient(ellipse 80% 80% at 0% 100%, #000 50%, transparent 90%)`;
      case "bottom-right":
        return `radial-gradient(ellipse 80% 80% at 100% 100%, #000 50%, transparent 90%)`;
      case "center":
        return `radial-gradient(ellipse 60% 60% at 50% 50%, #000 50%, transparent 90%)`;
      default:
        return `radial-gradient(ellipse 80% 80% at 0% 0%, #000 50%, transparent 90%)`;
    }
  };

  const getIntensityColor = () => {
    switch (intensity) {
      case "medium":
        return "#a1a1a1";
      case "heavy":
        return "#525252";
      default:
        return "#e7e5e4";
    }
  };

  const getBackgroundImage = () => {
    const color = getIntensityColor();

    if (variant === "dots") {
      return `radial-gradient(circle, ${color} 1px, transparent 1px)`;
    }

    if (variant === "lines") {
      return `
        linear-gradient(to right, ${color} 1px, transparent 1px),
        linear-gradient(to bottom, ${color} 1px, transparent 1px)
      `;
    }

    // grid with dashes (default)
    return `
      linear-gradient(to right, ${color} 1px, transparent 1px),
      linear-gradient(to bottom, ${color} 1px, transparent 1px)
    `;
  };

  return (
    <div
      className="absolute inset-0 z-0 pointer-events-none"
      style={{
        opacity: 0.25, // 👈 try 0.15–0.3
        backgroundImage: getBackgroundImage(),
        backgroundSize: variant === "dots" ? "40px 40px" : "20px 20px",
        backgroundPosition: "0 0",
        maskImage: `
          repeating-linear-gradient(
            to right,
            black 0px,
            black 3px,
            transparent 3px,
            transparent 8px
          ),
          repeating-linear-gradient(
            to bottom,
            black 0px,
            black 3px,
            transparent 3px,
            transparent 8px
          ),
          ${getPositionStyle()}
        `,
        WebkitMaskImage: `
          repeating-linear-gradient(
            to right,
            black 0px,
            black 3px,
            transparent 3px,
            transparent 8px
          ),
          repeating-linear-gradient(
            to bottom,
            black 0px,
            black 3px,
            transparent 3px,
            transparent 8px
          ),
          ${getPositionStyle()}
        `,
        maskComposite: "intersect",
        WebkitMaskComposite: "source-in",
      }}
    />
  );
}
