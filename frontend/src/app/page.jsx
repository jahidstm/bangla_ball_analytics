"use client";

import { useState } from "react";
import { Search, Sparkles, ArrowRight, Clock, TrendingUp, History as HistoryIcon, Bookmark, BookmarkCheck } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";

export default function Dashboard() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const { data } = await api.post("/insights/generate", { topic });
      setResult(data);
    } catch (err) {
      console.error("Failed to generate", err);
      alert("Error generating insights.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSave = async (postId) => {
    try {
      const { data } = await api.post(`/posts/${postId}/save`);
      // Update local state
      setResult((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          posts: prev.posts.map(post => 
            post.id === postId ? { ...post, is_saved: data.is_saved } : post
          )
        };
      });
    } catch (err) {
      console.error("Failed to save post", err);
    }
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
            disabled={loading}
            className="bg-primary hover:bg-primary-hover text-slate-950 font-semibold px-6 py-3 md:py-4 rounded-xl flex items-center justify-center gap-2 transition-all hover:shadow-[0_0_20px_rgba(16,185,129,0.4)] whitespace-nowrap disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                <span>Generating with AI...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Generate Analysis</span>
              </>
            )}
          </button>
        </form>
      </motion.div>

      {/* Results Section */}
      {result ? (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6 mt-8"
        >
          {/* Analysis Report */}
          {result.analysis_report && (
            <div className="glass-card p-6 md:p-8 space-y-6 border border-primary/20 bg-slate-900/50">
              <h2 className="text-2xl font-bold text-primary mb-4 flex items-center gap-2">
                <Sparkles className="w-6 h-6" />
                Tactical Analysis
              </h2>
              
              <div className="prose prose-invert max-w-none">
                <p className="text-lg text-slate-300 leading-relaxed">
                  {result.analysis_report.tactical_analysis}
                </p>
              </div>

              {result.analysis_report.key_insights && result.analysis_report.key_insights.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-xl font-semibold text-white mb-3">Key Insights</h3>
                  <ul className="space-y-2">
                    {result.analysis_report.key_insights.map((insight, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-slate-300">
                        <span className="text-primary mt-1">•</span>
                        <span>{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Generated Posts */}
          {result.posts && result.posts.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white mb-4">Generated Bangla Posts</h2>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {result.posts.map((post, idx) => (
                  <motion.div 
                    key={post.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass-card p-6 flex flex-col h-full border border-slate-700 hover:border-primary/50 transition-colors relative"
                  >
                    <div className="flex justify-between items-center mb-4 pb-4 border-b border-slate-700/50">
                      <span className="px-3 py-1 bg-primary/20 text-primary text-sm font-semibold rounded-full">
                        {post.style_type || "Variant " + (idx + 1)}
                      </span>
                      <div className="flex items-center gap-3">
                        <button 
                          onClick={() => handleToggleSave(post.id)}
                          className="text-slate-400 hover:text-primary transition-colors flex items-center justify-center p-1"
                          title={post.is_saved ? "Unsave" : "Save to Library"}
                        >
                          {post.is_saved ? (
                            <BookmarkCheck className="w-5 h-5 text-primary" />
                          ) : (
                            <Bookmark className="w-5 h-5" />
                          )}
                        </button>
                        <button 
                          onClick={() => navigator.clipboard.writeText(post.content)}
                          className="text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-1 bg-slate-800/50 hover:bg-slate-700 px-3 py-1 rounded-md"
                        >
                          Copy
                        </button>
                      </div>
                    </div>
                    <p className="text-slate-200 whitespace-pre-wrap flex-grow leading-relaxed">
                      {post.content}
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      ) : (
        /* Suggested & Recent Grids */
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
      )}
    </div>
  );
}
