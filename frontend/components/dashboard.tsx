"use client";
import { useMemo, useState } from "react";
import { Upload, Search, Send, KeyRound, Database } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

type SheetFile = { id: number; original_filename: string; row_count: number | null; column_count: number | null; sheets: { name: string; columns: { name: string; dtype: string; nullable: boolean }[]; sample_rows: Record<string, unknown>[] }[] };

const demoFiles: SheetFile[] = [{ id: 1, original_filename: "placements.xlsx", row_count: 1240, column_count: 8, sheets: [{ name: "Students", columns: [{ name: "Branch", dtype: "object", nullable: false }, { name: "Package", dtype: "float64", nullable: false }, { name: "Company", dtype: "object", nullable: true }], sample_rows: [] }] }];

export function Dashboard({ files = demoFiles }: { files?: SheetFile[] }) {
  const [selectedId, setSelectedId] = useState(files[0]?.id);
  const [question, setQuestion] = useState("Average package for CSE students");
  const selected = useMemo(() => files.find((file) => file.id === selectedId) ?? files[0], [files, selectedId]);
  const columns = selected?.sheets?.[0]?.columns ?? [];
  return <main className="grid min-h-[calc(100vh-4rem)] grid-cols-1 gap-4 p-4 lg:grid-cols-[280px_minmax(0,1fr)_340px]">
    <aside className="card p-4"><div className="mb-4 flex items-center justify-between"><h2 className="font-semibold">Files</h2><Button className="gap-2"><Upload size={16}/>Upload</Button></div><div className="relative mb-4"><Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500"/><Input className="pl-9" placeholder="Search files"/></div><div className="space-y-2">{files.map((file) => <button key={file.id} onClick={() => setSelectedId(file.id)} className={`w-full rounded-xl border p-3 text-left text-sm ${selected?.id === file.id ? "border-brand bg-brand/15" : "border-white/10 bg-white/5"}`}><div className="font-medium">{file.original_filename}</div><div className="mt-1 text-xs text-slate-400">{file.row_count ?? 0} rows · {file.column_count ?? 0} columns</div></button>)}</div></aside>
    <section className="card flex min-h-[70vh] flex-col p-4"><div className="border-b border-white/10 pb-4"><h1 className="text-xl font-bold">Ask SheetMind</h1><p className="text-sm text-slate-400">Natural-language analytics converted into validated structured actions.</p></div><div className="flex-1 space-y-4 overflow-auto py-6"><div className="ml-auto max-w-xl rounded-2xl bg-brand p-4 text-sm">{question}</div><div className="max-w-2xl rounded-2xl bg-slate-900 p-4 text-sm"><p className="font-semibold text-emerald-300">Average package is 18.4 LPA</p><div className="mt-4 rounded-xl border border-white/10 p-3"><div className="mb-2 text-xs uppercase text-slate-500">Execution plan</div><ol className="list-decimal space-y-1 pl-5 text-slate-300"><li>Filter Branch=CSE</li><li>Aggregate Package</li><li>Compute mean</li></ol></div></div></div><div className="flex gap-3 border-t border-white/10 pt-4"><Textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={2}/><Button className="self-end gap-2"><Send size={16}/>Ask</Button></div></section>
    <aside className="card p-4"><h2 className="mb-4 flex items-center gap-2 font-semibold"><Database size={18}/>Dataset insights</h2><div className="grid grid-cols-2 gap-3"><Metric label="Rows" value={selected?.row_count ?? 0}/><Metric label="Columns" value={selected?.column_count ?? 0}/></div><h3 className="mb-2 mt-6 text-sm font-semibold text-slate-300">Detected columns</h3><div className="space-y-2">{columns.map((column) => <div key={column.name} className="rounded-xl border border-white/10 p-3 text-sm"><div className="font-medium">{column.name}</div><div className="text-xs text-slate-500">{column.dtype}{column.nullable ? " · nullable" : ""}</div></div>)}</div><h3 className="mb-2 mt-6 text-sm font-semibold text-slate-300">Suggested questions</h3><div className="space-y-2 text-sm text-indigo-200"><button>Top 10 packages by branch</button><button>Null analysis for all columns</button><button>Average package by company</button></div><div className="mt-6 rounded-xl border border-amber-400/20 bg-amber-400/10 p-3 text-sm text-amber-100"><KeyRound className="mb-2 h-4 w-4"/>10 free queries included. Add an API key in Settings after quota ends.</div></aside>
  </main>;
}

function Metric({ label, value }: { label: string; value: number }) { return <div className="rounded-xl border border-white/10 bg-white/5 p-3"><div className="text-2xl font-bold">{value}</div><div className="text-xs text-slate-500">{label}</div></div>; }
