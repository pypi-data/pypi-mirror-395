# DocFind

A powerful cross-platform document indexing and search tool with both CLI and GUI interfaces.

## Features

- **Smart Auto Mode** 🎯: Automatically chooses between full-text and metadata-only indexing based on folder size
- **Full-text search** using SQLite FTS5 for blazing-fast queries
- **Multi-format support**: PDF, DOCX, XLSX, PPTX, HTML, XML, and plain text
- **Unknown format handling**: Hex extraction for files with unrecognized formats
- **Ripgrep integration**: Lightning-fast search using ripgrep for large files
- **CLI and GUI**: Professional command-line and PyQt5 desktop interfaces
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Thread-safe indexing**: Efficient multi-threaded document processing with stop capability
- **Large file support**: Handles files up to 10 GB with intelligent truncation
- **Dark theme**: Modern, accessible dark UI with customizable accent colors
- **Real-time progress**: Live progress tracking with detailed logging

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
   - For metadata-only indexed documents, ripgrep is auto-enabled
   - If ripgrep is not installed, a helpful dialog appears with download instructions
3. **View results**: Click result → Preview automatically loads and switches to Preview tab
   - See file details (path, type, size, extractor)
   - View file content with highlighted search matches
   - Works for both database-indexed and ripgrep-only results
4. **Export**: Click "Export Results" → Choose format (CSV or JSONL) → Save
   - CSV format: Excel-compatible with headers
   - JSONL format: One JSON object per line for programmatic processing

**Settings:**

Access via `File → Settings` (or press `Ctrl+,`):

- **Threads**: Number of parallel indexing threads (1-32)
  - Lower values (1-2) recommended for very large files to avoid database locking
  - Higher values (4+) optimal for many small files
- **Max file size**: Maximum file size to process (up to 10 GB)
  - Files larger than 500 MB will have text truncated for database storage
- **Index mode**: Choose indexing strategy ⭐
  - **Auto (Recommended)**: Automatically selects best mode based on folder size
    - Uses Full Text for folders ≤100 MB
    - Uses Metadata Only for folders >100 MB
  - **Metadata Only (Fast)**: Only indexes file metadata, uses ripgrep for search
    - Lightning fast indexing (seconds instead of hours)
    - Perfect for very large files or massive document collections
    - Requires ripgrep for searching
  - **Full Text (Slow)**: Extracts and indexes all text content
    - Best for small to medium collections
    - Enables FTS5 search without external dependencies
- **Trust external tools**: Enable external conversion tools
- **Ripgrep path**: Path to ripgrep executable
- **UI accent color**: Customize interface color

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
  "threads": 2,
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
  "db_path": "<platform-specific-data-dir>/docfind.db",
  "index_mode": "auto",
  "auto_mode_threshold": 104857600
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

- **Index Mode**: Choose the right mode for your use case:
  - **Auto (Recommended)**: Automatically picks best mode based on folder size
  - **Metadata Only**: Lightning-fast indexing (10-20 seconds for hundreds of GB)
  - **Full Text**: Slower but enables FTS5 search without ripgrep
- **Threads**: Default is 2 to avoid database locking. Use `--threads 1` for very large files (>500 MB)
- **File size**: Limit with `--max-size` to skip very large files (default: 10 GB)
- **Ignore patterns**: Configure patterns for files/folders to skip
- **Reindex**: Only use `--reindex` when necessary (slower)

### Searching

- **Automatic mode detection**: GUI auto-enables ripgrep for metadata-only indexed documents
- **FTS5**: Fast for most queries, supports phrase search (full-text mode)
- **Ripgrep**: Lightning-fast for simple string matches, regex support (metadata-only mode)
- **Rich results**: File path, line numbers, and text snippets displayed in GUI
- **Pagination**: Use `--limit` and `--offset` for large result sets
- **Filters**: Use `--root` to narrow search scope

### Database

- **Optimize**: Run `docfind optimize` periodically to compact database
- **Backup**: Database is a single `.db` file - easy to backup
- **Location**: Store on SSD for better performance

## Troubleshooting

### "Database locked" errors

- Reduce number of indexing threads in settings (try 1 thread for very large files)
- Close other DocFind instances accessing the same database
- Use metadata-only mode for large file collections (skips heavy database writes)
- Database timeout is 60 seconds with automatic retry (3 attempts with exponential backoff)

### "ripgrep not found" or "Ripgrep Required" dialog

DocFind automatically enables ripgrep when searching metadata-only indexed documents. If ripgrep is not installed:

- **Easy Installation**: Click "Open Download Page" in the dialog to download ripgrep
- **Manual Download**: Visit https://github.com/BurntSushi/ripgrep/releases
- **Windows**: Download the .zip file, extract `rg.exe`, and add it to your PATH
- **Linux**: `sudo apt install ripgrep` (Ubuntu/Debian) or use your package manager
- **macOS**: `brew install ripgrep`
- **Custom path**: Specify path in Settings → Ripgrep path

After installation, restart DocFind to detect ripgrep automatically.

### GUI doesn't start

- Check PyQt5 installation: `pip install --upgrade PyQt5`
- On Linux, install: `sudo apt-get install python3-pyqt5`
- Check logs: `~/.local/share/docfind/docfind_gui.log` (Linux)

