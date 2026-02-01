"use client";

import { useEffect, useState } from "react";
import { RiGithubFill, RiStarFill } from "@remixicon/react";

interface GitHubRepoData {
  stargazers_count: number;
}

export function GitHubButton() {
  const [stars, setStars] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStars = async () => {
      try {
        const response = await fetch(
          "https://api.github.com/repos/ellaboevans/vidgrab",
          {
            headers: {
              Accept: "application/vnd.github.v3+json",
            },
            next: { revalidate: 3600 }, // Cache for 1 hour
          },
        );

        if (response.ok) {
          const data: GitHubRepoData = await response.json();
          setStars(data.stargazers_count);
        }
      } catch (error) {
        console.error("Failed to fetch GitHub stars:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStars();
  }, []);

  const formatStars = (count: number): string => {
    if (count >= 1000) {
      return (count / 1000).toFixed(1).replace(/\.0$/, "") + "k";
    }
    return count.toString();
  };

  return (
    <a
      href="https://github.com/ellaboevans/vidgrab"
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-2 px-2 md:px-3 py-2 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary text-xs md:text-sm font-medium transition-colors border border-primary/20">
      <RiGithubFill className="w-5 h-5" />
      <span>Star</span>
      {!loading && stars !== null && (
        <div className="flex items-center gap-1 ml-1 pl-1 border-l border-primary/30">
          <RiStarFill className="w-3.5 h-3.5 fill-current" />
          <span>{formatStars(stars)}</span>
        </div>
      )}
    </a>
  );
}
