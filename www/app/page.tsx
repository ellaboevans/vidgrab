import { TopNav } from "@/components/top-nav";
import { HeroSection } from "@/components/hero-section";
import { FeaturesSection } from "@/components/features-section";
import { QualityOptions } from "@/components/quality-options";
import { PlatformShowcase } from "@/components/platform-showcase";
import { DownloadSection } from "@/components/download-section";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />
      <HeroSection />
      <FeaturesSection />
      <QualityOptions />
      <PlatformShowcase />
      <DownloadSection />
      <Footer />
    </main>
  );
}
