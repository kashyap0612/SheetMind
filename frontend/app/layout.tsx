import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata: Metadata = { title: "SheetMind", description: "AI spreadsheet analytics for modern teams" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <ClerkProvider><html lang="en"><body>{children}</body></html></ClerkProvider>;
}
