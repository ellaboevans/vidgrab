import { TopNav } from "@/components/top-nav";
import { HeroSection } from "@/components/hero-section";
import { FeaturesSection } from "@/components/features-section";
import { QualityOptions } from "@/components/quality-options";
import { PlatformShowcase } from "@/components/platform-showcase";
import { FAQSection } from "@/components/faq-section";
import { DownloadSection } from "@/components/download-section";
import { Footer } from "@/components/footer";
import { ComingSoonView } from "@/components/coming-soon-view";
import { useComingSoon } from "@/lib/use-coming-soon";

export default function Home() {
  const isComingSoon = useComingSoon();

  if (isComingSoon) {
    return <ComingSoonView />;
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />
      <HeroSection />
      <FeaturesSection />
      <QualityOptions />
      <PlatformShowcase />
      <FAQSection />
      <DownloadSection />
      <Footer />
    </main>
  );
}
