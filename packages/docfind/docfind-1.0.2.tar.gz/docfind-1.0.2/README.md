# DocFind

A powerful cross-platform document indexing and search tool with both CLI and GUI interfaces.

## Features

- **Full-text search** using SQLite FTS5 for blazing-fast queries
- **Multi-format support**: PDF, DOCX, XLSX, PPTX, HTML, XML, and plain text
- **Unknown format handling**: Hex extraction for files with unrecognized formats
- **Ripgrep integration**: Optional integration with ripgrep for enhanced search
- **CLI and GUI**: Professional command-line and PyQt5 desktop interfaces
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Thread-safe indexing**: Efficient multi-threaded document processing
- **Dark theme**: Modern, accessible dark UI with customizable accent colors

## Installation

### Prerequisites

- Python 3.8 or higher
- (Optional) [ripgrep](https://github.com/BurntSushi/ripgrep) for enhanced search

### Install from PyPI

```bash
pip install docfind
```

### Verify Installation

```bash
# Check CLI is available
docfind --help

# Launch GUI
docfind-gui
```

## Quick Start

### CLI Usage

#### Index documents

```bash
# Index a directory
docfind index /path/to/documents

# Index with progress display
docfind index /path/to/documents --progress

# Reindex existing documents
docfind index /path/to/documents --reindex

# Use multiple threads (default: 4)
docfind index /path/to/documents --threads 8

# Set maximum file size (in bytes)
docfind index /path/to/documents --max-size 52428800  # 50MB
```

#### Search documents

```bash
# Basic search
docfind search "python programming"

# Case-sensitive search
docfind search "Python" --case-sensitive

# Regex search
docfind search "func.*\(" --regex

# Whole word search
docfind search "test" --whole-word

# Use ripgrep for searching
docfind search "error" --use-ripgrep

# JSON output (JSONL format)
docfind search "data" --json

# Limit results
docfind search "query" --limit 50

# Filter by root path
docfind search "term" --root /path/to/documents
```

#### List indexed paths

```bash
# Show all indexed paths
docfind list

# JSON output
docfind list --json
```

#### Show statistics

```bash
# Display database statistics
docfind stats

# JSON output
docfind stats --json
```

#### Explain queries or documents

```bash
# Explain how a query would be executed
docfind explain --query "search term"

# Explain a specific document
docfind explain --path /path/to/file.pdf

# Show extracted text preview
docfind explain --path /path/to/file.pdf --show-text
```

#### Remove indexed data

```bash
# Remove specific root path
docfind remove --path /path/to/documents

# Remove all indexed data
docfind remove --all --force
```

#### Optimize database

```bash
# Optimize FTS index and vacuum database
docfind optimize
```

#### System check

```bash
# Check system configuration and dependencies
docfind doctor
```

### GUI Usage

Launch the GUI application:

```bash
docfind-gui
```

#### GUI Features

**Main Window Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│ File  Tools  Help                                           │
├───────────┬─────────────────────────────────┬───────────────┤
│           │ [Search...] [Options] [Actions] │               │
│ Projects  ├─────────────────────────────────┤ File Details  │
│           │                                 │               │
│ • /docs/  │      Results Table              │ Path: ...     │
│   (1234)  │                                 │ Type: pdf     │
│           │  Path | Type | Line | Snippet  │ Size: 2.3 MB  │
│ • /work/  │  ─────┼──────┼──────┼────────  │               │
│   (567)   │  ...  │ pdf  │  42  │ text..  │ [Actions]     │
│           │                                 │               │
│ [Add]     │                                 │ • Open Folder │
│ [Remove]  │      Preview / Text             │ • Copy Path   │
│           │                                 │ • Export      │
│           │  Extracted text with            │               │
│           │  highlighted matches...         │               │
│           │                                 │               │
├───────────┴─────────────────────────────────┴───────────────┤
│ [Progress Bar]                                              │
│ Log Console:                                                │
│ [12:34:56] [INFO] Indexing started...                       │
└─────────────────────────────────────────────────────────────┘
```

**Keyboard Shortcuts:**

- `Ctrl+F` - Focus search box
- `Ctrl+I` - Add folder to index
- `Ctrl+E` - Export results
- `Ctrl+,` - Open settings
- `Ctrl+Q` - Quit

**Workflow:**

1. **Add a folder**: Click "Add Folder" → Select directory → Index starts automatically
2. **Search**: Type in search box → Results appear in real-time (debounced)
3. **View results**: Click result → See details and preview with highlighted matches
4. **Export**: Select results → Click "Export Results" → Save as JSONL

**Settings:**

Access via `File → Settings`:

- Number of indexing threads
- Maximum file size to index
- Trust external conversion tools
- Ripgrep path
- UI accent color

## Supported File Formats

### Native Support

| Format | Extensions | Extractor |
|--------|-----------|-----------|
| PDF | `.pdf` | pdfminer.six |
| Word | `.docx` | python-docx |
| Excel | `.xlsx` | openpyxl |
| PowerPoint | `.pptx` | python-pptx |
| HTML | `.html`, `.htm` | beautifulsoup4 |
| XML | `.xml` | beautifulsoup4 |
| Text | `.txt`, `.md`, `.rst`, `.log` | Native |
| Source Code | `.py`, `.js`, `.java`, `.c`, `.cpp`, `.h`, `.cs`, `.go`, `.rs`, `.rb`, `.php`, `.sh`, `.bat`, `.ps1` | Native |
| Data | `.json`, `.csv` | Native |

### Fallback Support

For unknown file formats, DocFind uses **hex extraction** to extract readable ASCII/UTF-16 text strings from binary files.

### Legacy Formats

- `.doc`, `.xls`, `.ppt` - Extracted via hex extractor (native support requires external tools)

## Architecture

### Core Components

DocFind consists of several key modules:

- **CLI Interface** (`docfind`): Command-line tool for indexing and searching
- **GUI Application** (`docfind-gui`): PyQt5 desktop application with dark theme
- **Database Layer**: SQLite with FTS5 full-text search engine
- **Document Indexer**: Multi-threaded extraction and indexing engine
- **Search Engine**: Supports both FTS5 and optional ripgrep integration
- **Format Extractors**: PDF, Office, HTML, text, and hex-based fallback

### Database Schema

**documents table:**
- Stores file metadata (path, type, size, hash, mtime, status)
- Tracks indexing status and errors

**documents_fts (FTS5 virtual table):**
- Full-text search index with Porter stemming
- Unicode tokenization for international text
- BM25 ranking for relevance scoring

**extracted_text table:**
- Stores complete extracted text for preview
- Linked to documents via foreign key

### Threading Model

**GUI Application:**
- Main Thread: UI updates and user interaction
- IndexWorker Thread: Background document indexing with progress signals
- SearchWorker Thread: Async search operations
- Database: Thread-local connections with WAL mode for concurrent access

**CLI Application:**
- Main Thread: User interface and coordination
- ThreadPoolExecutor: Parallel document processing (configurable thread count)
- Database: Thread-safe with connection pooling

## Configuration

Configuration is stored in platform-specific locations:

- **Windows**: `%APPDATA%\docfind\config.json`
- **macOS**: `~/Library/Application Support/docfind/config.json`
- **Linux**: `~/.config/docfind/config.json`

### Default Configuration

```json
{
  "max_file_size": 104857600,
  "threads": 4,
  "ignore_globs": [
    "*.pyc",
    "__pycache__",
    ".git",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "*.log"
  ],
  "trust_external_tools": false,
  "ripgrep_path": "rg",
  "theme": "dark",
  "accent_color": "#3a7bd5",
  "db_path": "<platform-specific-data-dir>/docfind.db"
}
```

## Advanced Usage

### Custom Configuration

You can customize DocFind behavior by editing the configuration file:

```bash
# Linux/macOS
~/.config/docfind/config.json

# Windows
%APPDATA%\docfind\config.json
```

### Database Location

By default, the database is stored in:

```bash
# Linux
~/.local/share/docfind/docfind.db

# macOS
~/Library/Application Support/docfind/docfind.db

# Windows
%LOCALAPPDATA%\docfind\docfind.db
```

You can back up this single file to preserve your entire index.

### Environment Variables

- `DOCFIND_DB_PATH`: Override default database location
- `DOCFIND_CONFIG_PATH`: Override default config location
- `DOCFIND_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Performance Tips

### Indexing

- **Threads**: Use `--threads` to match your CPU cores (default: 4)
- **File size**: Limit with `--max-size` to skip very large files
- **Ignore patterns**: Configure patterns for files/folders to skip
- **Reindex**: Only use `--reindex` when necessary (slower)

### Searching

- **FTS5**: Fast for most queries, supports phrase search
- **Ripgrep**: Faster for simple string matches, regex support
- **Pagination**: Use `--limit` and `--offset` for large result sets
- **Filters**: Use `--root` to narrow search scope

### Database

- **Optimize**: Run `docfind optimize` periodically to compact database
- **Backup**: Database is a single `.db` file - easy to backup
- **Location**: Store on SSD for better performance

## Troubleshooting

### "Database locked" errors

- Close other DocFind instances accessing the same database
- Check for stale lock files
- Increase timeout in db.py (default: 30s)

### "ripgrep not found" warnings

- Install ripgrep: https://github.com/BurntSushi/ripgrep
- Or specify path in config: `"ripgrep_path": "/path/to/rg"`

### GUI doesn't start

- Check PyQt5 installation: `pip install --upgrade PyQt5`
- On Linux, install: `sudo apt-get install python3-pyqt5`
- Check logs: `~/.local/share/docfind/docfind_gui.log` (Linux)

### Extraction fails for PDF/Office files

- Ensure dependencies are installed: `pip install -r requirements.txt`
- For legacy formats (.doc, .xls, .ppt), use hex extraction (automatic fallback)
- Check file isn't corrupted: Try opening in native application

### High memory usage

- Reduce `max_file_size` in config
- Use fewer indexing threads
- Process large directories in smaller batches

## Security Considerations

- **External tools**: Disabled by default (`trust_external_tools: false`)
- **System paths**: GUI warns before indexing system directories
- **Network drives**: Warning displayed before indexing
- **File execution**: DocFind never executes indexed files
- **SQL injection**: Parameterized queries prevent injection


## License

MIT License - see LICENSE file for details.

## Credits

Built with:
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [SQLite FTS5](https://www.sqlite.org/fts5.html) - Full-text search
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six) - PDF extraction
- [python-docx](https://python-docx.readthedocs.io/) - DOCX extraction
- [openpyxl](https://openpyxl.readthedocs.io/) - XLSX extraction
- [python-pptx](https://python-pptx.readthedocs.io/) - PPTX extraction
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML parsing
- [ripgrep](https://github.com/BurntSushi/ripgrep) - Optional fast search

## Changelog

### Version 1.0.2

Metadata and configuration updates:
- Updated project URLs to cmdeniz.dev homepage
- Cleaned up package metadata

### Version 1.0.1

Bug fixes and improvements:
- Fixed FTS5 database schema issue causing "no such column: T.content" error
- Fixed GUI tests crashing on Linux CI environments
- Fixed reindex test timing issues on Windows
- Improved database update logic for document reindexing
- Updated README for PyPI publication

### Version 1.0.0

Initial release with:
- Full-text search using SQLite FTS5 with BM25 ranking
- CLI and PyQt5 GUI interfaces
- Support for PDF, DOCX, XLSX, PPTX, HTML, XML, and text files
- Hex extraction fallback for unknown formats
- Multi-threaded indexing with progress tracking
- Optional ripgrep integration for fast regex search
- Cross-platform support (Windows, macOS, Linux)
- Dark theme GUI with customizable accents
- Thread-safe database with WAL mode
- Comprehensive test suite (30+ tests)

## Support

For issues, questions, or feature requests, please visit:
- **PyPI Package**: https://pypi.org/project/docfind/
- **GitHub Issues**: https://github.com/CihanMertDeniz/docfind/issues
- **Documentation**: Full documentation available in this README

---

**DocFind** - Find anything in your documents, instantly. 🔍
