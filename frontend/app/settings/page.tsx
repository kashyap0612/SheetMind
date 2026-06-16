import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const providers = ["OpenAI", "Gemini", "Anthropic"];
export default function SettingsPage() {
  return <AppShell><main className="mx-auto max-w-4xl p-6"><h1 className="text-3xl font-black">API key management</h1><p className="mt-2 text-slate-400">Keys are validated server-side, encrypted with AES-256-GCM, and never returned to the browser.</p><div className="mt-8 space-y-4">{providers.map((provider) => <section key={provider} className="card p-5"><div className="mb-4 flex items-center justify-between"><div><h2 className="font-bold">{provider}</h2><p className="text-sm text-slate-400">Use your own key after free credits are exhausted.</p></div><span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">Not connected</span></div><div className="flex gap-3"><Input placeholder={`${provider} API key`}/><Button>Save</Button><Button className="bg-slate-800 hover:bg-slate-700">Delete</Button></div></section>)}</div></main></AppShell>;
}
