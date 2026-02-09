export const revalidate = 3600;

type GithubAsset = {
  name: string;
  browser_download_url: string;
  download_count: number;
};

type GithubRelease = {
  assets: GithubAsset[];
};

function buildHeaders() {
  const headers: Record<string, string> = {
    Accept: "application/vnd.github+json",
    "User-Agent": "VidGrab-DownloadCounter",
  };
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  return headers;
}

async function fetchAllReleases(): Promise<GithubRelease[]> {
  const releases: GithubRelease[] = [];
  let page = 1;

  while (page < 20) {
    const url = `https://api.github.com/repos/ellaboevans/vidgrab/releases?per_page=100&page=${page}`;
    const res = await fetch(url, { headers: buildHeaders() });
    if (!res.ok) break;
    const data = (await res.json()) as GithubRelease[];
    releases.push(...data);
    if (data.length < 100) break;
    page += 1;
  }

  return releases;
}

export async function GET() {
  try {
    const [latestRes, releases] = await Promise.all([
      fetch(
        "https://api.github.com/repos/ellaboevans/vidgrab/releases/latest",
        {
          headers: buildHeaders(),
        },
      ),
      fetchAllReleases(),
    ]);

    if (!latestRes.ok) {
      const text = await latestRes.text();
      return Response.json(
        {
          error: "Failed to fetch latest release",
          status: latestRes.status,
          detail: text,
        },
        { status: 500 },
      );
    }

    const latest = (await latestRes.json()) as GithubRelease;
    const totals: Record<string, number> = {};
    for (const rel of releases) {
      for (const asset of rel.assets || []) {
        totals[asset.name] = (totals[asset.name] || 0) + asset.download_count;
      }
    }

    // Legacy macOS asset name; merge into both arch-specific names
    const legacyMac = totals["VidGrab.dmg"] || 0;
    if (legacyMac > 0) {
      totals["VidGrab-arm64.dmg"] =
        (totals["VidGrab-arm64.dmg"] || 0) + legacyMac;
      totals["VidGrab-intel.dmg"] =
        (totals["VidGrab-intel.dmg"] || 0) + legacyMac;
    }

    const latestAssets: Record<
      string,
      { url: string; download_count: number }
    > = {};
    for (const asset of latest.assets || []) {
      latestAssets[asset.name] = {
        url: asset.browser_download_url,
        download_count: asset.download_count,
      };
    }

    return Response.json({
      totals,
      latestAssets,
    });
  } catch (error) {
    return Response.json(
      { error: "Failed to fetch download counts" },
      { status: 500 },
    );
  }
}
