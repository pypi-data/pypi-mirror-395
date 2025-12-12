"""
Search module for docfind.

Provides search functionality using SQLite FTS5 and optional ripgrep integration.
"""

import json
import logging
import subprocess
import re
from typing import Optional, List, Dict, Any, Generator
from pathlib import Path

from .db import DatabaseManager
from .utils import find_ripgrep

logger = logging.getLogger(__name__)


class SearchEngine:
    """Search engine with FTS5 and ripgrep support."""

    def __init__(self, db: DatabaseManager):
        """
        Initialize search engine.

        Args:
            db: Database manager
        """
        self.db = db
        self.rg_path = find_ripgrep()

    def search(
        self,
        query: str,
        use_ripgrep: bool = False,
        case_sensitive: bool = False,
        regex: bool = False,
        whole_word: bool = False,
        root_path: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search indexed documents.

        Args:
            query: Search query
            use_ripgrep: Use ripgrep for searching
            case_sensitive: Case-sensitive search
            regex: Treat query as regex
            whole_word: Match whole words only
            root_path: Filter by root path
            limit: Maximum results
            offset: Result offset

        Returns:
            List of search results
        """
        if use_ripgrep and self.rg_path:
            return self._search_with_ripgrep(
                query, case_sensitive, regex, whole_word, root_path, limit
            )
        else:
            return self._search_with_fts5(
                query, case_sensitive, whole_word, root_path, limit, offset
            )

    def _search_with_fts5(
        self,
        query: str,
        case_sensitive: bool,
        whole_word: bool,
        root_path: Optional[str],
        limit: int,
        offset: int,
    ) -> List[Dict[str, Any]]:
        """Search using FTS5."""
        # Build FTS5 query
        fts_query = self._build_fts5_query(query, whole_word)

        logger.debug(f"FTS5 query: {fts_query}")

        results = self.db.search(
            query=fts_query, root_path=root_path, limit=limit, offset=offset
        )

        # Post-process for case sensitivity
        if case_sensitive:
            results = [r for r in results if query in r.get("snippet", "")]

        return results

    def _build_fts5_query(self, query: str, whole_word: bool) -> str:
        """Build FTS5 query from search terms."""
        # Escape FTS5 special characters
        query = query.replace('"', '""')

        if whole_word:
            # Split into words and wrap each in quotes
            words = query.split()
            fts_query = " ".join([f'"{word}"' for word in words])
        else:
            # Use phrase query
            fts_query = f'"{query}"'

        return fts_query

    def _search_with_ripgrep(
        self,
        query: str,
        case_sensitive: bool,
        regex: bool,
        whole_word: bool,
        root_path: Optional[str],
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Search using ripgrep."""
        if not self.rg_path:
            logger.warning("ripgrep not available, falling back to FTS5")
            return self._search_with_fts5(
                query, case_sensitive, whole_word, root_path, limit, 0
            )

        # Get paths to search
        if root_path:
            roots = [root_path]
        else:
            # Get all indexed roots
            root_data = self.db.get_roots()
            roots = [r[0] for r in root_data]

        if not roots:
            logger.warning("No indexed paths to search")
            return []

        results = []

        for root in roots:
            try:
                rg_results = self._run_ripgrep(
                    query, root, case_sensitive, regex, whole_word, limit - len(results)
                )
                results.extend(rg_results)

                if len(results) >= limit:
                    break

            except Exception as e:
                logger.error(f"ripgrep search failed for {root}: {e}")
                continue

        return results[:limit]

    def _run_ripgrep(
        self,
        query: str,
        search_path: str,
        case_sensitive: bool,
        regex: bool,
        whole_word: bool,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Run ripgrep and parse results."""
        cmd = [self.rg_path, "--json"]

        # Add flags
        if not case_sensitive:
            cmd.append("-i")

        if not regex:
            cmd.append("-F")  # Fixed string search

        if whole_word:
            cmd.append("-w")

        # Add max count
        cmd.extend(["-m", str(limit)])

        # Add query and path
        cmd.append(query)
        cmd.append(search_path)

        logger.debug(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            return self._parse_ripgrep_json(result.stdout)

        except subprocess.TimeoutExpired:
            logger.error("ripgrep search timed out")
            return []
        except Exception as e:
            logger.error(f"ripgrep execution failed: {e}")
            return []

    def _parse_ripgrep_json(self, output: str) -> List[Dict[str, Any]]:
        """Parse ripgrep JSON output."""
        results = []

        for line in output.strip().split("\n"):
            if not line:
                continue

            try:
                obj = json.loads(line)

                if obj.get("type") == "match":
                    data = obj.get("data", {})
                    path_data = data.get("path", {})
                    line_number = data.get("line_number", 0)
                    lines = data.get("lines", {})
                    submatches = data.get("submatches", [])

                    # Extract match text
                    line_text = (
                        lines.get("text", "") if isinstance(lines, dict) else str(lines)
                    )

                    # Build snippet with context
                    snippet = line_text.strip()

                    # Get file info from database
                    file_path = (
                        path_data.get("text", "")
                        if isinstance(path_data, dict)
                        else str(path_data)
                    )
                    doc = self.db.get_document_by_path(file_path)

                    result = {
                        "path": file_path,
                        "line": line_number,
                        "snippet": snippet,
                        "source": "ripgrep",
                    }

                    # Add metadata from database if available
                    if doc:
                        result.update(
                            {
                                "id": doc.get("id"),
                                "source_type": doc.get("source_type"),
                                "extractor": doc.get("extractor"),
                                "file_size": doc.get("file_size"),
                                "mtime": doc.get("mtime"),
                                "root_path": doc.get("root_path"),
                            }
                        )

                    results.append(result)

            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse ripgrep JSON: {e}")
                continue

        return results

    def search_stream(
        self,
        query: str,
        use_ripgrep: bool = False,
        case_sensitive: bool = False,
        regex: bool = False,
        whole_word: bool = False,
        root_path: Optional[str] = None,
        batch_size: int = 50,
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Stream search results in batches.

        Args:
            query: Search query
            use_ripgrep: Use ripgrep
            case_sensitive: Case-sensitive search
            regex: Regex search
            whole_word: Whole word search
            root_path: Root path filter
            batch_size: Results per batch

        Yields:
            Batches of search results
        """
        if use_ripgrep and self.rg_path:
            # ripgrep returns all results at once
            results = self._search_with_ripgrep(
                query, case_sensitive, regex, whole_word, root_path, 10000
            )

            # Yield in batches
            for i in range(0, len(results), batch_size):
                yield results[i : i + batch_size]

        else:
            # FTS5 with pagination
            offset = 0
            while True:
                results = self._search_with_fts5(
                    query, case_sensitive, whole_word, root_path, batch_size, offset
                )

                if not results:
                    break

                yield results

                if len(results) < batch_size:
                    break

                offset += batch_size

    def explain_search(self, query: str) -> Dict[str, Any]:
        """
        Explain how a search query would be executed.

        Args:
            query: Search query

        Returns:
            Explanation dictionary
        """
        fts_query = self._build_fts5_query(query, False)

        explanation = {
            "original_query": query,
            "fts5_query": fts_query,
            "ripgrep_available": self.rg_path is not None,
            "ripgrep_path": self.rg_path,
        }

        # Get index stats
        stats = self.db.get_stats()
        explanation["index_stats"] = stats

        return explanation

    def get_document_text(self, doc_id: int) -> Optional[str]:
        """
        Get full extracted text for a document.

        Args:
            doc_id: Document ID

        Returns:
            Extracted text or None
        """
        doc = self.db.get_document(doc_id)
        if doc:
            return doc.get("extracted_text")
        return None

    def get_context(
        self, doc_id: int, query: str, context_lines: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get matching lines with context from a document.

        Args:
            doc_id: Document ID
            query: Search query
            context_lines: Lines of context before/after

        Returns:
            List of matches with context
        """
        text = self.get_document_text(doc_id)
        if not text:
            return []

        lines = text.split("\n")
        matches = []

        # Simple string matching (case-insensitive)
        query_lower = query.lower()

        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Extract context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)

                context_before = lines[start:i]
                context_after = lines[i + 1 : end]

                matches.append(
                    {
                        "line_number": i + 1,
                        "line": line,
                        "context_before": context_before,
                        "context_after": context_after,
                    }
                )

        return matches
