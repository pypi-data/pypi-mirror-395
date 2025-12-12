"""Database schema and connection management."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

from mcp_git_analyzer.config import get_db_path


SCHEMA = """
-- Repositories table
CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    local_path TEXT NOT NULL,
    default_branch TEXT DEFAULT 'main',
    cloned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed TIMESTAMP,
    description TEXT,
    metadata JSON
);

-- Files table  
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    path TEXT NOT NULL,
    language TEXT,
    content_hash TEXT,
    line_count INTEGER,
    last_modified TIMESTAMP,
    analyzed_at TIMESTAMP,
    UNIQUE(repo_id, path)
);

-- Symbols table (functions, classes, methods)
CREATE TABLE IF NOT EXISTS symbols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'function', 'class', 'method', 'variable'
    signature TEXT,
    docstring TEXT,
    start_line INTEGER,
    end_line INTEGER,
    parent_id INTEGER REFERENCES symbols(id),  -- for methods inside classes
    metadata JSON,  -- complexity, parameters, return type, etc.
    UNIQUE(file_id, name, type, start_line)
);

-- Imports table
CREATE TABLE IF NOT EXISTS imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    module TEXT NOT NULL,
    alias TEXT,
    imported_names TEXT,  -- JSON array of imported names
    is_relative BOOLEAN DEFAULT FALSE,
    line_number INTEGER,
    UNIQUE(file_id, module, imported_names)
);

-- Patterns table (detected algorithms, design patterns)
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol_id INTEGER REFERENCES symbols(id) ON DELETE CASCADE,
    file_id INTEGER REFERENCES files(id) ON DELETE CASCADE,
    pattern_type TEXT NOT NULL,  -- 'algorithm', 'design_pattern', 'idiom'
    pattern_name TEXT NOT NULL,  -- 'recursion', 'dynamic_programming', 'singleton', etc.
    confidence REAL DEFAULT 1.0,
    evidence TEXT,  -- why this pattern was detected
    metadata JSON
);

-- Documentation table (README, docstrings, comments)
CREATE TABLE IF NOT EXISTS documentation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER REFERENCES repositories(id) ON DELETE CASCADE,
    file_id INTEGER REFERENCES files(id) ON DELETE CASCADE,
    doc_type TEXT NOT NULL,  -- 'readme', 'docstring', 'comment', 'inline_comment'
    content TEXT NOT NULL,
    start_line INTEGER,
    end_line INTEGER,
    symbol_id INTEGER REFERENCES symbols(id)
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_files_repo ON files(repo_id);
CREATE INDEX IF NOT EXISTS idx_files_language ON files(language);
CREATE INDEX IF NOT EXISTS idx_symbols_file ON symbols(file_id);
CREATE INDEX IF NOT EXISTS idx_symbols_type ON symbols(type);
CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols(name);
CREATE INDEX IF NOT EXISTS idx_imports_file ON imports(file_id);
CREATE INDEX IF NOT EXISTS idx_imports_module ON imports(module);
CREATE INDEX IF NOT EXISTS idx_patterns_symbol ON patterns(symbol_id);
CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_patterns_name ON patterns(pattern_name);

-- Function calls table (for call graph analysis)
CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    caller_id INTEGER REFERENCES symbols(id) ON DELETE CASCADE,  -- NULL if caller not resolved
    caller_name TEXT NOT NULL,  -- Fully qualified caller name (e.g., "ClassName.method")
    callee_name TEXT NOT NULL,  -- Name of called function/method
    callee_id INTEGER REFERENCES symbols(id) ON DELETE SET NULL,  -- NULL if external/unresolved
    call_type TEXT NOT NULL,  -- 'function', 'method', 'builtin'
    line_number INTEGER,
    is_external BOOLEAN DEFAULT FALSE,
    module TEXT,  -- Module name if external call
    is_resolved BOOLEAN DEFAULT FALSE,  -- Whether callee_id was resolved
    metadata JSON  -- Additional info like arguments
);

-- Indexes for call graph queries
CREATE INDEX IF NOT EXISTS idx_calls_file ON calls(file_id);
CREATE INDEX IF NOT EXISTS idx_calls_caller_id ON calls(caller_id);
CREATE INDEX IF NOT EXISTS idx_calls_caller_name ON calls(caller_name);
CREATE INDEX IF NOT EXISTS idx_calls_callee_id ON calls(callee_id);
CREATE INDEX IF NOT EXISTS idx_calls_callee_name ON calls(callee_name);
CREATE INDEX IF NOT EXISTS idx_calls_call_type ON calls(call_type);

