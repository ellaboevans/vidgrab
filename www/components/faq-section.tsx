"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { parseLinksInText } from "@/lib/link-parser";
import { highlightQualityOptions } from "@/lib/quality-highlighter";

function formatAnswerText(text: string) {
  const withQuality = highlightQualityOptions(text);

  return withQuality.map((part, index) => {
    if (typeof part === "string") {
      return <span key={`${part}-${index}`}>{parseLinksInText(part)}</span>;
    }
    return part;
  });
}

export function FAQSection() {
  const faqs = [
    {
      id: "faq-1",
      question: "Is VidGrab free?",
      answer:
        "Yes, VidGrab is completely free and open-source. There are no hidden costs, subscriptions, or premium features. Download and use it as much as you want.",
    },
    {
      id: "faq-2",
      question: "What formats does VidGrab support?",
      answer:
        "VidGrab supports MP4, MKV, and WebM formats. You can also download audio-only in various formats. Choose the best format for your needs.",
    },
    {
      id: "faq-3",
      question: "Can I download entire playlists?",
      answer:
        "Yes, VidGrab can download entire playlists, channels, and even custom URLs. Add the playlist URL and it will download all videos automatically.",
    },
    {
      id: "faq-4",
      question: "What quality options are available?",
      answer:
        "VidGrab offers quality presets: best, 1080p, 720p, 480p, and audio-only. Choose based on your internet speed and storage preferences.",
    },
    {
      id: "faq-5",
      question: "Does VidGrab work offline?",
      answer:
        "VidGrab requires an internet connection to download videos from YouTube. However, once downloaded, you can watch them offline anytime.",
    },
    {
      id: "faq-6",
      question: "Is VidGrab legal?",
      answer:
        "VidGrab is a tool for downloading videos. Ensure you have the right to download content and respect copyright laws in your jurisdiction. Personal backups are generally allowed.",
    },
    {
      id: "faq-7",
      question: "Where are my downloads saved?",
      answer:
        "You can choose your download folder in settings. By default, downloads go to your Downloads folder. You can change this anytime.",
    },
    {
      id: "faq-8",
      question: "How do I report bugs or request features?",
      answer:
        "Visit our GitHub repository at github.com/ellaboevans/vidgrab/issues to report issues, request features, or contribute to the project.",
    },
  ];

  return (
    <section className="py-24 px-6 overflow-hidden">
      {/* Background accent */}
      <div className="absolute -top-40 -left-40 w-80 h-80 bg-primary/10 rounded-full filter blur-3xl opacity-20 pointer-events-none" />

      <div className="max-w-3xl mx-auto relative z-10">
        {/* Header */}
        <div className="mb-16 text-center px-4">
          <h2 className="text-4xl sm:text-5xl md:text-6xl font-bold font-mono-display tracking-tight mb-6">
            Frequently Asked Questions
          </h2>
          <p className="text-lg md:text-xl text-foreground/60 max-w-2xl mx-auto">
            Find answers to common questions about VidGrab and how to use it
            effectively.
          </p>
        </div>

        {/* FAQ Accordion */}
        <Accordion type="single" collapsible className="w-full space-y-3">
          {faqs.map((faq) => (
            <AccordionItem
              key={faq.id}
              value={faq.id}
              className="border border-border bg-card/40 rounded-lg px-6 py-2 hover:bg-card/60 transition-colors">
              <AccordionTrigger className="text-left hover:no-underline py-4">
                <span className="text-base md:text-lg font-semibold text-foreground">
                  {faq.question}
                </span>
              </AccordionTrigger>
              <AccordionContent className="text-foreground/80 text-base leading-relaxed pb-4">
                {formatAnswerText(faq.answer)}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>

        {/* Still have questions */}
        <div className="mt-16 text-center">
          <p className="text-foreground/60 mb-4">
            Didn&apos;t find what you&apos;re looking for?
          </p>
          <a
            href="https://github.com/ellaboevans/vidgrab/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-6 py-3 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-lg transition-colors">
            Open an Issue on GitHub
          </a>
        </div>
      </div>
    </section>
  );
}
