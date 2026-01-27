import { TopNav } from "@/components/top-nav";
import { DownloadGrid } from "@/components/download-grid";
import { MacOSInstructions } from "@/components/macos-instructions";
import { Footer } from "@/components/footer";

export const metadata = {
  title: "Download VidGrab - All Platforms",
  description: "Download VidGrab for macOS, Windows, or Linux. Step-by-step installation guides included.",
};

export default function DownloadPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />
      <DownloadGrid />
      <MacOSInstructions />
      <Footer />
    </main>
  );
}
