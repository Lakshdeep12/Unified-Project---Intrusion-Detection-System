import { createFileRoute, Outlet, useRouterState } from "@tanstack/react-router";
import { AnimatePresence, motion } from "framer-motion";
import { lazy, Suspense, useEffect, useState } from "react";
import { Sidebar } from "@/components/cyber/Sidebar";
import { TopNav } from "@/components/cyber/TopNav";
import { getToken } from "@/lib/api";

const ParticleField = lazy(() =>
  import("@/components/cyber/ParticleField").then((m) => ({ default: m.ParticleField })),
);

export const Route = createFileRoute("/_app")({
  component: AppLayout,
});

function AppLayout() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      window.location.href = "/login";
      return;
    }
    setIsReady(true);
  }, []);

  if (!isReady) {
    return (
      <div className="min-h-screen grid place-items-center text-sm font-mono text-cyber-cyan">
        Checking operator session...
      </div>
    );
  }

  return (
    <div className="min-h-screen flex w-full relative">
      <Suspense fallback={null}>
        <ParticleField />
      </Suspense>

      <Sidebar />

      <div className="flex-1 min-w-0 flex flex-col">
        <TopNav />
        <main className="flex-1 p-4 lg:pl-0">
          <AnimatePresence mode="wait">
            <motion.div
              key={pathname}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
