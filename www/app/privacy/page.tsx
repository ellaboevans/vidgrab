import { TopNav } from "@/components/top-nav";
import { PrivacyContent } from "@/components/privacy-content";
import { Footer } from "@/components/footer";

export const metadata = {
  title: "Privacy Policy - VidGrab | No Tracking, No Data Collection",
  description:
    "VidGrab's privacy policy. We don't track you, collect data, or see your downloads. Completely open-source and privacy-focused. Your privacy is paramount.",
  keywords: [
    "privacy policy",
    "no tracking",
    "no data collection",
    "open source privacy",
    "VidGrab privacy",
  ],
  openGraph: {
    title: "Privacy Policy - VidGrab",
    description:
      "VidGrab's privacy policy. We don't track you, collect data, or see your downloads.",
    url: `${process.env.NEXT_PUBLIC_SITE_URL as string}/privacy`,
    type: "website",
  },
};

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <TopNav />
      <PrivacyContent />
      <Footer />
    </main>
  );
}
