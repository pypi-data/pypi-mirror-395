"""
Tests for indexer module.
"""

import pytest
import tempfile
from pathlib import Path

from docfind.db import DatabaseManager
from docfind.indexer import DocumentIndexer, TextExtractor
from docfind.hex_extractor import HexExtractor


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def db():
    """Create temporary database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = DatabaseManager(db_path)
    yield db
    db.close()

    if db_path.exists():
        db_path.unlink()


def test_text_extractor_plain_text(temp_dir):
    """Test extracting plain text."""
    # Create test file
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, world!", encoding="utf-8")

    extractor = TextExtractor()
    text, extractor_name = extractor.extract(test_file, "txt")

    assert text == "Hello, world!"
    assert "text" in extractor_name


def test_text_extractor_unknown_format(temp_dir):
    """Test extracting from unknown format using hex extraction."""
    # Create binary file with some text
    test_file = temp_dir / "test.bin"
    test_file.write_bytes(b"\x00\x01Hello\x00World\xff")

    extractor = TextExtractor()
    text, extractor_name = extractor.extract(test_file, "bin")

    assert "Hello" in text
    assert "World" in text
    assert extractor_name == "hex-extractor"


def test_hex_extractor():
    """Test hex extractor."""
    data = b"\x00\x01\x02Python Programming\x00\xff\xfeTest Data\x00"

    extractor = HexExtractor(min_length=4)
    text = extractor.extract_from_bytes(data)

    assert "Python Programming" in text
    assert "Test Data" in text


def test_document_indexer_single_file(temp_dir, db):
    """Test indexing a single file."""
    # Create test file
    test_file = temp_dir / "test.txt"
    test_file.write_text("Test document content", encoding="utf-8")

    indexer = DocumentIndexer(db)
    success = indexer.index_single_file(test_file, temp_dir)

    assert success

    # Verify in database
    doc = db.get_document_by_path(str(test_file))
    assert doc is not None
    assert "Test document content" in doc["extracted_text"]


def test_document_indexer_directory(temp_dir, db):
    """Test indexing a directory."""
    # Create test files
    (temp_dir / "file1.txt").write_text("Content 1", encoding="utf-8")
    (temp_dir / "file2.txt").write_text("Content 2", encoding="utf-8")
    (temp_dir / "file3.md").write_text("# Markdown", encoding="utf-8")

    # Create subdirectory
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    (subdir / "file4.txt").write_text("Content 4", encoding="utf-8")

    indexer = DocumentIndexer(db)
    progress = indexer.index_directory(temp_dir, threads=1)

    assert progress.total_files == 4
    assert progress.successful == 4
    assert progress.failed == 0

    # Verify all files in database
    stats = db.get_stats()
    assert stats["total_docs"] == 4


def test_document_indexer_ignore_patterns(temp_dir, db):
    """Test ignoring files based on patterns."""
    # Create test files
    (temp_dir / "file.txt").write_text("Keep this", encoding="utf-8")
    (temp_dir / "file.pyc").write_text("Ignore this", encoding="utf-8")
    (temp_dir / "test.log").write_text("Ignore this", encoding="utf-8")

    indexer = DocumentIndexer(db, ignore_patterns=["*.pyc", "*.log"])
    progress = indexer.index_directory(temp_dir, threads=1)

    assert progress.total_files == 1
    assert progress.successful == 1

    # Verify only txt file indexed
    stats = db.get_stats()
    assert stats["total_docs"] == 1


def test_document_indexer_max_file_size(temp_dir, db):
    """Test max file size limit."""
    # Create small file
    small_file = temp_dir / "small.txt"
    small_file.write_text("x" * 100, encoding="utf-8")

    # Create large file
    large_file = temp_dir / "large.txt"
    large_file.write_text("x" * 10000, encoding="utf-8")

    indexer = DocumentIndexer(db, max_file_size=1000)
    progress = indexer.index_directory(temp_dir, threads=1)

    # Only small file should be indexed
    assert progress.total_files == 1
    assert progress.successful == 1

    stats = db.get_stats()
    assert stats["total_docs"] == 1


def test_document_indexer_reindex(temp_dir, db):
    """Test reindexing."""
    import time
    import os

    test_file = temp_dir / "test.txt"
    test_file.write_text("Original content", encoding="utf-8")

    indexer = DocumentIndexer(db)

    # First index
    indexer.index_single_file(test_file, temp_dir)

    doc = db.get_document_by_path(str(test_file))
    assert "Original content" in doc["extracted_text"]

    # Wait to ensure mtime changes (Windows filesystem has low resolution)
    time.sleep(0.1)

    # Modify file
    test_file.write_text("Updated content", encoding="utf-8")

    # Ensure mtime is updated by touching the file
    os.utime(test_file, None)
    time.sleep(0.1)

    # Reindex
    indexer.index_single_file(test_file, temp_dir)

    doc = db.get_document_by_path(str(test_file))
    assert "Updated content" in doc["extracted_text"]
