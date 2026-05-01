import { motion } from "framer-motion";
import { Panel, PanelHeader } from "./Card";
import { Globe2 } from "lucide-react";

const sources = [
  { country: "China", city: "Beijing", count: 1284, x: 78, y: 38 },
  { country: "Russia", city: "Moscow", count: 942, x: 58, y: 28 },
  { country: "USA", city: "Ashburn", count: 631, x: 25, y: 40 },
  { country: "Brazil", city: "São Paulo", count: 412, x: 33, y: 68 },
  { country: "India", city: "Mumbai", count: 388, x: 68, y: 50 },
  { country: "Germany", city: "Frankfurt", count: 271, x: 51, y: 32 },
];

export function GeoPanel() {
  return (
    <Panel className="p-0">
      <PanelHeader
        accent="GEO INTEL"
        title="Threat Origin Map"
        subtitle="Top attacker geolocations"
        right={<Globe2 className="h-4 w-4 text-cyber-cyan" />}
      />
      <div className="px-5 pb-5">
        <div className="relative aspect-[2/1] rounded-xl border border-cyber-cyan/15 bg-gradient-to-br from-cyber-blue/10 to-cyber-violet/5 overflow-hidden grid-bg">
          <div className="absolute inset-0" style={{
            background: "radial-gradient(ellipse at center, transparent 30%, oklch(0.14 0.03 260 / 0.7) 100%)"
          }} />
          {/* World blob hint */}
          <svg viewBox="0 0 100 50" className="absolute inset-0 w-full h-full opacity-20" preserveAspectRatio="none">
            <path d="M5,30 Q15,20 25,28 T45,30 Q55,18 70,25 T95,30 L95,40 Q80,45 60,38 T30,42 Q15,40 5,38 Z" fill="oklch(0.85 0.18 200)" />
          </svg>

          {sources.map((s, i) => (
            <motion.div
              key={s.country}
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.1 + i * 0.08, type: "spring", stiffness: 200 }}
              className="absolute -translate-x-1/2 -translate-y-1/2 group"
              style={{ left: `${s.x}%`, top: `${s.y}%` }}
            >
              <span className="absolute inset-0 rounded-full bg-cyber-red/40 animate-ping" style={{ animationDuration: "2.5s" }} />
              <span className="relative block h-3 w-3 rounded-full bg-cyber-red shadow-[0_0_12px_2px_oklch(0.68_0.25_22/0.8)]" />
              <div className="absolute left-4 top-1/2 -translate-y-1/2 whitespace-nowrap opacity-0 group-hover:opacity-100 transition pointer-events-none">
                <div className="glass rounded-md px-2 py-1 text-[10px] font-mono">
                  {s.city} · <span className="text-cyber-red">{s.count}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-2">
          {sources.slice(0, 6).map((s) => (
            <div key={s.country} className="flex items-center justify-between rounded-lg bg-white/[0.03] border border-white/5 px-2.5 py-1.5">
              <div className="min-w-0">
                <p className="text-xs font-medium truncate">{s.country}</p>
                <p className="text-[10px] text-muted-foreground font-mono truncate">{s.city}</p>
              </div>
              <span className="text-[11px] font-mono text-cyber-red">{s.count}</span>
            </div>
          ))}
        </div>
      </div>
    </Panel>
  );
}
