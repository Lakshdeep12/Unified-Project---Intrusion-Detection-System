const particles = Array.from({ length: 70 }, (_, i) => ({
  id: i,
  left: `${(i * 37) % 100}%`,
  top: `${(i * 53) % 100}%`,
  delay: `${(i % 12) * 0.4}s`,
  size: `${2 + (i % 3)}px`,
}));

export function ParticleField() {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none overflow-hidden">
      <div className="absolute inset-0 grid-bg opacity-40" />
      <div className="absolute inset-0 cyber-grid-floor" />
      {particles.map((p) => (
        <span
          key={p.id}
          className="absolute rounded-full bg-cyber-cyan/70 particle-dot"
          style={{
            left: p.left,
            top: p.top,
            width: p.size,
            height: p.size,
            animationDelay: p.delay,
          }}
        />
      ))}
      <div className="absolute inset-0" style={{ background: "radial-gradient(ellipse at center, transparent 30%, oklch(0.10 0.03 260 / 0.85) 90%)" }} />
    </div>
  );
}
