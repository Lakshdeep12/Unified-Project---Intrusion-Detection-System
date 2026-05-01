import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Brain, Eye, Lock, Network, Radar, Workflow, Cpu, Bell } from "lucide-react";
import { Panel } from "@/components/cyber/Card";

export const Route = createFileRoute("/_app/features")({
  head: () => ({
    meta: [
      { title: "Features — SENTINEL IDS" },
      { name: "description", content: "Adaptive ML, deep packet inspection, geo intelligence and more." },
    ],
  }),
  component: FeaturesPage,
});

const features = [
  { icon: Brain, title: "Hybrid ML Engine", desc: "Random Forest classification plus Isolation Forest anomaly detection over flow-level features.", accent: "cyan" },
  { icon: Radar, title: "Prediction API", desc: "FastAPI endpoint validates the 15-feature model contract and stores every prediction event.", accent: "violet" },
  { icon: Eye, title: "Evaluation Reports", desc: "Reproducible scripts benchmark saved model sets against CICIDS2017 samples.", accent: "green" },
  { icon: Network, title: "Live Dashboard", desc: "Stats, alerts and event logs refresh from backend data instead of fixed mock records.", accent: "cyan" },
  { icon: Lock, title: "Authentication", desc: "JWT-based login and registration endpoints secure operator access workflows.", accent: "red" },
  { icon: Workflow, title: "Docker Workflow", desc: "Backend and frontend services can be launched together with Docker Compose.", accent: "violet" },
  { icon: Cpu, title: "Local Capture Mode", desc: "Scapy-based packet capture converts packets into the model feature order when permissions allow.", accent: "green" },
  { icon: Bell, title: "Alert Storage", desc: "Attack predictions generate alert records that are visible in the SOC console.", accent: "cyan" },
] as const;

const accentMap = {
  cyan: "from-cyber-cyan/30 to-cyber-cyan/5 text-cyber-cyan border-cyber-cyan/30",
  violet: "from-cyber-violet/30 to-cyber-violet/5 text-cyber-violet border-cyber-violet/30",
  green: "from-cyber-green/30 to-cyber-green/5 text-cyber-green border-cyber-green/30",
  red: "from-cyber-red/30 to-cyber-red/5 text-cyber-red border-cyber-red/30",
} as const;

function FeaturesPage() {
  return (
    <div className="space-y-8 mt-4">
      <header className="max-w-3xl">
        <p className="text-[11px] font-mono uppercase tracking-[0.3em] text-cyber-cyan">CAPABILITIES</p>
        <h1 className="font-display text-3xl md:text-5xl font-bold mt-2 gradient-text">
          Built for the modern threat landscape
        </h1>
        <p className="text-muted-foreground mt-3">
          Eight pillars that turn raw packets into actionable intelligence — without analyst burnout.
        </p>
      </header>

      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((f, i) => {
          const Icon = f.icon;
          const cls = accentMap[f.accent];
          return (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06, type: "spring", stiffness: 180, damping: 22 }}
            >
              <Panel className="p-5 h-full" glow={f.accent === "red" ? "red" : f.accent === "green" ? "green" : "cyan"}>
                <div className={`inline-flex h-11 w-11 items-center justify-center rounded-xl border bg-gradient-to-br ${cls}`}>
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="font-display font-semibold text-base mt-4">{f.title}</h3>
                <p className="text-xs text-muted-foreground mt-1.5 leading-relaxed">{f.desc}</p>
                <div className="mt-4 h-px bg-gradient-to-r from-transparent via-cyber-cyan/30 to-transparent" />
                <p className="mt-3 text-[10px] font-mono uppercase tracking-widest text-muted-foreground">
                  Module · 0{i + 1}
                </p>
              </Panel>
            </motion.div>
          );
        })}
      </section>
    </div>
  );
}
