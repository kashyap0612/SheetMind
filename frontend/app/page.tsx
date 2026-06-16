import Link from "next/link";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";

export default function Home() {
  return <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,#312e81,transparent_35%),#020617]">
    <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
      <div className="text-xl font-black tracking-tight">SheetMind</div>
      <div className="flex items-center gap-4"><SignedOut><SignInButton mode="modal"><Button>Google sign in</Button></SignInButton></SignedOut><SignedIn><Link href="/dashboard" className="text-sm text-slate-200">Dashboard</Link><UserButton /></SignedIn></div>
    </nav>
    <section className="mx-auto grid max-w-7xl gap-10 px-6 py-20 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
      <div><p className="mb-4 inline-flex rounded-full border border-white/10 px-3 py-1 text-sm text-indigo-200">Bring your own OpenAI, Gemini, or Anthropic key</p><h1 className="text-5xl font-black tracking-tight md:text-7xl">Ask your spreadsheets anything.</h1><p className="mt-6 max-w-2xl text-lg text-slate-300">Upload CSV or XLSX files, inspect metadata, run safe structured analytics actions, and get plain-English answers with execution plans.</p><div className="mt-8"><Link href="/dashboard"><Button className="px-6 py-3">Start analyzing</Button></Link></div></div>
      <div className="card p-6"><div className="mb-4 text-sm text-slate-400">Example prompt</div><div className="rounded-xl bg-slate-900 p-4">Average package for CSE students</div><div className="mt-6 space-y-3 text-sm"><div className="rounded-xl border border-emerald-400/20 bg-emerald-400/10 p-4"><b>Answer:</b> Average package is 18.4 LPA</div><ol className="list-decimal space-y-2 pl-5 text-slate-300"><li>Filter Branch=CSE</li><li>Aggregate Package</li><li>Compute mean</li></ol></div></div>
    </section>
  </main>;
}
