import { useEffect, useRef, useState } from "react";

export function Counter({
  value, duration = 1500, format,
}: { value: number; duration?: number; format?: (n: number) => string }) {
  const [n, setN] = useState(0);
  const start = useRef<number | null>(null);
  const from = useRef(0);

  useEffect(() => {
    from.current = n;
    start.current = null;
    let raf = 0;
    const tick = (t: number) => {
      if (start.current === null) start.current = t;
      const p = Math.min(1, (t - start.current) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(Math.round(from.current + (value - from.current) * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, duration]);

  return <>{format ? format(n) : n.toLocaleString()}</>;
}
