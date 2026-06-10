"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, History as HistoryIcon, Bookmark, Settings, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

const LINKS = [
  { name: "Dashboard", href: "/", icon: Home },
  { name: "History", href: "/history", icon: HistoryIcon },
  { name: "Library", href: "/library", icon: Bookmark },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 glass border-r border-slate-700/50 flex flex-col pt-6 hidden md:flex">
      <div className="px-6 mb-8">
        <button className="w-full relative group overflow-hidden rounded-xl bg-slate-800 border border-slate-700 hover:border-primary/50 transition-colors p-3 flex items-center justify-center gap-2">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10 opacity-0 group-hover:opacity-100 transition-opacity" />
          <Sparkles className="w-4 h-4 text-primary group-hover:text-glow transition-all" />
          <span className="font-medium text-sm text-slate-200 group-hover:text-white">New Insight</span>
        </button>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {LINKS.map((link) => {
          const isActive = pathname === link.href;
          const Icon = link.icon;
          
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors outline-none",
                isActive 
                  ? "text-white" 
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="active-nav-indicator"
                  className="absolute inset-0 bg-slate-800 border border-slate-700 rounded-lg"
                  initial={false}
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <Icon className={cn("w-4 h-4 relative z-10", isActive ? "text-primary text-glow" : "")} />
              <span className="relative z-10">{link.name}</span>
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 mt-auto border-t border-slate-800">
        <div className="text-xs text-slate-500 text-center">v1.0.0 (Phase 2)</div>
      </div>
    </aside>
  );
}
