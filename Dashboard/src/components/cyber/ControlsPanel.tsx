import { useState } from "react";
import { motion } from "framer-motion";
import { Panel, PanelHeader } from "./Card";
import { Sliders } from "lucide-react";

const modes = ["Alpha", "Beta", "Hybrid"] as const;

export function ControlsPanel() {
  const [threshold, setThreshold] = useState(72);
  const [speed, setSpeed] = useState(1.0);
  const [mode, setMode] = useState<typeof modes[number]>("Hybrid");
  const [autoBlock, setAutoBlock] = useState(true);
  const [verbose, setVerbose] = useState(false);

  return (
    <Panel className="p-0">
      <PanelHeader
        accent="ENGINE CONFIG"
        title="System Controls"
        subtitle="Tune detection sensitivity"
        right={<Sliders className="h-4 w-4 text-cyber-cyan" />}
      />
      <div className="px-5 pb-5 space-y-5">
        {/* Threshold */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs uppercase tracking-widest font-mono text-muted-foreground">Attack Threshold</label>
            <span className="text-sm font-mono text-cyber-cyan text-glow-cyan">{threshold}%</span>
          </div>
          <div className="relative h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-cyber-cyan to-cyber-violet glow-cyan"
              style={{ width: `${threshold}%` }}
            />
            <input
              type="range" min={0} max={100} value={threshold}
              onChange={(e) => setThreshold(+e.target.value)}
              className="absolute inset-0 w-full opacity-0 cursor-pointer"
            />
            <div
              className="absolute top-1/2 -translate-y-1/2 h-4 w-4 rounded-full bg-cyber-cyan border-2 border-background pointer-events-none"
              style={{ left: `calc(${threshold}% - 8px)`, boxShadow: "0 0 14px oklch(0.85 0.18 200 / 0.9)" }}
            />
          </div>
        </div>

        {/* Replay speed */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs uppercase tracking-widest font-mono text-muted-foreground">Replay Speed</label>
            <span className="text-sm font-mono text-cyber-green">{speed.toFixed(1)}x</span>
          </div>
          <div className="relative h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-cyber-green to-cyber-cyan glow-green"
              style={{ width: `${(speed / 4) * 100}%` }}
            />
            <input
              type="range" min={0.25} max={4} step={0.25} value={speed}
              onChange={(e) => setSpeed(+e.target.value)}
              className="absolute inset-0 w-full opacity-0 cursor-pointer"
            />
            <div
              className="absolute top-1/2 -translate-y-1/2 h-4 w-4 rounded-full bg-cyber-green border-2 border-background pointer-events-none"
              style={{ left: `calc(${(speed / 4) * 100}% - 8px)`, boxShadow: "0 0 14px oklch(0.82 0.22 150 / 0.9)" }}
            />
          </div>
        </div>

        {/* Mode segmented */}
        <div>
          <label className="text-xs uppercase tracking-widest font-mono text-muted-foreground mb-2 block">Detection Mode</label>
          <div className="relative grid grid-cols-3 gap-1 p-1 rounded-lg bg-white/[0.04] border border-white/10">
            {modes.map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className="relative py-2 text-xs font-mono uppercase tracking-wider transition"
              >
                {mode === m && (
                  <motion.span
                    layoutId="mode-pill"
                    className="absolute inset-0 rounded-md bg-gradient-to-br from-cyber-cyan/30 to-cyber-violet/20 border border-cyber-cyan/50 glow-cyan"
                  />
                )}
                <span className={`relative ${mode === m ? "text-cyber-cyan" : "text-muted-foreground"}`}>{m}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Toggles */}
        <div className="space-y-2">
          <Toggle label="Auto-block malicious IPs" value={autoBlock} onChange={setAutoBlock} accent="green" />
          <Toggle label="Verbose logging" value={verbose} onChange={setVerbose} accent="cyan" />
        </div>
      </div>
    </Panel>
  );
}

function Toggle({
  label, value, onChange, accent,
}: { label: string; value: boolean; onChange: (v: boolean) => void; accent: "green" | "cyan" }) {
  return (
    <button
      onClick={() => onChange(!value)}
      className="w-full flex items-center justify-between rounded-lg border border-white/10 bg-white/[0.03] px-3 py-2.5 hover:border-cyber-cyan/30 transition"
    >
      <span className="text-sm">{label}</span>
      <span className={`relative h-5 w-9 rounded-full transition ${value ? (accent === "green" ? "bg-cyber-green/40" : "bg-cyber-cyan/40") : "bg-white/10"}`}>
        <motion.span
          layout
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
          className={`absolute top-0.5 h-4 w-4 rounded-full ${value ? (accent === "green" ? "bg-cyber-green glow-green" : "bg-cyber-cyan glow-cyan") : "bg-white/70"}`}
          style={{ left: value ? "calc(100% - 18px)" : "2px" }}
        />
      </span>
    </button>
  );
}
