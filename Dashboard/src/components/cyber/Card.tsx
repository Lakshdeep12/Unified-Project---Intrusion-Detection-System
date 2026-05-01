import { motion, type HTMLMotionProps } from "framer-motion";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

interface PanelProps extends HTMLMotionProps<"div"> {
  glow?: "cyan" | "red" | "green" | "none";
}

export const Panel = forwardRef<HTMLDivElement, PanelProps>(
  ({ className, glow = "none", children, ...props }, ref) => {
    return (
      <motion.div
        ref={ref}
        whileHover={{ y: -2 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
        className={cn(
          "glass rounded-2xl relative overflow-hidden group",
          glow === "cyan" && "hover:glow-cyan",
          glow === "red" && "hover:glow-red",
          glow === "green" && "hover:glow-green",
          className,
        )}
        {...props}
      >
        <span className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyber-cyan/40 to-transparent" />
        {children as React.ReactNode}
      </motion.div>
    );
  },
);
Panel.displayName = "Panel";

export function PanelHeader({
  title, subtitle, accent, right,
}: {
  title: string; subtitle?: string; accent?: string; right?: React.ReactNode;
}) {
  return (
    <div className="flex items-start justify-between gap-3 px-5 pt-5 pb-3">
      <div>
        {accent && (
          <p className="text-[10px] uppercase font-mono tracking-[0.25em] text-cyber-cyan mb-1">
            {accent}
          </p>
        )}
        <h3 className="font-display text-base font-semibold leading-tight">{title}</h3>
        {subtitle && <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>}
      </div>
      {right}
    </div>
  );
}
