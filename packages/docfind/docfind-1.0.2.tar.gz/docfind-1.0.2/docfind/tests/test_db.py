"""
Tests for database module.
"""

import pytest
import tempfile
from pathlib import Path

from docfind.db import DatabaseManager


@pytest.fixture
def db():
    """Create temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = DatabaseManager(db_path)
    yield db
    db.close()

    # Cleanup
    if db_path.exists():
        db_path.unlink()


def test_database_creation(db):
    """Test database creation."""
    assert db.db_path.exists()


def test_insert_document(db):
    """Test document insertion."""
    doc_id = db.insert_document(
        path="/test/file.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Hello, world!",
        extractor="text",
        sha256="abc123",
        file_size=1024,
        mtime=123456.0,
        status="success",
    )

    assert doc_id > 0

    # Retrieve document
    doc = db.get_document(doc_id)
    assert doc is not None
    assert doc["path"] == "/test/file.txt"
    assert doc["extracted_text"] == "Hello, world!"


def test_search_documents(db):
    """Test document search."""
    # Insert test documents
    db.insert_document(
        path="/test/file1.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Python programming language",
        extractor="text",
    )

    db.insert_document(
        path="/test/file2.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="JavaScript web development",
        extractor="text",
    )

    # Search for "Python"
    results = db.search("Python")
    assert len(results) == 1
    assert results[0]["path"] == "/test/file1.txt"

    # Search for "programming"
    results = db.search("programming")
    assert len(results) == 1

    # Search for non-existent term
    results = db.search("Ruby")
    assert len(results) == 0


def test_get_document_by_path(db):
    """Test getting document by path."""
    db.insert_document(
        path="/test/unique.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Unique content",
        extractor="text",
    )

    doc = db.get_document_by_path("/test/unique.txt")
    assert doc is not None
    assert doc["path"] == "/test/unique.txt"

    # Non-existent path
    doc = db.get_document_by_path("/test/nonexistent.txt")
    assert doc is None


def test_delete_document(db):
    """Test document deletion."""
    doc_id = db.insert_document(
        path="/test/delete.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="To be deleted",
        extractor="text",
    )

    # Verify it exists
    doc = db.get_document(doc_id)
    assert doc is not None

    # Delete it
    db.delete_document(doc_id)

    # Verify it's gone
    doc = db.get_document(doc_id)
    assert doc is None


def test_delete_by_root(db):
    """Test deleting documents by root path."""
    # Insert documents with different roots
    db.insert_document(
        path="/root1/file.txt",
        root_path="/root1",
        source_type="txt",
        extracted_text="Root 1",
        extractor="text",
    )

    db.insert_document(
        path="/root2/file.txt",
        root_path="/root2",
        source_type="txt",
        extracted_text="Root 2",
        extractor="text",
    )

    # Delete root1
    db.delete_by_root("/root1")

    # Verify root1 is gone
    doc = db.get_document_by_path("/root1/file.txt")
    assert doc is None

    # Verify root2 still exists
    doc = db.get_document_by_path("/root2/file.txt")
    assert doc is not None


def test_get_roots(db):
    """Test getting indexed roots."""
    db.insert_document(
        path="/root1/file1.txt",
        root_path="/root1",
        source_type="txt",
        extracted_text="File 1",
        extractor="text",
    )

    db.insert_document(
        path="/root1/file2.txt",
        root_path="/root1",
        source_type="txt",
        extracted_text="File 2",
        extractor="text",
    )

    db.insert_document(
        path="/root2/file.txt",
        root_path="/root2",
        source_type="txt",
        extracted_text="File",
        extractor="text",
    )

    roots = db.get_roots()
    assert len(roots) == 2

    # Check counts
    root_dict = {r[0]: r[1] for r in roots}
    assert root_dict["/root1"] == 2
    assert root_dict["/root2"] == 1


def test_get_stats(db):
    """Test getting database statistics."""
    # Insert documents
    db.insert_document(
        path="/test/file.txt",
        root_path="/test",
        source_type="txt",
        extracted_text="Content",
        extractor="text",
        file_size=100,
    )

    db.insert_document(
        path="/test/file.pdf",
        root_path="/test",
        source_type="pdf",
        extracted_text="PDF content",
        extractor="pdfminer",
        file_size=200,
    )

    stats = db.get_stats()

    assert stats["total_docs"] == 2
    assert stats["total_size"] == 300
    assert stats["root_count"] == 1
    assert "by_type" in stats
    assert stats["by_type"]["txt"] == 1
    assert stats["by_type"]["pdf"] == 1
