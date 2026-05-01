import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ShieldCheck } from "lucide-react";
import { FormEvent, useState } from "react";
import { API_BASE, saveSession } from "@/lib/api";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Login - SENTINEL IDS" },
      { name: "description", content: "Operator login for SENTINEL IDS." },
    ],
  }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setMessage("");

    try {
      if (mode === "register") {
        const register = await fetch(`${API_BASE}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        const registerBody = await register.json().catch(() => ({}));
        if (!register.ok) throw new Error(registerBody.detail || "Registration failed");
      }

      const form = new URLSearchParams();
      form.set("username", username);
      form.set("password", password);

      const login = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form,
      });
      const loginBody = await login.json().catch(() => ({}));
      if (!login.ok) throw new Error(loginBody.detail || "Login failed");

      saveSession(loginBody.access_token, username);
      await navigate({ to: "/" });
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Authentication failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen grid place-items-center px-4">
      <section className="glass-strong w-full max-w-md rounded-2xl p-6 glow-cyan">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-cyber-cyan to-cyber-violet grid place-items-center">
            <ShieldCheck className="h-5 w-5 text-background" />
          </div>
          <div>
            <h1 className="font-display text-2xl font-bold gradient-text">SENTINEL IDS</h1>
            <p className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Operator Access</p>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-2 rounded-lg border border-white/10 bg-white/[0.03] p-1">
          <button
            onClick={() => setMode("login")}
            className={`rounded-md py-2 text-sm font-semibold transition ${mode === "login" ? "bg-cyber-cyan/20 text-cyber-cyan" : "text-muted-foreground"}`}
          >
            Login
          </button>
          <button
            onClick={() => setMode("register")}
            className={`rounded-md py-2 text-sm font-semibold transition ${mode === "register" ? "bg-cyber-cyan/20 text-cyber-cyan" : "text-muted-foreground"}`}
          >
            Register
          </button>
        </div>

        <form onSubmit={submit} className="mt-6 space-y-4">
          <label className="block">
            <span className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Username</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              minLength={3}
              className="mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm outline-none focus:border-cyber-cyan/50"
              placeholder="operator"
            />
          </label>
          <label className="block">
            <span className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Password</span>
            <input
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              minLength={6}
              type="password"
              className="mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm outline-none focus:border-cyber-cyan/50"
              placeholder="minimum 6 characters"
            />
          </label>

          {message && (
            <p className="rounded-lg border border-cyber-red/30 bg-cyber-red/10 px-3 py-2 text-sm text-cyber-red">
              {message}
            </p>
          )}

          <button
            disabled={isLoading}
            className="w-full rounded-xl bg-gradient-to-r from-cyber-cyan to-cyber-blue px-4 py-2.5 text-sm font-semibold text-background glow-cyan disabled:opacity-60"
          >
            {isLoading ? "Connecting..." : mode === "login" ? "Login" : "Register and Login"}
          </button>
        </form>
      </section>
    </main>
  );
}
