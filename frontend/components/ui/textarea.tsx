import * as React from "react";
import { cn } from "@/lib/utils";

export function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea {...props} className={cn("w-full rounded-xl border border-white/10 bg-slate-900/80 px-3 py-2 text-sm outline-none ring-brand/40 placeholder:text-slate-500 focus:ring-2", props.className)} />;
}
