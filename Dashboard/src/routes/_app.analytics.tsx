import { createFileRoute } from "@tanstack/react-router";
import { Fragment, useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { Panel, PanelHeader } from "@/components/cyber/Card";

export const Route = createFileRoute("/_app/analytics")({
  head: () => ({
    meta: [
      { title: "Analytics — SENTINEL IDS" },
      { name: "description", content: "Model analytics: confusion matrix, ROC, precision-recall, feature importance." },
    ],
  }),
  component: AnalyticsPage,
});

const tooltipStyle = {
  background: "oklch(0.18 0.035 260 / 0.92)",
  border: "1px solid oklch(0.85 0.18 200 / 0.35)",
  borderRadius: 12,
  fontSize: 12,
  fontFamily: "JetBrains Mono",
};

function AnalyticsPage() {
  const [cm, setCm] = useState<number[][]>([[0, 0], [0, 0]]);
  const [roc, setRoc] = useState<any[]>([]);
  const [pr, setPr] = useState<any[]>([]);
  const [features, setFeatures] = useState<any[]>([]);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
        
        const [cmRes, rocRes, prRes, featRes] = await Promise.all([
          fetch(`${baseUrl}/metrics/confusion-matrix`),
          fetch(`${baseUrl}/metrics/roc`),
          fetch(`${baseUrl}/metrics/precision-recall`),
          fetch(`${baseUrl}/metrics/feature-importance`)
        ]);

        if (cmRes.ok) {
          const data = await cmRes.json();
          setCm(data.matrix);
        }
        
        if (rocRes.ok) {
          const data = await rocRes.json();
          const rocData = data.fpr.map((f: number, i: number) => ({
            fpr: +f.toFixed(2),
            tpr: +data.tpr[i].toFixed(3),
            baseline: +f.toFixed(2)
          }));
          setRoc(rocData);
        }
        
        if (prRes.ok) {
          const data = await prRes.json();
          const prData = data.recall.map((r: number, i: number) => ({
            recall: +r.toFixed(2),
            precision: +data.precision[i].toFixed(3)
          }));
          setPr(prData);
        }
        
        if (featRes.ok) {
          const data = await featRes.json();
          const featData = data.features.map((f: any) => ({
            name: f.name,
            v: f.importance
          }));
          setFeatures(featData);
        }
      } catch (err) {
        console.error("Failed to fetch analytics metrics", err);
      }
    };
    
    fetchData();
  }, []);

  return (
    <div className="space-y-6 mt-4">
      <header>
        <p className="text-[11px] font-mono uppercase tracking-[0.3em] text-cyber-cyan">MODEL · v4.2-hybrid</p>
        <h1 className="font-display text-3xl md:text-4xl font-bold mt-1 gradient-text">Detection Analytics</h1>
        <p className="text-sm text-muted-foreground mt-1">Performance, calibration and feature attribution.</p>
      </header>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Confusion Matrix */}
        <Panel>
          <PanelHeader accent="EVALUATION" title="Confusion Matrix" subtitle="Test set · 11,323 flows" />
          <div className="px-5 pb-5">
            <div className="grid grid-cols-[auto_1fr_1fr] gap-2 text-xs font-mono">
              <div />
              <div className="text-center text-muted-foreground">Pred · Normal</div>
              <div className="text-center text-muted-foreground">Pred · Attack</div>

              {(["Actual · Normal", "Actual · Attack"] as const).map((label, r) => (
                <Fragment key={`row-${r}`}>
                  <div className="text-muted-foreground self-center pr-2">{label}</div>
                  {[0, 1].map((c) => {
                    const v = cm[r][c];
                    const correct = r === c;
                    const max = Math.max(...cm.flat());
                    const intensity = v / max;
                    return (
                      <motion.div
                        key={`${r}-${c}`}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.1 + (r * 2 + c) * 0.08 }}
                        className="aspect-square rounded-xl border grid place-items-center relative overflow-hidden"
                        style={{
                          background: correct
                            ? `oklch(0.82 0.22 150 / ${0.15 + intensity * 0.55})`
                            : `oklch(0.68 0.25 22 / ${0.15 + intensity * 0.55})`,
                          borderColor: correct ? "oklch(0.82 0.22 150 / 0.5)" : "oklch(0.68 0.25 22 / 0.5)",
                        }}
                      >
                        <div className="text-center">
                          <p className="font-display text-2xl font-bold tabular-nums">{v.toLocaleString()}</p>
                          <p className="text-[10px] mt-0.5 opacity-70">
                            {r === 0 && c === 0 && "TN"}
                            {r === 0 && c === 1 && "FP"}
                            {r === 1 && c === 0 && "FN"}
                            {r === 1 && c === 1 && "TP"}
                          </p>
                        </div>
                      </motion.div>
                    );
                  })}
                </Fragment>
              ))}
            </div>
            <div className="grid grid-cols-3 gap-2 mt-4 text-center">
              <Metric label="Accuracy" value="98.07%" />
              <Metric label="Precision" value="90.04%" />
              <Metric label="Recall" value="94.41%" />
            </div>
          </div>
        </Panel>

        {/* Feature importance */}
        <Panel>
          <PanelHeader accent="EXPLAINABILITY" title="Feature Importance" subtitle="SHAP-based attribution" />
          <div className="px-5 pb-5 h-[320px] min-w-[300px] min-h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={features} layout="vertical" margin={{ left: 16, right: 12, top: 8 }}>
                <CartesianGrid stroke="oklch(0.85 0.18 200 / 0.07)" horizontal={false} />
                <XAxis type="number" domain={[0, 1]} tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fill: "oklch(0.85 0.04 240)", fontSize: 11, fontFamily: "JetBrains Mono" }} width={110} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "oklch(0.85 0.18 200 / 0.06)" }} />
                <Bar dataKey="v" radius={[0, 8, 8, 0]} animationDuration={1100}>
                  {features.map((_, i) => (
                    <Cell key={i} fill={`oklch(0.85 0.18 ${200 - i * 8})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* ROC */}
        <Panel>
          <PanelHeader accent="ROC · AUC = 0.978" title="Receiver Operating Characteristic" subtitle="True vs False positive rate" />
          <div className="px-5 pb-5 h-[300px] min-w-[300px] min-h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={roc} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
                <defs>
                  <linearGradient id="roc-stroke" x1="0" x2="1">
                    <stop offset="0%" stopColor="oklch(0.82 0.22 150)" />
                    <stop offset="100%" stopColor="oklch(0.85 0.18 200)" />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="oklch(0.85 0.18 200 / 0.07)" />
                <XAxis dataKey="fpr" tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} axisLine={false} tickLine={false} label={{ value: "FPR", position: "insideBottom", offset: -2, fill: "oklch(0.7 0.04 240)", fontSize: 10 }} />
                <YAxis tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} axisLine={false} tickLine={false} width={32} />
                <Tooltip contentStyle={tooltipStyle} />
                <Line type="monotone" dataKey="baseline" stroke="oklch(0.55 0.04 240)" strokeDasharray="4 4" dot={false} strokeWidth={1.5} />
                <Line type="monotone" dataKey="tpr" stroke="url(#roc-stroke)" strokeWidth={3} dot={false} animationDuration={1400} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* PR */}
        <Panel>
          <PanelHeader accent="PR · AP = 0.961" title="Precision-Recall Curve" subtitle="Operating point @ 0.72 threshold" />
          <div className="px-5 pb-5 h-[300px] min-w-[300px] min-h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={pr} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
                <CartesianGrid stroke="oklch(0.85 0.18 200 / 0.07)" />
                <XAxis dataKey="recall" tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "oklch(0.7 0.04 240)", fontSize: 10, fontFamily: "JetBrains Mono" }} axisLine={false} tickLine={false} width={32} />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend wrapperStyle={{ fontSize: 11, fontFamily: "JetBrains Mono" }} />
                <Line type="monotone" dataKey="precision" stroke="oklch(0.7 0.22 305)" strokeWidth={3} dot={false} animationDuration={1400} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.03] py-2.5">
      <p className="text-[10px] uppercase tracking-widest text-muted-foreground font-mono">{label}</p>
      <p className="font-display text-lg font-bold text-cyber-cyan text-glow-cyan">{value}</p>
    </div>
  );
}
