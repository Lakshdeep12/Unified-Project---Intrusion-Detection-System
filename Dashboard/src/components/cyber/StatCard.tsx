import { Panel } from "./Card";
import { Counter } from "./Counter";
import type { LucideIcon } from "lucide-react";

export function StatCard({
  label, value, suffix, icon: Icon, accent = "cyan", delta,
}: {
  label: string; value: number; suffix?: string;
  icon: LucideIcon; accent?: "cyan" | "green" | "red" | "violet";
  delta?: string;
}) {
  const accentMap = {
    cyan: "text-cyber-cyan border-cyber-cyan/30 from-cyber-cyan/20",
    green: "text-cyber-green border-cyber-green/30 from-cyber-green/20",
    red: "text-cyber-red border-cyber-red/30 from-cyber-red/20",
    violet: "text-cyber-violet border-cyber-violet/30 from-cyber-violet/20",
  } as const;
  const cls = accentMap[accent];

  return (
    <Panel glow={accent === "red" ? "red" : accent === "green" ? "green" : "cyan"} className="p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground font-mono">{label}</p>
          <p className="mt-2 font-display text-3xl font-bold tabular-nums">
            <Counter value={value} />
            {suffix && <span className="text-base font-mono text-muted-foreground ml-1">{suffix}</span>}
          </p>
          {delta && <p className={`mt-1 text-xs font-mono ${cls.split(" ")[0]}`}>{delta}</p>}
        </div>
        <div className={`h-11 w-11 rounded-xl border bg-gradient-to-br to-transparent grid place-items-center ${cls}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className="mt-4 h-1 w-full rounded-full bg-white/5 overflow-hidden">
        <div className={`h-full rounded-full bg-gradient-to-r ${cls} to-transparent shimmer`} style={{ width: "70%" }} />
      </div>
    </Panel>
  );
}
