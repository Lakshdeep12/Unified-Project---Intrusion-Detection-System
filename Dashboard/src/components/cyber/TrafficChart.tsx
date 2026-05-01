import { useEffect, useState } from "react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Panel, PanelHeader } from "./Card";

const emptyTraffic = Array.from({ length: 60 }, (_, i) => ({
  t: i,
  attacks: 0,
  normal: 0,
}));

export function TrafficChart() {
  const [data, setData] = useState(emptyTraffic);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/attack-rate`);
        if (!res.ok) throw new Error('Network response was not ok');
        const json = await res.json();
        if (json.history && json.history.length > 0) {
          setData(json.history.map((d: any, i: number) => ({
            t: i,
            attacks: d.attacks,
            normal: d.normal || 0
          })));
        }
        setError(null);
      } catch (error: any) {
        console.error("Failed to fetch attack rate:", error);
        setError("Failed to connect to threat stream");
      } finally {
        setIsLoading(false);
      }
    };

    fetchData(); // Initial fetch
    const id = setInterval(fetchData, 1500);
    return () => clearInterval(id);
  }, []);

  return (
    <Panel className="p-0" glow="cyan">
      <PanelHeader
        accent="LAST 60 SECONDS"
        title="Network Traffic / Attacks"
        subtitle="Live packet rate (pkt/s)"
        right={
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-cyber-cyan" />NORMAL</span>
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-cyber-red" />ATTACK</span>
          </div>
        }
      />
      <div className="h-[280px] px-2 pb-3 relative">
        {isLoading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/50 backdrop-blur-sm">
            <div className="h-6 w-6 border-2 border-cyber-cyan border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
        {error && !isLoading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/50 backdrop-blur-sm">
            <p className="text-cyber-red text-sm font-mono bg-cyber-red/10 px-3 py-1 rounded border border-cyber-red/30">{error}</p>
          </div>
        )}
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="g-normal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.85 0.18 200)" stopOpacity={0.45} />
                <stop offset="100%" stopColor="oklch(0.85 0.18 200)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="g-attack" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="oklch(0.68 0.25 22)" stopOpacity={0.55} />
                <stop offset="100%" stopColor="oklch(0.68 0.25 22)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="oklch(0.85 0.18 200 / 0.07)" vertical={false} />
            <XAxis dataKey="t" tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} tickLine={false} axisLine={false} width={32} />
            <Tooltip
              contentStyle={{
                background: "oklch(0.18 0.035 260 / 0.92)",
                border: "1px solid oklch(0.85 0.18 200 / 0.35)",
                borderRadius: 12,
                fontSize: 12,
                fontFamily: "JetBrains Mono",
              }}
              labelStyle={{ color: "oklch(0.85 0.18 200)" }}
            />
            <Area type="monotone" dataKey="normal" stroke="oklch(0.85 0.18 200)" strokeWidth={2} fill="url(#g-normal)" isAnimationActive={false} />
            <Area type="monotone" dataKey="attacks" stroke="oklch(0.68 0.25 22)" strokeWidth={2} fill="url(#g-attack)" isAnimationActive={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Panel>
  );
}
