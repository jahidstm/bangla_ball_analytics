"use client";

import { useState } from "react";
import { Search, Sparkles, ArrowRight, Clock, TrendingUp, History as HistoryIcon } from "lucide-react";
import { motion } from "framer-motion";

export default function Dashboard() {
  const [topic, setTopic] = useState("");

  const handleGenerate = (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    // We will connect this to backend next
    console.log("Generating insight for:", topic);
  };

  return (
    <div className="space-y-8 h-full flex flex-col">
      {/* Hero Header */}
      <header className="mb-4">
        <h1 className="text-3xl md:text-4xl font-heading font-bold mb-3">
          Discover Football <span className="text-primary text-glow">Insights</span>
        </h1>
        <p className="text-slate-400 text-lg">Generate deep analytics and Bangla content instantly using AI.</p>
      </header>

      {/* Main Search/Generate Bar */}
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-2 md:p-3 relative z-10"
      >
        <form onSubmit={handleGenerate} className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="E.g., Messi's performance vs Top 6 in 2024..."
              className="w-full bg-slate-800/50 border border-slate-700 focus:border-primary/50 focus:ring-1 focus:ring-primary/50 rounded-xl py-3 md:py-4 pl-12 pr-4 text-white placeholder-slate-500 outline-none transition-all text-base md:text-lg"
            />
          </div>
          <button 
            type="submit"
            className="bg-primary hover:bg-primary-hover text-slate-950 font-semibold px-6 py-3 md:py-4 rounded-xl flex items-center justify-center gap-2 transition-all hover:shadow-[0_0_20px_rgba(16,185,129,0.4)] whitespace-nowrap"
          >
            <Sparkles className="w-5 h-5" />
            <span>Generate Analysis</span>
          </button>
        </form>
      </motion.div>

      {/* Suggested & Recent Grids */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        
        {/* Trending Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-slate-300 font-medium">
            <TrendingUp className="w-5 h-5 text-accent" />
            <h2>Trending Topics</h2>
          </div>
          <div className="grid grid-cols-1 gap-3">
            {["Real Madrid's new formation analysis", "Mbappe's impact in La Liga", "Argentina vs Brazil tactical review"].map((item, i) => (
              <motion.button 
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                onClick={() => setTopic(item)}
                className="glass-card p-4 text-left flex items-center justify-between group cursor-pointer"
              >
                <span className="text-slate-300 group-hover:text-white transition-colors">{item}</span>
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-primary transition-colors" />
              </motion.button>
            ))}
          </div>
        </div>

        {/* Recent History Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-slate-300 font-medium">
            <Clock className="w-5 h-5 text-slate-400" />
            <h2>Recent Analyses</h2>
          </div>
          <div className="glass-card p-6 flex flex-col items-center justify-center text-center h-[240px] border-dashed border-2 border-slate-700/50 bg-slate-900/20">
            <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mb-3">
              <HistoryIcon className="w-6 h-6 text-slate-500" />
            </div>
            <p className="text-slate-400 mb-1">No recent history</p>
            <p className="text-sm text-slate-500">Your generated insights will appear here</p>
          </div>
        </div>

      </div>
    </div>
  );
}
