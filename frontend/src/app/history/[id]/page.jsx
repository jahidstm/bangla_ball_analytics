"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Sparkles, Bookmark, BookmarkCheck } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";

export default function HistoryDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params?.id) {
      fetchInsightDetails(params.id);
    }
  }, [params?.id]);

  const fetchInsightDetails = async (id) => {
    try {
      setLoading(true);
      const { data } = await api.get(`/insights/${id}`);
      setResult(data);
    } catch (err) {
      console.error("Failed to fetch insight details", err);
      alert("Error loading insight details.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSave = async (postId) => {
    try {
      const { data } = await api.post(`/posts/${postId}/save`);
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

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!result) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center">
        <h2 className="text-2xl font-bold text-white mb-2">Insight Not Found</h2>
        <button 
          onClick={() => router.back()}
          className="text-primary hover:underline"
        >
          Go back
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 h-full flex flex-col">
      <header className="mb-2">
        <button 
          onClick={() => router.push("/history")}
          className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-6 group w-fit"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Back to History
        </button>
        <h1 className="text-3xl md:text-4xl font-heading font-bold mb-3 text-white">
          {result.topic}
        </h1>
        <p className="text-slate-400">
          Generated on {new Date(result.created_at).toLocaleString()}
        </p>
      </header>

      {/* Analysis Report */}
      {result.analysis_report && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6 md:p-8 space-y-6 border border-primary/20 bg-slate-900/50"
        >
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
        </motion.div>
      )}

      {/* Generated Posts */}
      {result.posts && result.posts.length > 0 && (
        <div className="space-y-4 mt-6">
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
    </div>
  );
}
