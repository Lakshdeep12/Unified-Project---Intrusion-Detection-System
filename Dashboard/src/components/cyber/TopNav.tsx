import { Bell, Search, User, LogOut, Settings, ShieldAlert } from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { clearSession, getUsername } from "@/lib/api";

type AlertItem = {
  id?: number;
  timestamp?: string;
  message?: string;
  attack_type?: string;
  source_ip?: string;
};

export function TopNav() {
  const [time, setTime] = useState(() => new Date());
  const [query, setQuery] = useState("");
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [showAlerts, setShowAlerts] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [username, setUsername] = useState("Operator");

  useEffect(() => {
    setUsername(getUsername());
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
        const res = await fetch(`${baseUrl}/alerts/recent?limit=5`);
        if (!res.ok) return;
        const data = await res.json();
        setAlerts(data.alerts || []);
      } catch (error) {
        console.error("Failed to fetch notifications", error);
      }
    };

    fetchAlerts();
    const id = setInterval(fetchAlerts, 5000);
    return () => clearInterval(id);
  }, []);

  const runSearch = () => {
    const trimmed = query.trim();
    if (!trimmed) return;
    window.location.href = `/tools?query=${encodeURIComponent(trimmed)}`;
  };

  return (
    <header className="sticky top-0 z-30 px-4 lg:pl-0 lg:pr-4 pt-4">
      <div className="glass rounded-2xl px-4 sm:px-6 py-3 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-cyber-green opacity-75 animate-ping" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-cyber-green" />
          </span>
          <span className="text-xs font-mono uppercase tracking-widest text-cyber-green">LIVE</span>
          <span className="hidden sm:inline text-xs text-muted-foreground/70 ml-2 font-mono">
            {time.toISOString().replace("T", " ").slice(0, 19)} UTC
          </span>
        </div>

        <div className="flex-1 hidden md:flex items-center gap-2 max-w-md mx-auto">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") runSearch();
              }}
              placeholder="Search threats, IPs, signatures…"
              className="w-full bg-white/5 border border-white/10 rounded-lg pl-9 pr-3 py-2 text-sm placeholder:text-muted-foreground/60 focus:outline-none focus:border-cyber-cyan/50 focus:bg-white/[0.07] transition"
            />
            <button
              onClick={runSearch}
              className="absolute right-1.5 top-1/2 -translate-y-1/2 rounded-md px-2 py-1 text-[10px] font-mono uppercase text-cyber-cyan hover:bg-cyber-cyan/10"
            >
              Go
            </button>
          </div>
        </div>

        <div className="ml-auto flex items-center gap-2">
          <div className="relative">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setShowAlerts((value) => !value);
                setShowProfile(false);
              }}
              aria-label="Open notifications"
              className="relative h-9 w-9 grid place-items-center rounded-lg bg-white/5 border border-white/10 hover:border-cyber-cyan/40 transition"
            >
              <Bell className="h-4 w-4" />
              {alerts.length > 0 && (
                <span className="absolute -top-1 -right-1 h-4 min-w-4 px-1 rounded-full bg-cyber-red text-[10px] font-bold grid place-items-center text-white pulse-ring-red">
                  {alerts.length}
                </span>
              )}
            </motion.button>

            {showAlerts && (
              <div className="absolute right-0 mt-2 w-80 rounded-xl border border-white/10 bg-background/95 p-3 shadow-2xl backdrop-blur-xl">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-xs font-mono uppercase tracking-widest text-cyber-cyan">Notifications</p>
                  <button
                    onClick={() => { window.location.href = "/tools"; }}
                    className="text-[10px] font-mono text-muted-foreground hover:text-cyber-cyan"
                  >
                    View all
                  </button>
                </div>
                <div className="space-y-2 max-h-72 overflow-y-auto">
                  {alerts.length === 0 && (
                    <p className="rounded-lg border border-white/10 bg-white/[0.03] px-3 py-4 text-center text-sm text-muted-foreground">
                      No alerts yet.
                    </p>
                  )}
                  {alerts.map((alert, index) => (
                    <button
                      key={alert.id ?? index}
                      onClick={() => { window.location.href = "/tools"; }}
                      className="w-full text-left rounded-lg border border-white/10 bg-white/[0.03] px-3 py-2 hover:border-cyber-red/40 transition"
                    >
                      <div className="flex items-start gap-2">
                        <ShieldAlert className="h-4 w-4 mt-0.5 text-cyber-red" />
                        <div className="min-w-0">
                          <p className="text-sm font-semibold truncate">{alert.attack_type || "ML-Anomaly"}</p>
                          <p className="text-xs text-muted-foreground truncate">{alert.message || "Prediction alert"}</p>
                          <p className="text-[10px] font-mono text-muted-foreground mt-1">{alert.timestamp || "Live event"}</p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="relative">
            <button
              onClick={() => {
                setShowProfile((value) => !value);
                setShowAlerts(false);
              }}
              className="h-9 pl-1 pr-3 flex items-center gap-2 rounded-lg bg-white/5 border border-white/10 hover:border-cyber-cyan/40 transition"
            >
              <div className="h-7 w-7 rounded-md bg-gradient-to-br from-cyber-cyan to-cyber-violet grid place-items-center">
                <User className="h-3.5 w-3.5 text-background" />
              </div>
              <div className="hidden sm:block leading-tight text-left">
                <p className="text-xs font-semibold">{username}</p>
                <p className="text-[10px] text-muted-foreground font-mono">SOC · LVL 5</p>
              </div>
            </button>

            {showProfile && (
              <div className="absolute right-0 mt-2 w-56 rounded-xl border border-white/10 bg-background/95 p-2 shadow-2xl backdrop-blur-xl">
                <div className="px-3 py-2 border-b border-white/10 mb-1">
                  <p className="text-sm font-semibold">{username}</p>
                  <p className="text-xs text-muted-foreground font-mono">sentinel.local</p>
                </div>
                <button
                  onClick={() => { window.location.href = "/features"; }}
                  className="w-full flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-white/5 transition"
                >
                  <User className="h-4 w-4 text-cyber-cyan" /> View profile
                </button>
                <button
                  onClick={() => { window.location.href = "/tools"; }}
                  className="w-full flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-white/5 transition"
                >
                  <Settings className="h-4 w-4 text-cyber-green" /> Engine settings
                </button>
                <button
                  onClick={() => {
                    clearSession();
                    window.location.href = "/login";
                  }}
                  className="w-full flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-cyber-red/10 text-cyber-red transition"
                >
                  <LogOut className="h-4 w-4" /> Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
