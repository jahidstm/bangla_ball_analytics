"use client";

import { useState, useEffect } from "react";
import { History as HistoryIcon, Search, Calendar, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import Link from "next/link";

export default function HistoryPage() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const { data } = await api.get("/insights/");
      setInsights(data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    } finally {
      setLoading(false);
    }
  };

  const filteredInsights = insights.filter(i => 
    i.topic.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 h-full flex flex-col">
      <header className="mb-4 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-heading font-bold mb-3 flex items-center gap-3">
            <HistoryIcon className="w-8 h-8 text-primary" />
            Generation <span className="text-primary text-glow">History</span>
          </h1>
          <p className="text-slate-400 text-lg">View all your past AI-generated football insights.</p>
        </div>
        
        <div className="relative w-full md:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search history..."
            className="w-full bg-slate-800/80 border border-slate-700 focus:border-primary/50 rounded-lg py-2 pl-10 pr-4 text-white placeholder-slate-500 outline-none transition-all"
          />
        </div>
      </header>

      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      ) : filteredInsights.length === 0 ? (
        <div className="glass-card flex-1 flex flex-col items-center justify-center text-center p-10 border-dashed border-2 border-slate-700/50 bg-slate-900/20">
          <HistoryIcon className="w-12 h-12 text-slate-600 mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">No History Found</h3>
          <p className="text-slate-400 max-w-md">
            {searchQuery 
              ? "No insights match your search query."
              : "You haven't generated any insights yet. Head over to the Dashboard to create one!"}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {filteredInsights.map((insight, idx) => (
            <motion.div
              key={insight.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <Link href={`/history/${insight.id}`}>
                <div className="glass-card p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 group hover:border-primary/50 transition-colors cursor-pointer">
                  <div className="space-y-1 flex-1">
                    <h3 className="text-lg font-bold text-white group-hover:text-primary transition-colors">
                      {insight.topic}
                    </h3>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-slate-400">
                      <span className="flex items-center gap-1.5">
                        <Calendar className="w-4 h-4" />
                        {new Date(insight.created_at).toLocaleDateString("en-US", {
                          year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
                        })}
                      </span>
                      {insight.status === "completed" ? (
                        <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {insight.post_count} Posts Generated
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-md bg-red-500/10 text-red-400 border border-red-500/20">
                          Failed
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center group-hover:bg-primary/20 group-hover:text-primary transition-all">
                    <ChevronRight className="w-5 h-5" />
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
