"use client";

import { useState, useEffect } from "react";
import { Bookmark, BookmarkCheck, Library as LibraryIcon, Search, Copy, Check } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "@/lib/api";

export default function LibraryPage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    fetchSavedPosts();
  }, []);

  const fetchSavedPosts = async () => {
    try {
      setLoading(true);
      const { data } = await api.get("/posts/saved");
      setPosts(data);
    } catch (err) {
      console.error("Failed to fetch saved posts", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSave = async (postId) => {
    try {
      const { data } = await api.post(`/posts/${postId}/save`);
      // If it's unsaved, remove it from the list
      if (!data.is_saved) {
        setPosts((prev) => prev.filter(post => post.id !== postId));
      }
    } catch (err) {
      console.error("Failed to unsave post", err);
    }
  };

  const handleCopy = (id, content) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredPosts = posts.filter(p => 
    p.content.toLowerCase().includes(searchQuery.toLowerCase()) || 
    (p.style_type && p.style_type.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="space-y-8 h-full flex flex-col">
      <header className="mb-4 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-heading font-bold mb-3 flex items-center gap-3">
            <LibraryIcon className="w-8 h-8 text-primary" />
            Your <span className="text-primary text-glow">Library</span>
          </h1>
          <p className="text-slate-400 text-lg">All your favorite generated football posts in one place.</p>
        </div>
        
        <div className="relative w-full md:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search saved posts..."
            className="w-full bg-slate-800/80 border border-slate-700 focus:border-primary/50 rounded-lg py-2 pl-10 pr-4 text-white placeholder-slate-500 outline-none transition-all"
          />
        </div>
      </header>

      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      ) : filteredPosts.length === 0 ? (
        <div className="glass-card flex-1 flex flex-col items-center justify-center text-center p-10 border-dashed border-2 border-slate-700/50 bg-slate-900/20">
          <Bookmark className="w-12 h-12 text-slate-600 mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">Library is Empty</h3>
          <p className="text-slate-400 max-w-md">
            {searchQuery 
              ? "No saved posts match your search query."
              : "You haven't saved any posts yet. Click the bookmark icon on any generated post to save it here."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
          {filteredPosts.map((post, idx) => (
            <motion.div
              key={post.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.05 }}
              className="glass-card p-6 flex flex-col h-full border border-slate-700 hover:border-primary/50 transition-colors relative group"
            >
              <div className="flex justify-between items-center mb-4 pb-4 border-b border-slate-700/50">
                <span className="px-3 py-1 bg-primary/20 text-primary text-sm font-semibold rounded-full">
                  {post.style_type || "Post Variant"}
                </span>
                
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                  <button 
                    onClick={() => handleToggleSave(post.id)}
                    className="text-primary hover:text-red-400 transition-colors flex items-center justify-center p-1"
                    title="Remove from Library"
                  >
                    <BookmarkCheck className="w-5 h-5" />
                  </button>
                </div>
              </div>

              <p className="text-slate-200 whitespace-pre-wrap flex-grow leading-relaxed mb-6">
                {post.content}
              </p>

              <div className="flex justify-end mt-auto pt-4 border-t border-slate-800">
                <button 
                  onClick={() => handleCopy(post.id, post.content)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                    copiedId === post.id 
                      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/50" 
                      : "bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700 hover:text-white"
                  }`}
                >
                  {copiedId === post.id ? (
                    <>
                      <Check className="w-4 h-4" /> Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" /> Copy Text
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