-- FTS5 virtual table for full-text search on symbols
CREATE VIRTUAL TABLE IF NOT EXISTS symbols_fts USING fts5(
    name,
    signature,
    docstring,
    content='symbols',
    content_rowid='id'
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER IF NOT EXISTS symbols_ai AFTER INSERT ON symbols BEGIN
    INSERT INTO symbols_fts(rowid, name, signature, docstring) 
    VALUES (new.id, new.name, new.signature, new.docstring);
END;

CREATE TRIGGER IF NOT EXISTS symbols_ad AFTER DELETE ON symbols BEGIN
    INSERT INTO symbols_fts(symbols_fts, rowid, name, signature, docstring) 
    VALUES ('delete', old.id, old.name, old.signature, old.docstring);
END;

CREATE TRIGGER IF NOT EXISTS symbols_au AFTER UPDATE ON symbols BEGIN
    INSERT INTO symbols_fts(symbols_fts, rowid, name, signature, docstring) 
    VALUES ('delete', old.id, old.name, old.signature, old.docstring);
    INSERT INTO symbols_fts(rowid, name, signature, docstring) 
    VALUES (new.id, new.name, new.signature, new.docstring);
END;

-- FTS5 for documentation search
CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
    content,
    content='documentation',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS docs_ai AFTER INSERT ON documentation BEGIN
    INSERT INTO docs_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE TRIGGER IF NOT EXISTS docs_ad AFTER DELETE ON documentation BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, content) VALUES ('delete', old.id, old.content);
END;

CREATE TRIGGER IF NOT EXISTS docs_au AFTER UPDATE ON documentation BEGIN
    INSERT INTO docs_fts(docs_fts, rowid, content) VALUES ('delete', old.id, old.content);
    INSERT INTO docs_fts(rowid, content) VALUES (new.id, new.content);
END;

-- Core algorithms table (unique algorithm implementations)
CREATE TABLE IF NOT EXISTS core_algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol_id INTEGER NOT NULL REFERENCES symbols(id) ON DELETE CASCADE,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    repo_id INTEGER NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    
    -- Source code storage
    source_code TEXT NOT NULL,           -- Original function source
    normalized_code TEXT,                -- Whitespace/comment normalized
    ast_hash TEXT,                       -- Structure hash (ignores var names/literals)
    
    -- Complexity metrics (JSON)
    complexity_metrics JSON,             -- {cyclomatic, nesting_depth, loops, conditionals, lines}
    
    -- Classification
    static_category TEXT,                -- Static analysis category: sorting/searching/graph/dp/math/string/tree/io/other
    llm_category TEXT,                   -- LLM-determined category
    
    -- LLM analysis results (JSON)
    llm_analysis JSON,                   -- {purpose, time_complexity, space_complexity, use_cases, improvements}
    
    -- Embedding for similarity search
    embedding BLOB,                      -- Vector embedding (float32 array)
    embedding_model TEXT,                -- Model used to generate embedding
    embedding_dimension INTEGER,         -- Dimension of the embedding vector
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(symbol_id)
);

-- Indexes for core_algorithms
CREATE INDEX IF NOT EXISTS idx_algorithms_symbol ON core_algorithms(symbol_id);
CREATE INDEX IF NOT EXISTS idx_algorithms_file ON core_algorithms(file_id);
CREATE INDEX IF NOT EXISTS idx_algorithms_repo ON core_algorithms(repo_id);
CREATE INDEX IF NOT EXISTS idx_algorithms_ast_hash ON core_algorithms(ast_hash);
CREATE INDEX IF NOT EXISTS idx_algorithms_static_category ON core_algorithms(static_category);
CREATE INDEX IF NOT EXISTS idx_algorithms_llm_category ON core_algorithms(llm_category);

-- FTS5 for algorithm search
CREATE VIRTUAL TABLE IF NOT EXISTS algorithms_fts USING fts5(
    source_code,
    llm_analysis,
    content='core_algorithms',
    content_rowid='id'
);

-- Triggers to keep algorithms FTS in sync
CREATE TRIGGER IF NOT EXISTS algorithms_ai AFTER INSERT ON core_algorithms BEGIN
    INSERT INTO algorithms_fts(rowid, source_code, llm_analysis) 
    VALUES (new.id, new.source_code, new.llm_analysis);
END;

CREATE TRIGGER IF NOT EXISTS algorithms_ad AFTER DELETE ON core_algorithms BEGIN
    INSERT INTO algorithms_fts(algorithms_fts, rowid, source_code, llm_analysis) 
    VALUES ('delete', old.id, old.source_code, old.llm_analysis);
END;

CREATE TRIGGER IF NOT EXISTS algorithms_au AFTER UPDATE ON core_algorithms BEGIN
    INSERT INTO algorithms_fts(algorithms_fts, rowid, source_code, llm_analysis) 
    VALUES ('delete', old.id, old.source_code, old.llm_analysis);
    INSERT INTO algorithms_fts(rowid, source_code, llm_analysis) 
    VALUES (new.id, new.source_code, new.llm_analysis);
END;
"""


def init_db(db_path: Path | None = None) -> None:
    """Initialize the database with schema."""
    path = db_path or get_db_path()
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


@contextmanager
def get_connection(db_path: Path | None = None) -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection with row factory."""
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


class Database:
    """Database access layer."""
    
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or get_db_path()
        init_db(self.db_path)
    
    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection."""
        with get_connection(self.db_path) as conn:
            yield conn
    
    def execute(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Execute a query and return results."""
        with self.connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.fetchall()
    
    def execute_many(self, sql: str, params_list: list[tuple]) -> None:
        """Execute a query with multiple parameter sets."""
        with self.connection() as conn:
            conn.executemany(sql, params_list)
            conn.commit()
    
    def insert(self, sql: str, params: tuple = ()) -> int:
        """Insert a row and return the last row id."""
        with self.connection() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
    
    def row_to_dict(self, row: sqlite3.Row) -> dict:
        """Convert a Row to a dictionary."""
        return dict(zip(row.keys(), row))
