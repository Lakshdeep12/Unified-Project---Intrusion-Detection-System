import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Search, ShieldAlert } from "lucide-react";
import { Panel, PanelHeader } from "@/components/cyber/Card";
import { ControlsPanel } from "@/components/cyber/ControlsPanel";
import type { Alert, Severity } from "@/data/mock";

export const Route = createFileRoute("/_app/tools")({
  head: () => ({
    meta: [
      { title: "Tools & Logs — SENTINEL IDS" },
      { name: "description", content: "Operator tools: full event log, search and engine controls." },
    ],
  }),
  component: ToolsPage,
});

const sevColor = {
  critical: "text-cyber-red bg-cyber-red/10 border-cyber-red/40",
  high: "text-cyber-amber bg-cyber-amber/10 border-cyber-amber/40",
  medium: "text-cyber-cyan bg-cyber-cyan/10 border-cyber-cyan/40",
  low: "text-cyber-green bg-cyber-green/10 border-cyber-green/40",
} as const;

function ToolsPage() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [allLogs, setAllLogs] = useState<Alert[]>([]);
  const perPage = 10;

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get("query");
    if (query) setQ(query);

    const fetchLogs = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
        const res = await fetch(`${baseUrl}/logs?page=1&limit=100`);
        if (!res.ok) return;
        const data = await res.json();
        const rows: Alert[] = (data.logs || []).map((row: any) => {
          const isAttack = row.is_attack === 1;
          const severity: Severity = isAttack ? "critical" : "low";
          return {
            id: String(row.id),
            time: row.timestamp?.split(" ")[1] || row.timestamp || "",
            type: row.prediction || "UNKNOWN",
            source: row.source_ip || "API input",
            country: "Unknown",
            city: "Unknown",
            severity,
            signature: isAttack ? "ML anomaly" : "Model event",
          };
        });
        setAllLogs(rows);
      } catch (error) {
        console.error("Failed to fetch event logs", error);
      }
    };

    fetchLogs();
    const id = setInterval(fetchLogs, 5000);
    return () => clearInterval(id);
  }, []);

  const filtered = useMemo(
    () =>
      allLogs.filter((l) =>
        [l.type, l.source, l.country, l.city, l.signature].join(" ").toLowerCase().includes(q.toLowerCase()),
      ),
    [q],
  );
  const pages = Math.max(1, Math.ceil(filtered.length / perPage));
  const view = filtered.slice((page - 1) * perPage, page * perPage);

  return (
    <div className="space-y-6 mt-4">
      <header>
        <p className="text-[11px] font-mono uppercase tracking-[0.3em] text-cyber-cyan">OPERATOR CONSOLE</p>
        <h1 className="font-display text-3xl md:text-4xl font-bold mt-1 gradient-text">Tools & Event Log</h1>
        <p className="text-sm text-muted-foreground mt-1">Forensic-grade log access with engine-level controls.</p>
      </header>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <Panel className="p-0">
            <PanelHeader
              accent="EVENT LOG"
              title="Detected Events"
              subtitle={`${filtered.length} records`}
              right={
                <div className="relative">
                  <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                  <input
                    placeholder="filter…"
                    value={q}
                    onChange={(e) => { setQ(e.target.value); setPage(1); }}
                    className="bg-white/5 border border-white/10 rounded-md pl-7 pr-2 py-1.5 text-xs font-mono w-44 focus:outline-none focus:border-cyber-cyan/50"
                  />
                </div>
              }
            />
            <div className="px-3 pb-3 overflow-x-auto">
              <table className="w-full text-sm border-separate border-spacing-y-1">
                <thead>
                  <tr className="text-[10px] uppercase tracking-widest text-muted-foreground font-mono">
                    <th className="text-left px-3 py-2">Time</th>
                    <th className="text-left px-3 py-2">Type</th>
                    <th className="text-left px-3 py-2">Source IP</th>
                    <th className="text-left px-3 py-2">Geo</th>
                    <th className="text-left px-3 py-2">Sig</th>
                    <th className="text-left px-3 py-2">Severity</th>
                  </tr>
                </thead>
                <tbody>
                  {view.map((l, i) => (
                    <motion.tr
                      key={l.id + i}
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.025 }}
                      className={`group ${l.severity === "critical" ? "bg-cyber-red/5" : "bg-white/[0.02]"} hover:bg-cyber-cyan/5 transition`}
                    >
                      <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground rounded-l-lg border-l border-y border-white/5">{l.time}</td>
                      <td className="px-3 py-2.5 border-y border-white/5">
                        <span className="flex items-center gap-2">
                          {l.severity === "critical" && <ShieldAlert className="h-3.5 w-3.5 text-cyber-red" />}
                          <span className={l.severity === "critical" ? "text-cyber-red font-semibold" : ""}>{l.type}</span>
                        </span>
                      </td>
                      <td className="px-3 py-2.5 font-mono text-xs border-y border-white/5">{l.source}</td>
                      <td className="px-3 py-2.5 text-xs border-y border-white/5">{l.city}, {l.country}</td>
                      <td className="px-3 py-2.5 font-mono text-[11px] text-muted-foreground border-y border-white/5">{l.signature}</td>
                      <td className="px-3 py-2.5 rounded-r-lg border-r border-y border-white/5">
                        <span className={`text-[10px] uppercase font-mono font-bold tracking-wider px-2 py-0.5 rounded border ${sevColor[l.severity]}`}>
                          {l.severity}
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                  {view.length === 0 && (
                    <tr><td colSpan={6} className="text-center py-10 text-muted-foreground text-sm">No stored events yet. Run `/api/predict` to create real records.</td></tr>
                  )}
                </tbody>
              </table>

              <div className="flex items-center justify-between mt-3 px-2">
                <p className="text-[11px] font-mono text-muted-foreground">
                  Page {page} / {pages}
                </p>
                <div className="flex gap-1">
                  <button
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="h-8 w-8 grid place-items-center rounded-md border border-white/10 bg-white/5 hover:border-cyber-cyan/40 transition disabled:opacity-40"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setPage((p) => Math.min(pages, p + 1))}
                    disabled={page === pages}
                    className="h-8 w-8 grid place-items-center rounded-md border border-white/10 bg-white/5 hover:border-cyber-cyan/40 transition disabled:opacity-40"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </Panel>
        </div>

        <ControlsPanel />
      </section>
    </div>
  );
}
