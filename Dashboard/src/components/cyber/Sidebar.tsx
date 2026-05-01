import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Home, BarChart3, Sparkles, Wrench, ShieldCheck } from "lucide-react";

const items = [
  { to: "/", label: "Home", icon: Home },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/features", label: "Features", icon: Sparkles },
  { to: "/tools", label: "Tools", icon: Wrench },
] as const;

export function Sidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <aside className="hidden lg:flex flex-col w-64 shrink-0 h-screen sticky top-0 p-4 z-20">
      <div className="glass rounded-2xl flex-1 flex flex-col p-5">
        <div className="flex items-center gap-3 px-2 py-1">
          <div className="relative">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyber-cyan to-cyber-violet flex items-center justify-center glow-cyan">
              <ShieldCheck className="h-5 w-5 text-background" />
            </div>
            <span className="absolute -top-1 -right-1 h-3 w-3 rounded-full bg-cyber-green pulse-ring" />
          </div>
          <div>
            <p className="font-display font-bold text-lg leading-none tracking-wide">SENTINEL</p>
            <p className="text-[10px] uppercase tracking-[0.2em] text-cyber-cyan/80 mt-1">IDS · v4.2</p>
          </div>
        </div>

        <div className="my-6 h-px bg-gradient-to-r from-transparent via-cyber-cyan/30 to-transparent" />

        <nav className="flex flex-col gap-1.5">
          {items.map((item) => {
            const active = pathname === item.to;
            const Icon = item.icon;
            return (
              <Link key={item.to} to={item.to} className="relative">
                <motion.div
                  whileHover={{ x: 4 }}
                  className={`relative flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                    active
                      ? "text-foreground bg-cyber-cyan/10 border border-cyber-cyan/30"
                      : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                  }`}
                >
                  {active && (
                    <motion.span
                      layoutId="active-pill"
                      className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-0.5 rounded-r bg-cyber-cyan glow-cyan"
                    />
                  )}
                  <Icon className={`h-4 w-4 ${active ? "text-cyber-cyan" : ""}`} />
                  <span>{item.label}</span>
                  {active && <span className="ml-auto text-[10px] font-mono text-cyber-cyan">●</span>}
                </motion.div>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto">
          <div className="rounded-xl border border-cyber-green/20 bg-cyber-green/5 p-3">
            <div className="flex items-center gap-2 mb-2">
              <span className="h-2 w-2 rounded-full bg-cyber-green pulse-ring" />
              <p className="text-xs font-semibold text-cyber-green">All Systems Nominal</p>
            </div>
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              Threat engine online · 12 sensors active
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
