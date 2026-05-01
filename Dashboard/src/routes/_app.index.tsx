import { Link, createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Activity, ShieldAlert, ShieldCheck, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/cyber/StatCard";
import { AlertsPanel } from "@/components/cyber/AlertsPanel";
import { TrafficChart } from "@/components/cyber/TrafficChart";
import { GeoPanel } from "@/components/cyber/GeoPanel";
import { ControlsPanel } from "@/components/cyber/ControlsPanel";

export const Route = createFileRoute("/_app/")({
  head: () => ({
    meta: [
      { title: "SOC Console — SENTINEL IDS" },
      { name: "description", content: "Live SOC console: real-time intrusion detection, geo intel, threat alerts." },
    ],
  }),
  component: HomePage,
});

function HomePage() {
  const [stats, setStats] = useState({
    total_packets: 0,
    attacks_detected: 0,
    normal_traffic: 0,
    latency: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/live-stats`);
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        setStats(prev => ({
          ...prev,
          total_packets: data.total_packets || prev.total_packets,
          attacks_detected: data.attacks_detected || prev.attacks_detected,
          normal_traffic: data.normal_traffic || prev.normal_traffic,
          latency: data.latency ?? prev.latency
        }));
      } catch (error) {
        console.error("Failed to fetch live stats:", error);
      }
    };

    fetchStats();
    const id = setInterval(fetchStats, 5000);
    return () => clearInterval(id);
  }, []);

  const launchConsole = () => {
    document.getElementById("live-console")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="space-y-6 mt-4">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-3xl glass-strong p-8 md:p-12">
        <div className="absolute inset-0 grid-bg opacity-30" />
        <div className="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-cyber-cyan/20 blur-3xl" />
        <div className="absolute -bottom-24 -left-20 w-80 h-80 rounded-full bg-cyber-violet/20 blur-3xl" />

        <div className="relative">
          <motion.div
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 rounded-full border border-cyber-cyan/30 bg-cyber-cyan/5 px-3 py-1 mb-5"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-cyber-green pulse-ring" />
            <span className="text-[11px] font-mono uppercase tracking-[0.25em] text-cyber-cyan">Threat Engine · Online</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="font-display text-3xl md:text-5xl lg:text-6xl font-bold leading-[1.05] tracking-tight max-w-4xl"
          >
            <span className="gradient-text text-glow-cyan">Real-Time Intrusion</span>
            <br />
            <span className="text-foreground">Detection System</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}
            className="mt-5 max-w-2xl text-sm md:text-base text-muted-foreground"
          >
            Analyzing submitted network-flow features with a hybrid Random Forest and Isolation Forest pipeline.
            New predictions are stored as events and reflected in the live dashboard.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}
            className="mt-7 flex flex-wrap gap-3"
          >
            <button
              onClick={launchConsole}
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyber-cyan to-cyber-blue px-5 py-2.5 text-sm font-semibold text-background glow-cyan hover:opacity-95 transition"
            >
              <Zap className="h-4 w-4" /> Launch Live Console
            </button>
            <Link
              to="/analytics"
              className="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-5 py-2.5 text-sm font-semibold hover:border-cyber-cyan/40 transition"
            >
              View Threat Report
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Traffic" value={stats.total_packets} suffix="pkt" icon={Activity} accent="cyan" delta="▲ Live" />
        <StatCard label="Attacks Detected" value={stats.attacks_detected} icon={ShieldAlert} accent="red" delta="▲ Live stream" />
        <StatCard label="Normal Packets" value={stats.normal_traffic} icon={ShieldCheck} accent="green" delta={`${((stats.normal_traffic / Math.max(1, stats.total_packets)) * 100).toFixed(2)}% clean`} />
        <StatCard label="Avg Latency" value={stats.latency} suffix="ms" icon={Zap} accent="violet" delta="◀ stable" />
      </section>

      {/* Main grid */}
      <section id="live-console" className="grid grid-cols-1 lg:grid-cols-3 gap-4 scroll-mt-24">
        <div className="lg:col-span-2 space-y-4">
          <TrafficChart />
          <GeoPanel />
        </div>
        <div className="space-y-4">
          <AlertsPanel />
          <ControlsPanel />
        </div>
      </section>
    </div>
  );
}
