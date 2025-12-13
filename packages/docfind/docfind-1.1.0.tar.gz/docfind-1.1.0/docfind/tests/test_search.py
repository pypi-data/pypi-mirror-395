"""
Tests for search module.
"""

import pytest
import tempfile
from pathlib import Path

from docfind.db import DatabaseManager
from docfind.search import SearchEngine


@pytest.fixture
def db_with_data():
    """Create database with test data."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = DatabaseManager(db_path)

    # Insert test documents
    db.insert_document(
        path="/test/python.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Python is a high-level programming language. It is widely used for web development, data science, and automation.",
        extractor="text",
    )

    db.insert_document(
        path="/test/javascript.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="JavaScript is a scripting language for web pages. It runs in the browser and enables interactive web applications.",
        extractor="text",
    )

    db.insert_document(
        path="/test/java.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Java is an object-oriented programming language. It is used for enterprise applications and Android development.",
        extractor="text",
    )

    yield db

    db.close()
    if db_path.exists():
        db_path.unlink()


def test_search_basic(db_with_data):
    """Test basic search."""
    search = SearchEngine(db_with_data)

    results = search.search("Python")
    assert len(results) == 1
    assert results[0]["path"] == "/test/python.txt"


def test_search_multiple_results(db_with_data):
    """Test search returning multiple results."""
    search = SearchEngine(db_with_data)

    results = search.search("programming")
    assert len(results) == 2  # Python and Java


def test_search_no_results(db_with_data):
    """Test search with no results."""
    search = SearchEngine(db_with_data)

    results = search.search("Ruby")
    assert len(results) == 0


def test_search_with_limit(db_with_data):
    """Test search with result limit."""
    search = SearchEngine(db_with_data)

    results = search.search("programming", limit=1)
    assert len(results) == 1


def test_search_with_root_filter(db_with_data):
    """Test search filtered by root path."""
    # Add document with different root
    db_with_data.insert_document(
        path="/other/python.txt",
        root_path="/other",
        source_type="txt",
        extracted_text="Python in another root",
        extractor="text",
    )

    search = SearchEngine(db_with_data)

    # Search all roots
    results = search.search("Python")
    assert len(results) == 2

    # Search specific root
    results = search.search("Python", root_path="/test")
    assert len(results) == 1
    assert results[0]["root_path"] == "/test"


def test_get_document_text(db_with_data):
    """Test getting full document text."""
    search = SearchEngine(db_with_data)

    # Get document
    doc = db_with_data.get_document_by_path("/test/python.txt")
    doc_id = doc["id"]

    text = search.get_document_text(doc_id)
    assert text is not None
    assert "Python" in text
    assert "programming language" in text


def test_get_context(db_with_data):
    """Test getting search context."""
    search = SearchEngine(db_with_data)

    doc = db_with_data.get_document_by_path("/test/python.txt")
    doc_id = doc["id"]

    matches = search.get_context(doc_id, "Python", context_lines=1)
    assert len(matches) > 0
    assert "Python" in matches[0]["line"]


def test_explain_search(db_with_data):
    """Test search explanation."""
    search = SearchEngine(db_with_data)

    explanation = search.explain_search("Python programming")

    assert "original_query" in explanation
    assert "fts5_query" in explanation
    assert "index_stats" in explanation
    assert explanation["original_query"] == "Python programming"


def test_search_stream(db_with_data):
    """Test streaming search results."""
    search = SearchEngine(db_with_data)

    batches = list(search.search_stream("programming", batch_size=1))

    # Should have 2 batches (2 results with batch_size=1)
    assert len(batches) == 2
    assert len(batches[0]) == 1
    assert len(batches[1]) == 1


def test_build_fts5_query(db_with_data):
    """Test FTS5 query building."""
    search = SearchEngine(db_with_data)

    # Simple query
    query = search._build_fts5_query("test", whole_word=False)
    assert query == '"test"'

    # Whole word query
    query = search._build_fts5_query("test query", whole_word=True)
    assert '"test"' in query
    assert '"query"' in query
