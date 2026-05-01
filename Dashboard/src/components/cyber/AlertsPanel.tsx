import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";
import { AlertTriangle, MapPin } from "lucide-react";
import { Panel, PanelHeader } from "./Card";
import type { Alert, Severity } from "@/data/mock";

const sevColor = {
  critical: "text-cyber-red border-cyber-red/40 bg-cyber-red/10",
  high: "text-cyber-amber border-cyber-amber/40 bg-cyber-amber/10",
  medium: "text-cyber-cyan border-cyber-cyan/40 bg-cyber-cyan/10",
  low: "text-cyber-green border-cyber-green/40 bg-cyber-green/10",
} as const;

export function AlertsPanel() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/alerts/recent?limit=30`);
        if (!res.ok) throw new Error('Network response was not ok');
        const json = await res.json();
        if (json.alerts) {
          const formattedAlerts = json.alerts.map((a: any, i: number) => {
            const attackType = a.attack_type || "ML-Anomaly";
            const severity: Severity = attackType === 'DDoS' || attackType === 'SQL Injection' || attackType === 'ML-Anomaly' ? 'critical' : attackType === 'Brute Force' ? 'high' : 'medium';
            return {
              id: a.id?.toString() || `${i}-${a.timestamp}`,
              time: a.timestamp?.split(' ')[1] || a.timestamp || "now",
              type: attackType,
              source: a.source_ip || "API input",
              country: 'Unknown',
              city: 'Unknown',
              severity,
              signature: a.message || "Prediction alert",
            };
          });
          setAlerts(formattedAlerts);
        }
        setError(null);
      } catch (error: any) {
        console.error("Failed to fetch alerts:", error);
        setError("Disconnected from alert stream");
      } finally {
        setIsLoading(false);
      }
    };

    fetchAlerts();
    const id = setInterval(fetchAlerts, 2400);
    return () => clearInterval(id);
  }, []);

  return (
    <Panel className="flex flex-col h-full relative" glow="red">
      <PanelHeader
        accent="LIVE FEED"
        title="Threat Alerts"
        subtitle="Real-time incident stream"
        right={
          <div className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-cyber-red/10 border border-cyber-red/30">
            <span className="h-1.5 w-1.5 rounded-full bg-cyber-red pulse-ring-red" />
            <span className="text-[10px] font-mono text-cyber-red">REC</span>
          </div>
        }
      />
      <div className="px-3 pb-3 flex-1 overflow-y-auto max-h-[420px] space-y-2 relative">
        {isLoading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/50 backdrop-blur-sm">
            <div className="h-6 w-6 border-2 border-cyber-red border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
        {error && !isLoading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/50 backdrop-blur-sm">
            <p className="text-cyber-red text-sm font-mono bg-cyber-red/10 px-3 py-1 rounded border border-cyber-red/30">{error}</p>
          </div>
        )}
        <AnimatePresence initial={false}>
          {alerts.length === 0 && !isLoading && !error && (
            <div className="h-32 grid place-items-center text-center text-muted-foreground text-sm">
              No alerts yet. Submit an attack prediction to populate the live feed.
            </div>
          )}
          {alerts.map((a) => (
            <motion.div
              key={a.id}
              layout
              initial={{ opacity: 0, x: -16, scale: 0.98 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 16 }}
              transition={{ type: "spring", stiffness: 260, damping: 24 }}
              className={`relative rounded-xl border px-3 py-2.5 ${
                a.severity === "critical"
                  ? "border-cyber-red/40 bg-cyber-red/5 glow-red"
                  : "border-white/10 bg-white/[0.03] hover:border-cyber-cyan/30"
              } transition-colors`}
            >
              <div className="flex items-start gap-2.5">
                <div className={`h-7 w-7 shrink-0 rounded-md border grid place-items-center ${sevColor[a.severity]}`}>
                  <AlertTriangle className="h-3.5 w-3.5" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-baseline justify-between gap-2">
                    <p className="text-sm font-semibold truncate">{a.type}</p>
                    <span className="text-[10px] font-mono text-muted-foreground shrink-0">{a.time}</span>
                  </div>
                  <p className="text-xs text-muted-foreground font-mono truncate">
                    {a.source} · {a.signature}
                  </p>
                  <div className="flex items-center gap-1 mt-1 text-[11px] text-muted-foreground">
                    <MapPin className="h-3 w-3" />
                    <span>{a.city}, {a.country}</span>
                    <span className={`ml-auto px-1.5 py-0.5 rounded text-[9px] uppercase font-bold tracking-wider border ${sevColor[a.severity]}`}>
                      {a.severity}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </Panel>
  );
}
