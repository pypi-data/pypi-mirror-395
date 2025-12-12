"""Database schema definitions."""

# Table schemas
SCHEMA_DEFINITIONS = {
    "prompt_versions": """
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            user_prompt TEXT NOT NULL,
            metadata TEXT,
            git_commit TEXT,
            timestamp TEXT NOT NULL,
            created_by TEXT,
            tags TEXT,
            UNIQUE(name, version)
        )
    """,
    "prompt_metrics": """
        CREATE TABLE IF NOT EXISTS prompt_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            model_name TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            total_tokens INTEGER,
            cost_eur REAL,
            latency_ms REAL,
            quality_score REAL,
            accuracy REAL,
            temperature REAL,
            top_p REAL,
            max_tokens INTEGER,
            success BOOLEAN,
            error_message TEXT,
            timestamp TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE
        )
    """,
    "annotations": """
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            annotation_type TEXT DEFAULT 'comment',
            resolved BOOLEAN DEFAULT 0,
            FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE
        )
    """,
    "version_tags": """
        CREATE TABLE IF NOT EXISTS version_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE,
            UNIQUE(version_id, tag)
        )
    """,
}

# Indexes for performance
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_name_version ON prompt_versions(name, version)",
    "CREATE INDEX IF NOT EXISTS idx_timestamp ON prompt_versions(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_name ON prompt_versions(name)",
    "CREATE INDEX IF NOT EXISTS idx_metrics_version ON prompt_metrics(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON prompt_metrics(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_annotations_version ON annotations(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_tags_version ON version_tags(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_tags_tag ON version_tags(tag)",
]

# Schema version for migrations
SCHEMA_VERSION = 1
