"""
Supabase Database Setup Script
================================
এই SQL গুলো Supabase Dashboard > SQL Editor এ রান করুন।

Steps:
1. Supabase Dashboard এ যান
2. বামদিকে "SQL Editor" এ ক্লিক করুন
3. "New Query" ক্লিক করুন
4. নিচের সমস্ত SQL কপি করে paste করুন
5. "Run" বাটনে ক্লিক করুন
"""

SQL = """
-- ── Extensions ─────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── Insights Table ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    analysis_report JSONB,
    chart_data JSONB,
    chart_image_path TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Posts Table ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insight_id UUID REFERENCES insights(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    style_type VARCHAR(50),
    hashtags TEXT[],
    is_saved BOOLEAN DEFAULT FALSE,
    is_edited BOOLEAN DEFAULT FALSE,
    edited_content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Players Cache Table ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS players_cache (
    id VARCHAR(50) PRIMARY KEY,
    name TEXT NOT NULL,
    team TEXT,
    nationality TEXT,
    position TEXT,
    age INTEGER,
    stats JSONB,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- ── Style Posts Table (RAG metadata) ────────────────────────────────────
CREATE TABLE IF NOT EXISTS style_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    page_name TEXT,
    style_type TEXT,
    chroma_doc_id TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Indexes ─────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_insights_status ON insights(status);
CREATE INDEX IF NOT EXISTS idx_insights_created_at ON insights(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_insight_id ON posts(insight_id);
CREATE INDEX IF NOT EXISTS idx_posts_is_saved ON posts(is_saved);

-- ── Updated_at auto-update trigger ──────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_insights_updated_at
    BEFORE UPDATE ON insights
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ── Verification ────────────────────────────────────────────────────────
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""

if __name__ == "__main__":
    print("=" * 60)
    print("Bangla Ball Analytics — Database Setup SQL")
    print("=" * 60)
    print()
    print("Supabase Dashboard > SQL Editor > New Query এ")
    print("নিচের SQL কপি করে Paste করুন এবং Run করুন:")
    print()
    print(SQL)
