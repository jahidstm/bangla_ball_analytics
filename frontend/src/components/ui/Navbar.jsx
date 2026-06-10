"use client";

import { useEffect, useState } from "react";
import { Activity, Database, ServerCrash } from "lucide-react";
import { api } from "@/lib/api";

export default function Navbar() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await api.get("/health");
        if (res.data.database === "connected") {
          setStatus("connected");
        } else {
          setStatus("db_error");
        }
      } catch (err) {
        setStatus("disconnected");
      }
    };
    
    checkHealth();
    // Poll every 30s
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 glass border-b border-slate-700/50 px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-accent flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.4)]">
          <Activity className="w-4 h-4 text-white" />
        </div>
        <h1 className="font-heading font-bold text-xl tracking-wide bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
          Bangla Ball <span className="text-primary text-glow">Analytics</span>
        </h1>
      </div>

      <div className="flex items-center gap-2 text-sm px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700">
        {status === "checking" && (
          <><div className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" /> <span className="text-slate-400">Checking...</span></>
        )}
        {status === "connected" && (
          <><Database className="w-3.5 h-3.5 text-primary" /> <span className="text-primary font-medium">DB Connected</span></>
        )}
        {status === "db_error" && (
          <><Database className="w-3.5 h-3.5 text-red-400" /> <span className="text-red-400">DB Error</span></>
        )}
        {status === "disconnected" && (
          <><ServerCrash className="w-3.5 h-3.5 text-red-500" /> <span className="text-red-500">API Offline</span></>
        )}
      </div>
    </header>
  );
}