### Extraction fails for PDF/Office files

- Ensure dependencies are installed: `pip install -r requirements.txt`
- For legacy formats (.doc, .xls, .ppt), use hex extraction (automatic fallback)
- Check file isn't corrupted: Try opening in native application

### High memory usage

- Use metadata-only or auto mode instead of full-text mode
- Reduce `max_file_size` in config
- Use fewer indexing threads (1-2 instead of 4+)
- Process large directories in smaller batches

### Indexing is too slow

- **For large file collections (>100 MB total)**: Use Auto or Metadata Only mode
  - Metadata mode indexes hundreds of GB in 10-20 seconds
  - Only stores file paths and metadata (ripgrep searches actual files)
- **For small collections (<100 MB total)**: Use Full Text mode
  - Extracts and indexes all text content
  - Enables fast FTS5 search without external tools
- Check Settings → Index Mode to change behavior

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

### Version 1.1.0

Major performance improvements and bug fixes for large folder search:

#### 🚀 Performance Improvements
- **Smart Auto Mode**: Automatically chooses between full-text and metadata-only indexing based on folder size (100 MB threshold)
- **Lightning-fast indexing**:
  - First-time indexing: ~10 minutes for 285 GB (metadata-only mode)
  - Re-indexing unchanged files: Under 1 second (batch query + in-memory skip checks)
- **Performance optimizations**:
  - Skipped hash calculation in metadata-only mode (eliminates reading entire files)
  - Batch-load existing documents for skip checking (1 query vs 285 queries)
  - In-memory duplicate detection (nanoseconds vs milliseconds per file)

#### 🔍 Search Enhancements
- **Fixed ripgrep search for large folders (>100MB)**:
  - Metadata-only indexed documents now properly searched with ripgrep
  - Auto-detects metadata-only mode and enables ripgrep automatically
  - Fixed auto-enable logic to count ALL metadata-only documents (not just first)
  - Auto-checks ripgrep checkbox when enabled so users can see it's active
- **Enhanced debugging and logging**:
  - Detailed INFO-level logging for ripgrep command execution
  - Logs ripgrep return codes, output length, and parsed results count
  - Better error messages when ripgrep returns empty results or errors
  - Debug logging for JSON parsing showing each match found
- **Improved result handling**:
  - Files not in database now included in results with minimal metadata
  - Better error handling with full tracebacks in debug mode
  - Fixed JSON parsing to handle edge cases
- **Helpful ripgrep installation**:
  - Clear dialog if ripgrep is not found (with download link and instructions)
  - One-click "Open Download Page" button for easy installation
  - Shows count of metadata-only documents when auto-enabling
- **Rich search results**: File path, line numbers, and text snippets displayed in GUI

#### 💾 Database & File Handling
- **Large file support**: Increased max file size to 10 GB with automatic text truncation at 500 MB
- **Stop functionality**: Can now stop indexing operations in GUI with proper cleanup
- **Database improvements**:
  - Increased timeout from 30s to 60s
  - Added retry logic with exponential backoff for locked database
  - Reduced default threads from 4 to 2 to minimize locking issues
  - Batch metadata queries for 100x+ faster skip checking
- **Enhanced error handling**: Automatic truncation and retry for oversized text content

#### 🎨 UI/UX Improvements
- **Real-time progress**: Live progress tracking with detailed logging in GUI
- **Settings improvements**: Added index mode selector (Auto/Metadata Only/Full Text) with helpful tooltips
- **Better warnings**: Alert users when no files found due to size limits or patterns
- **Log console**: Detailed color-coded logs showing indexing and search operations
- **Auto-preview on click**: Clicking a search result automatically loads and displays the file preview
  - Automatically switches to Preview tab for better UX
  - Highlights search matches in the preview
  - Works for both database-indexed and ripgrep-only results
  - **Smart context loading**: For ripgrep results, shows ±50 lines around the match (not entire file)
  - Matched line is highlighted with ">>>" prefix and line numbers shown
  - **Chunked file reader for extremely large files (500+ GB)**:
    - Files >100 MB use memory-efficient line-by-line reading
    - Only reads the specific lines needed (±50 around match)
    - Prevents memory issues and crashes with massive files
    - Automatic detection and logging when chunked reader is activated
- **CSV export option**: Export search results as CSV (Excel-compatible) or JSONL
  - CSV includes headers and all result fields
  - JSONL maintains backward compatibility for programmatic processing

#### 🐛 Bug Fixes
- **Fixed search returning 0 results**: Ripgrep now properly searches files in folders >100MB
  - Fixed critical Unicode encoding error when ripgrep searches binary/mixed-encoding files
  - Added UTF-8 encoding with error replacement to handle all file types
  - Added `--text` flag to ripgrep to search binary files without errors
- **Fixed preview not loading for metadata-only indexed documents**:
  - Fixed empty string handling - now properly detects and falls back to file reading
  - Preview now works for all search results, whether from database or ripgrep
  - Added detailed logging to debug preview loading issues
- **Fixed test failures**: Added missing `existing_docs` parameter to `index_single_file` method
- **Fixed auto-enable detection**: Now correctly counts all metadata-only documents, not just the first one
- **Fixed NoneType error**: Safe handling when ripgrep stdout is None due to encoding issues

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
