import Link from "next/link";
import { UserButton } from "@clerk/nextjs";

export function AppShell({ children }: { children: React.ReactNode }) {
  return <div className="min-h-screen bg-slate-950"><header className="flex h-16 items-center justify-between border-b border-white/10 px-6"><Link href="/dashboard" className="text-lg font-black">SheetMind</Link><nav className="flex items-center gap-5 text-sm text-slate-300"><Link href="/dashboard">Dashboard</Link><Link href="/settings">Settings</Link><Link href="/profile">Profile</Link><UserButton /></nav></header>{children}</div>;
}
