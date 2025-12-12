"""
PyQt5 GUI for docfind.

Professional dark-themed desktop application for document indexing and search.
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QLabel,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QListWidget,
    QTabWidget,
    QGroupBox,
    QSpinBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHeaderView,
    QAbstractItemView,
    QMenu,
    QAction,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSettings, pyqtSlot
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QKeySequence

from . import __version__
from .db import DatabaseManager
from .indexer import DocumentIndexer, IndexProgress
from .search import SearchEngine
from .utils import Config, get_default_db_path, format_size, is_system_path

logger = logging.getLogger(__name__)


class IndexWorker(QThread):
    """Worker thread for indexing operations."""

    progress_update = pyqtSignal(object)  # IndexProgress
    finished = pyqtSignal(object)  # Final IndexProgress
    error = pyqtSignal(str)  # Error message
    log = pyqtSignal(str, str)  # level, message

    def __init__(
        self, db: DatabaseManager, root_path: Path, reindex: bool, config: Config
    ):
        super().__init__()
        self.db = db
        self.root_path = root_path
        self.reindex = reindex
        self.config = config
        self._stop_requested = False

    def run(self):
        """Run indexing in thread."""
        try:
            self.log.emit("info", f"Starting index of {self.root_path}")

            indexer = DocumentIndexer(
                db=self.db,
                max_file_size=self.config["max_file_size"],
                trust_external_tools=self.config["trust_external_tools"],
                ignore_patterns=self.config["ignore_globs"],
            )

            def progress_callback(progress):
                if not self._stop_requested:
                    self.progress_update.emit(progress)

            progress = indexer.index_directory(
                root_path=self.root_path,
                reindex=self.reindex,
                threads=self.config["threads"],
                progress_callback=progress_callback,
            )

            if self._stop_requested:
                self.log.emit("warning", "Indexing stopped by user")
            else:
                self.log.emit(
                    "info", f"Indexing complete: {progress.successful} files indexed"
                )

            self.finished.emit(progress)

        except Exception as e:
            self.log.emit("error", f"Indexing failed: {e}")
            self.error.emit(str(e))

    def stop(self):
        """Request stop."""
        self._stop_requested = True


class SearchWorker(QThread):
    """Worker thread for search operations."""

    results = pyqtSignal(list)  # Search results
    finished = pyqtSignal()
    error = pyqtSignal(str)
    log = pyqtSignal(str, str)

    def __init__(self, search_engine: SearchEngine, query: str, options: dict):
        super().__init__()
        self.search_engine = search_engine
        self.query = query
        self.options = options

    def run(self):
        """Run search in thread."""
        try:
            self.log.emit("info", f"Searching for: {self.query}")

            results = self.search_engine.search(query=self.query, **self.options)

            self.results.emit(results)
            self.log.emit("info", f"Found {len(results)} results")
            self.finished.emit()

        except Exception as e:
            self.log.emit("error", f"Search failed: {e}")
            self.error.emit(str(e))
            self.finished.emit()


class SettingsDialog(QDialog):
    """Settings dialog."""

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        layout = QFormLayout()

        # Threads
        self.threads_spin = QSpinBox()
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(32)
        self.threads_spin.setValue(self.config["threads"])
        layout.addRow("Threads:", self.threads_spin)

        # Max file size
        self.max_size_spin = QSpinBox()
        self.max_size_spin.setMinimum(1)
        self.max_size_spin.setMaximum(1000)
        self.max_size_spin.setValue(self.config["max_file_size"] // (1024 * 1024))
        self.max_size_spin.setSuffix(" MB")
        layout.addRow("Max file size:", self.max_size_spin)

        # Trust external tools
        self.trust_check = QCheckBox()
        self.trust_check.setChecked(self.config["trust_external_tools"])
        layout.addRow("Trust external tools:", self.trust_check)

        # Ripgrep path
        self.rg_path_edit = QLineEdit()
        self.rg_path_edit.setText(self.config["ripgrep_path"])
        layout.addRow("Ripgrep path:", self.rg_path_edit)

        # Accent color
        self.accent_edit = QLineEdit()
        self.accent_edit.setText(self.config["accent_color"])
        layout.addRow("Accent color:", self.accent_edit)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def get_settings(self) -> dict:
        """Get settings from dialog."""
        return {
            "threads": self.threads_spin.value(),
            "max_file_size": self.max_size_spin.value() * 1024 * 1024,
            "trust_external_tools": self.trust_check.isChecked(),
            "ripgrep_path": self.rg_path_edit.text(),
            "accent_color": self.accent_edit.text(),
        }


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DocFind {__version__}")
        self.setGeometry(100, 100, 1400, 900)

        # Configuration
        self.config = Config()

        # Database
        db_path = Path(self.config["db_path"])
        self.db = DatabaseManager(db_path)

        # Search engine
        self.search_engine = SearchEngine(self.db)

        # Workers
        self.index_worker: Optional[IndexWorker] = None
        self.search_worker: Optional[SearchWorker] = None

        # Search debounce timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

        # Current results
        self.current_results = []

        # Initialize UI
        self.init_ui()
        self.load_stylesheet()
        self.load_roots()

        # Settings
        self.settings = QSettings("DocFind", "DocFind")
        self.restore_geometry()

    def init_ui(self):
        """Initialize user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left sidebar
        sidebar = self.create_sidebar()
        splitter.addWidget(sidebar)

        # Center area
        center = self.create_center_area()
        splitter.addWidget(center)

        # Right panel
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Set splitter sizes
        splitter.setSizes([250, 800, 350])

        # Create status bar
        self.statusBar().showMessage("Ready")

        # Create menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        settings_action = QAction("&Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        index_action = QAction("&Index", self)
        index_action.setShortcut(QKeySequence("Ctrl+I"))
        index_action.triggered.connect(self.add_folder)
        tools_menu.addAction(index_action)

        optimize_action = QAction("&Optimize Database", self)
        optimize_action.triggered.connect(self.optimize_database)
        tools_menu.addAction(optimize_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_sidebar(self) -> QWidget:
        """Create left sidebar."""
        sidebar = QWidget()
        layout = QVBoxLayout()
        sidebar.setLayout(layout)

        # Title
        title = QLabel("Projects")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        layout.addWidget(title)

        # Roots list
        self.roots_list = QListWidget()
        self.roots_list.itemSelectionChanged.connect(self.on_root_selected)
        layout.addWidget(self.roots_list)

        # Buttons
        btn_layout = QVBoxLayout()

        self.btn_add_folder = QPushButton("Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        btn_layout.addWidget(self.btn_add_folder)

        self.btn_remove_folder = QPushButton("Remove")
        self.btn_remove_folder.clicked.connect(self.remove_folder)
        btn_layout.addWidget(self.btn_remove_folder)

        layout.addLayout(btn_layout)

        return sidebar

    def create_center_area(self) -> QWidget:
        """Create center area."""
        center = QWidget()
        layout = QVBoxLayout()
        center.setLayout(layout)

        # Toolbar
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Results tab
        results_widget = self.create_results_tab()
        self.tabs.addTab(results_widget, "Results")

        # Preview tab
        preview_widget = self.create_preview_tab()
        self.tabs.addTab(preview_widget, "Preview")

        # Bottom: Progress and logs
        bottom = self.create_bottom_area()
        layout.addWidget(bottom)

        return center

    def create_toolbar(self) -> QWidget:
        """Create toolbar."""
        toolbar = QWidget()
        layout = QHBoxLayout()
        toolbar.setLayout(layout)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.returnPressed.connect(self.perform_search)
        layout.addWidget(self.search_input)

        # Search options
        self.cb_case = QCheckBox("Match Case")
        layout.addWidget(self.cb_case)

        self.cb_regex = QCheckBox("Regex")
        layout.addWidget(self.cb_regex)

        self.cb_whole = QCheckBox("Whole Word")
        layout.addWidget(self.cb_whole)

        self.cb_ripgrep = QCheckBox("Use rg")
        layout.addWidget(self.cb_ripgrep)

        # Buttons
        self.btn_index = QPushButton("Index")
        self.btn_index.clicked.connect(self.start_index)
        layout.addWidget(self.btn_index)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop_index)
        self.btn_stop.setEnabled(False)
        layout.addWidget(self.btn_stop)

        return toolbar

    def create_results_tab(self) -> QWidget:
        """Create results tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(
            ["Path", "Type", "Line", "Snippet", "Modified"]
        )
        self.results_table.horizontalHeader().setStretchLastSection(False)
        self.results_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.Stretch
        )
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.itemSelectionChanged.connect(self.on_result_selected)
        self.results_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(
            self.show_result_context_menu
        )
        layout.addWidget(self.results_table)

        return widget

    def create_preview_tab(self) -> QWidget:
        """Create preview tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Toolbar
        toolbar = QHBoxLayout()

        self.btn_copy_text = QPushButton("Copy Text")
        self.btn_copy_text.clicked.connect(self.copy_preview_text)
        toolbar.addWidget(self.btn_copy_text)

        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Preview text
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.preview_text)

        return widget

    def create_right_panel(self) -> QWidget:
        """Create right panel."""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Details group
        details_group = QGroupBox("File Details")
        details_layout = QVBoxLayout()
        details_group.setLayout(details_layout)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(200)
        details_layout.addWidget(self.details_text)

        layout.addWidget(details_group)

        # Actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        actions_group.setLayout(actions_layout)

        self.btn_open_folder = QPushButton("Open Folder")
        self.btn_open_folder.clicked.connect(self.open_file_location)
        actions_layout.addWidget(self.btn_open_folder)

        self.btn_copy_path = QPushButton("Copy Path")
        self.btn_copy_path.clicked.connect(self.copy_file_path)
        actions_layout.addWidget(self.btn_copy_path)

        self.btn_export = QPushButton("Export Results")
        self.btn_export.clicked.connect(self.export_results)
        actions_layout.addWidget(self.btn_export)

        layout.addWidget(actions_group)

        layout.addStretch()

        return panel

    def create_bottom_area(self) -> QWidget:
        """Create bottom area with progress and logs."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Log console
        log_label = QLabel("Log Console")
        log_label.setStyleSheet("font-weight: bold; padding: 4px;")
        layout.addWidget(log_label)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setMaximumHeight(150)
        self.log_console.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_console)

        return widget

    def load_stylesheet(self):
        """Load dark theme stylesheet."""
        qss_path = Path(__file__).parent / "resources" / "qss" / "dark_theme.qss"

        if qss_path.exists():
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            # Fallback inline stylesheet
            self.setStyleSheet(
                """
                QWidget {
                    background-color: #0f1113;
                    color: #d8dee9;
                }
                QMainWindow {
                    background-color: #0f1113;
                }
                QPushButton {
                    background-color: #1e2124;
                    border: 1px solid #2d3135;
                    border-radius: 4px;
                    padding: 6px 12px;
                    color: #d8dee9;
                }
                QPushButton:hover {
                    background-color: #2d3135;
                }
                QPushButton:pressed {
                    background-color: #3a7bd5;
                }
                QLineEdit {
                    background-color: #1e2124;
                    border: 1px solid #2d3135;
                    border-radius: 4px;
                    padding: 6px;
                    color: #d8dee9;
                }
                QTableWidget {
                    background-color: #1e2124;
                    alternate-background-color: #252830;
                    border: 1px solid #2d3135;
                    gridline-color: #2d3135;
                }
                QTableWidget::item:selected {
                    background-color: #3a7bd5;
                }
                QHeaderView::section {
                    background-color: #1e2124;
                    color: #d8dee9;
                    padding: 6px;
                    border: 1px solid #2d3135;
                }
                QTextEdit {
                    background-color: #1e2124;
                    border: 1px solid #2d3135;
                    border-radius: 4px;
                    color: #d8dee9;
                }
                QListWidget {
                    background-color: #1e2124;
                    border: 1px solid #2d3135;
                    border-radius: 4px;
                }
                QListWidget::item:selected {
                    background-color: #3a7bd5;
                }
                QProgressBar {
                    border: 1px solid #2d3135;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3a7bd5;
                }
            """
            )

    def load_roots(self):
        """Load indexed roots into sidebar."""
        self.roots_list.clear()
        roots = self.db.get_roots()

        for root, count, _ in roots:
            self.roots_list.addItem(f"{root} ({count} docs)")

    def add_folder(self):
        """Add folder to index."""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder to Index", str(Path.home())
        )

        if not folder:
            return

        folder_path = Path(folder)

        # Check for system paths
        if is_system_path(folder_path):
            reply = QMessageBox.question(
                self,
                "System Path",
                f"{folder_path} appears to be a system path. Continue?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        # Ask about reindexing
        existing = self.db.get_document_by_path(str(folder_path))
        reindex = False

        if existing:
            reply = QMessageBox.question(
                self,
                "Reindex",
                "This folder is already indexed. Reindex?",
                QMessageBox.Yes | QMessageBox.No,
            )
            reindex = reply == QMessageBox.Yes

        # Start indexing
        self.start_index_worker(folder_path, reindex)

    def start_index(self):
        """Start indexing current selection."""
        current = self.roots_list.currentItem()
        if not current:
            QMessageBox.warning(self, "No Selection", "Please select a folder first.")
            return

        # Extract path from item text
        text = current.text()
        path = text.split(" (")[0]

        self.start_index_worker(Path(path), True)

    def start_index_worker(self, root_path: Path, reindex: bool):
        """Start index worker thread."""
        if self.index_worker and self.index_worker.isRunning():
            QMessageBox.warning(
                self,
                "Already Indexing",
                "An indexing operation is already in progress.",
            )
            return

        self.index_worker = IndexWorker(self.db, root_path, reindex, self.config)
        self.index_worker.progress_update.connect(self.on_index_progress)
        self.index_worker.finished.connect(self.on_index_finished)
        self.index_worker.error.connect(self.on_index_error)
        self.index_worker.log.connect(self.add_log)

        self.btn_index.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.index_worker.start()

    def stop_index(self):
        """Stop indexing."""
        if self.index_worker:
            self.index_worker.stop()
            self.add_log("warning", "Stopping indexing...")

    @pyqtSlot(object)
    def on_index_progress(self, progress: IndexProgress):
        """Handle index progress update."""
        stats = progress.get_stats()

        if stats["total_files"] > 0:
            percent = int((stats["processed_files"] / stats["total_files"]) * 100)
            self.progress_bar.setValue(percent)

        self.statusBar().showMessage(
            f"Indexing: {stats['processed_files']}/{stats['total_files']} files "
            f"({stats['successful']} ok, {stats['failed']} errors)"
        )

    @pyqtSlot(object)
    def on_index_finished(self, progress: IndexProgress):
        """Handle index completion."""
        stats = progress.get_stats()

        self.progress_bar.setVisible(False)
        self.btn_index.setEnabled(True)
        self.btn_stop.setEnabled(False)

        self.statusBar().showMessage(
            f"Indexing complete: {stats['successful']} files indexed in {stats['elapsed_seconds']:.1f}s"
        )

        # Reload roots
        self.load_roots()

    @pyqtSlot(str)
    def on_index_error(self, error: str):
        """Handle index error."""
        self.progress_bar.setVisible(False)
        self.btn_index.setEnabled(True)
        self.btn_stop.setEnabled(False)

        QMessageBox.critical(self, "Indexing Error", f"Indexing failed: {error}")

    def on_search_text_changed(self):
        """Handle search text change (debounced)."""
        self.search_timer.stop()
        if self.search_input.text():
            self.search_timer.start(300)  # 300ms debounce

    def perform_search(self):
        """Perform search."""
        query = self.search_input.text().strip()

        if not query:
            self.current_results = []
            self.results_table.setRowCount(0)
            return

        options = {
            "case_sensitive": self.cb_case.isChecked(),
            "regex": self.cb_regex.isChecked(),
            "whole_word": self.cb_whole.isChecked(),
            "use_ripgrep": self.cb_ripgrep.isChecked(),
            "limit": 1000,
        }

        # Start search worker
        if self.search_worker and self.search_worker.isRunning():
            # Wait for previous search to complete
            return

        self.search_worker = SearchWorker(self.search_engine, query, options)
        self.search_worker.results.connect(self.on_search_results)
        self.search_worker.error.connect(self.on_search_error)
        self.search_worker.log.connect(self.add_log)

        self.statusBar().showMessage("Searching...")
        self.search_worker.start()

    @pyqtSlot(list)
    def on_search_results(self, results: list):
        """Handle search results."""
        self.current_results = results
        self.results_table.setRowCount(len(results))

        for i, result in enumerate(results):
            path = result.get("path", "")
            source_type = result.get("source_type", "")
            line = str(result.get("line", ""))
            snippet = result.get("snippet", "")[:100]
            mtime = result.get("mtime", 0)

            # Format mtime
            if mtime:
                dt = datetime.fromtimestamp(mtime)
                mtime_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                mtime_str = ""

            self.results_table.setItem(i, 0, QTableWidgetItem(path))
            self.results_table.setItem(i, 1, QTableWidgetItem(source_type))
            self.results_table.setItem(i, 2, QTableWidgetItem(line))
            self.results_table.setItem(i, 3, QTableWidgetItem(snippet))
            self.results_table.setItem(i, 4, QTableWidgetItem(mtime_str))

        self.statusBar().showMessage(f"Found {len(results)} results")

    @pyqtSlot(str)
    def on_search_error(self, error: str):
        """Handle search error."""
        self.statusBar().showMessage(f"Search error: {error}")

    def on_result_selected(self):
        """Handle result selection."""
        selected_rows = self.results_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.current_results):
            return

        result = self.current_results[row]

        # Show details
        details = f"Path: {result.get('path', '')}\n"
        details += f"Type: {result.get('source_type', '')}\n"
        details += f"Size: {format_size(result.get('file_size', 0) or 0)}\n"
        details += f"Extractor: {result.get('extractor', '')}\n"
        details += f"SHA256: {result.get('sha256', '')[:16]}...\n"

        self.details_text.setText(details)

        # Load preview
        doc_id = result.get("id")
        if doc_id:
            text = self.search_engine.get_document_text(doc_id)
            if text:
                self.preview_text.setPlainText(text[:100000])  # Limit to 100KB
                self.highlight_matches()

    def highlight_matches(self):
        """Highlight search matches in preview."""
        query = self.search_input.text().strip()
        if not query:
            return

        cursor = self.preview_text.textCursor()
        cursor.movePosition(QTextCursor.Start)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#3a7bd5"))

        # Simple highlighting (case-insensitive)
        while True:
            cursor = self.preview_text.document().find(query, cursor)
            if cursor.isNull():
                break
            cursor.mergeCharFormat(fmt)

    def on_root_selected(self):
        """Handle root selection."""
        pass

    def remove_folder(self):
        """Remove selected folder from index."""
        current = self.roots_list.currentItem()
        if not current:
            return

        text = current.text()
        path = text.split(" (")[0]

        reply = QMessageBox.question(
            self,
            "Remove Index",
            f"Remove index for {path}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.db.delete_by_root(path)
            self.load_roots()
            self.add_log("info", f"Removed index for {path}")

    def show_result_context_menu(self, position):
        """Show context menu for results table."""
        menu = QMenu()

        open_action = menu.addAction("Open File")
        open_action.triggered.connect(self.open_selected_file)

        copy_action = menu.addAction("Copy Path")
        copy_action.triggered.connect(self.copy_file_path)

        menu.exec_(self.results_table.mapToGlobal(position))

    def open_selected_file(self):
        """Open selected file."""
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.current_results):
            return

        result = self.current_results[row]
        path = result.get("path", "")

        if path:
            import subprocess
            import platform

            system = platform.system()
            try:
                if system == "Windows":
                    subprocess.Popen(["explorer", "/select,", path])
                elif system == "Darwin":
                    subprocess.Popen(["open", "-R", path])
                else:
                    subprocess.Popen(["xdg-open", str(Path(path).parent)])
            except Exception as e:
                self.add_log("error", f"Failed to open file: {e}")

    def open_file_location(self):
        """Open file location."""
        self.open_selected_file()

    def copy_file_path(self):
        """Copy selected file path to clipboard."""
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.current_results):
            return

        result = self.current_results[row]
        path = result.get("path", "")

        if path:
            QApplication.clipboard().setText(path)
            self.statusBar().showMessage("Path copied to clipboard")

    def copy_preview_text(self):
        """Copy preview text to clipboard."""
        text = self.preview_text.toPlainText()
        QApplication.clipboard().setText(text)
        self.statusBar().showMessage("Text copied to clipboard")

    def export_results(self):
        """Export search results to JSONL."""
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No results to export.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            str(Path.home() / "docfind_results.jsonl"),
            "JSONL Files (*.jsonl);;All Files (*)",
        )

        if not filename:
            return

        try:
            import json

            with open(filename, "w") as f:
                for result in self.current_results:
                    f.write(json.dumps(result) + "\n")

            self.statusBar().showMessage(
                f"Exported {len(self.current_results)} results"
            )
            self.add_log("info", f"Exported results to {filename}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export: {e}")

    def show_settings(self):
        """Show settings dialog."""
        dialog = SettingsDialog(self.config, self)

        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()

            for key, value in settings.items():
                self.config[key] = value

            self.config.save()
            self.add_log("info", "Settings saved")

    def optimize_database(self):
        """Optimize database."""
        reply = QMessageBox.question(
            self,
            "Optimize Database",
            "This may take a few minutes. Continue?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.statusBar().showMessage("Optimizing database...")
            self.db.optimize()
            self.statusBar().showMessage("Database optimized")
            self.add_log("info", "Database optimized")

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About DocFind",
            f"<h3>DocFind {__version__}</h3>"
            "<p>A cross-platform document indexing and search tool.</p>"
            "<p>Supports PDF, DOCX, XLSX, PPTX, HTML, and more.</p>",
        )

    def add_log(self, level: str, message: str):
        """Add log message to console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {"info": "#d8dee9", "warning": "#ebcb8b", "error": "#bf616a"}.get(
            level, "#d8dee9"
        )

        html = f'<span style="color: {color}">[{timestamp}] [{level.upper()}] {message}</span><br>'
        self.log_console.append(html)

    def restore_geometry(self):
        """Restore window geometry."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        """Handle window close."""
        self.settings.setValue("geometry", self.saveGeometry())

        # Stop workers
        if self.index_worker and self.index_worker.isRunning():
            self.index_worker.stop()
            self.index_worker.wait(5000)

        event.accept()


def main():
    """Main GUI entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("DocFind")
    app.setOrganizationName("DocFind")

    # Setup logging
    from .utils import setup_logging, get_data_dir

    log_file = get_data_dir() / "docfind_gui.log"
    setup_logging(log_file=log_file, level=logging.INFO)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
