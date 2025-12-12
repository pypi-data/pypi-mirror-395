"""
Database module for docfind.

Manages SQLite database with FTS5 full-text search for indexed documents.
Thread-safe design with connection pooling.
"""

import sqlite3
import threading
import logging
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Thread-safe SQLite database manager with FTS5 support.

    Uses connection-per-thread pattern for thread safety.
    """

    def __init__(self, db_path: Path):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._local = threading.local()
        self._lock = threading.Lock()
        self._ensure_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, "connection"):
            conn = sqlite3.connect(
                str(self.db_path), check_same_thread=False, timeout=30.0
            )
            conn.row_factory = sqlite3.Row
            # Enable FTS5
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            self._local.connection = conn
        return self._local.connection

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise

    def _ensure_database(self):
        """Create database schema if it doesn't exist."""
        with self._lock:
            conn = self._get_connection()

            # Main documents table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    root_path TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    extractor TEXT,
                    sha256 TEXT,
                    file_size INTEGER,
                    mtime REAL,
                    indexed_at REAL NOT NULL,
                    status TEXT DEFAULT 'success',
                    error_message TEXT
                )
            """
            )

            # FTS5 virtual table for full-text search
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
                USING fts5(
                    path,
                    content,
                    tokenize='porter unicode61'
                )
            """
            )

            # Extracted text table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS extracted_text (
                    document_id INTEGER PRIMARY KEY,
                    text TEXT,
                    FOREIGN KEY (document_id) REFERENCES documents(id)
                        ON DELETE CASCADE
                )
            """
            )

            # Indexes for performance
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_documents_path
                ON documents(path)
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_documents_root_path
                ON documents(root_path)
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_documents_mtime
                ON documents(mtime)
            """
            )

            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    def insert_document(
        self,
        path: str,
        root_path: str,
        source_type: str,
        extracted_text: str,
        extractor: Optional[str] = None,
        sha256: Optional[str] = None,
        file_size: Optional[int] = None,
        mtime: Optional[float] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> int:
        """
        Insert or update a document in the database.

        Args:
            path: File path
            root_path: Root directory being indexed
            source_type: File type/extension
            extracted_text: Extracted text content
            extractor: Name of extractor used
            sha256: File hash
            file_size: File size in bytes
            mtime: File modification time
            status: Index status ('success', 'error', 'skipped')
            error_message: Error message if status is 'error'

        Returns:
            Document ID
        """
        with self.transaction() as conn:
            # Check if document already exists
            existing = conn.execute(
                "SELECT id FROM documents WHERE path = ?", (path,)
            ).fetchone()

            if existing:
                doc_id = existing[0]
                # Update existing document
                conn.execute(
                    """
                    UPDATE documents
                    SET root_path=?, source_type=?, extractor=?, sha256=?,
                        file_size=?, mtime=?, indexed_at=?, status=?, error_message=?
                    WHERE id=?
                """,
                    (
                        root_path,
                        source_type,
                        extractor,
                        sha256,
                        file_size,
                        mtime,
                        datetime.now().timestamp(),
                        status,
                        error_message,
                        doc_id,
                    ),
                )
            else:
                # Insert new document
                cursor = conn.execute(
                    """
                    INSERT INTO documents
                    (path, root_path, source_type, extractor, sha256,
                     file_size, mtime, indexed_at, status, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        path,
                        root_path,
                        source_type,
                        extractor,
                        sha256,
                        file_size,
                        mtime,
                        datetime.now().timestamp(),
                        status,
                        error_message,
                    ),
                )
                doc_id = cursor.lastrowid

            # Update FTS content and extracted text
            if extracted_text and status == "success":
                # Delete old FTS entry if exists, then insert new one
                conn.execute("DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
                conn.execute(
                    "INSERT INTO documents_fts(rowid, path, content) VALUES (?, ?, ?)",
                    (doc_id, path, extracted_text),
                )

                # Store full extracted text separately
                conn.execute(
                    """
                    INSERT OR REPLACE INTO extracted_text
                    (document_id, text)
                    VALUES (?, ?)
                """,
                    (doc_id, extracted_text),
                )
            elif existing:
                # If updating but no text provided, delete FTS entries
                conn.execute("DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
                conn.execute(
                    "DELETE FROM extracted_text WHERE document_id = ?", (doc_id,)
                )

            return doc_id

    def search(
        self,
        query: str,
        root_path: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search documents using FTS5.

        Args:
            query: Search query (FTS5 syntax)
            root_path: Filter by root path
            limit: Maximum results to return
            offset: Result offset for pagination

        Returns:
            List of matching documents with metadata
        """
        conn = self._get_connection()

        sql = """
            SELECT
                d.id,
                d.path,
                d.root_path,
                d.source_type,
                d.extractor,
                d.sha256,
                d.file_size,
                d.mtime,
                d.indexed_at,
                d.status,
                snippet(documents_fts, 1, '<mark>', '</mark>', '...', 64) as snippet,
                bm25(documents_fts) as rank
            FROM documents_fts
            JOIN documents d ON documents_fts.rowid = d.id
            WHERE documents_fts MATCH ?
        """

        params: List[Any] = [query]

        if root_path:
            sql += " AND d.root_path = ?"
            params.append(root_path)

        sql += " ORDER BY rank LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor = conn.execute(sql, params)

        results = []
        for row in cursor:
            results.append(dict(row))

        return results

    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Get document by ID with full extracted text."""
        conn = self._get_connection()

        cursor = conn.execute(
            """
            SELECT
                d.*,
                et.text as extracted_text
            FROM documents d
            LEFT JOIN extracted_text et ON d.id = et.document_id
            WHERE d.id = ?
        """,
            (doc_id,),
        )

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_document_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        """Get document by file path."""
        conn = self._get_connection()

        cursor = conn.execute(
            """
            SELECT
                d.*,
                et.text as extracted_text
            FROM documents d
            LEFT JOIN extracted_text et ON d.id = et.document_id
            WHERE d.path = ?
        """,
            (path,),
        )

        row = cursor.fetchone()
        return dict(row) if row else None

    def delete_document(self, doc_id: int):
        """Delete document by ID."""
        with self.transaction() as conn:
            conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))

    def delete_by_root(self, root_path: str):
        """Delete all documents under a root path."""
        with self.transaction() as conn:
            conn.execute("DELETE FROM documents WHERE root_path = ?", (root_path,))

    def get_roots(self) -> List[Tuple[str, int, float]]:
        """
        Get all indexed root paths with document counts.

        Returns:
            List of (root_path, doc_count, last_indexed) tuples
        """
        conn = self._get_connection()

        cursor = conn.execute(
            """
            SELECT
                root_path,
                COUNT(*) as doc_count,
                MAX(indexed_at) as last_indexed
            FROM documents
            GROUP BY root_path
            ORDER BY last_indexed DESC
        """
        )

        return [
            (row["root_path"], row["doc_count"], row["last_indexed"]) for row in cursor
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self._get_connection()

        cursor = conn.execute(
            """
            SELECT
                COUNT(*) as total_docs,
                SUM(file_size) as total_size,
                COUNT(DISTINCT root_path) as root_count,
                COUNT(CASE WHEN status = 'error' THEN 1 END) as error_count
            FROM documents
        """
        )

        stats = dict(cursor.fetchone())

        # Get type breakdown
        cursor = conn.execute(
            """
            SELECT source_type, COUNT(*) as count
            FROM documents
            GROUP BY source_type
            ORDER BY count DESC
        """
        )

        stats["by_type"] = {row["source_type"]: row["count"] for row in cursor}

        return stats

    def optimize(self):
        """Optimize FTS index and vacuum database."""
        with self._lock:
            conn = self._get_connection()
            logger.info("Optimizing FTS index...")
            conn.execute("INSERT INTO documents_fts(documents_fts) VALUES('optimize')")
            logger.info("Vacuuming database...")
            conn.execute("VACUUM")
            conn.commit()
            logger.info("Database optimization complete")

    def close(self):
        """Close database connection."""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            delattr(self._local, "connection")
