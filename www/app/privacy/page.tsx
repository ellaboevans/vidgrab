import { TopNav } from "@/components/top-nav";
import { PrivacyContent } from "@/components/privacy-content";
import { Footer } from "@/components/footer";

export const metadata = {
  title: "Privacy Policy - VidGrab",
  description:
    "VidGrab's privacy policy. We don't track you, collect data, or see your downloads. Your privacy is paramount.",
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
