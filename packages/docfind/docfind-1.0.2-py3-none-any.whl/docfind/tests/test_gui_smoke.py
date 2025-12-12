"""
Smoke tests for GUI.

Basic tests to ensure GUI components can be instantiated.
"""

import pytest
import sys
import os
from pathlib import Path

# Only run if PyQt5 is available
pytest.importorskip("PyQt5")

from PyQt5.QtWidgets import QApplication


# Skip GUI tests in CI environment (they crash even with xvfb)
skip_gui = pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="GUI tests are unstable in CI environment",
)


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_import_gui():
    """Test importing GUI module."""
    from docfind import gui

    assert gui is not None


@skip_gui
def test_main_window_creation(qapp):
    """Test creating main window."""
    from docfind.gui import MainWindow

    window = MainWindow()
    assert window is not None
    assert window.windowTitle() is not None


@skip_gui
def test_settings_dialog(qapp):
    """Test creating settings dialog."""
    from docfind.gui import SettingsDialog
    from docfind.utils import Config

    config = Config()
    dialog = SettingsDialog(config)
    assert dialog is not None


@skip_gui
def test_stylesheet_loading(qapp):
    """Test that stylesheet can be loaded."""
    from docfind.gui import MainWindow

    window = MainWindow()

    # Check that stylesheet is set (either from file or inline)
    stylesheet = window.styleSheet()
    assert stylesheet is not None
    assert len(stylesheet) > 0


@skip_gui
def test_worker_threads(qapp):
    """Test that worker threads can be created."""
    from docfind.gui import IndexWorker, SearchWorker
    from docfind.db import DatabaseManager
    from docfind.search import SearchEngine
    from docfind.utils import Config
    import tempfile

    # Create temp database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = DatabaseManager(db_path)
    config = Config()

    # Test IndexWorker creation
    worker = IndexWorker(db, Path.home(), False, config)
    assert worker is not None

    # Test SearchWorker creation
    search = SearchEngine(db)
    search_worker = SearchWorker(search, "test", {})
    assert search_worker is not None

    # Cleanup
    db.close()
    db_path.unlink()


@skip_gui
def test_ui_components(qapp):
    """Test that UI components are created."""
    from docfind.gui import MainWindow

    window = MainWindow()

    # Check main components exist
    assert window.search_input is not None
    assert window.results_table is not None
    assert window.preview_text is not None
    assert window.log_console is not None
    assert window.progress_bar is not None
    assert window.roots_list is not None


@skip_gui
def test_menu_actions(qapp):
    """Test that menu actions are created."""
    from docfind.gui import MainWindow

    window = MainWindow()

    # Check menu bar exists
    menubar = window.menuBar()
    assert menubar is not None

    # Check that menus exist
    actions = menubar.actions()
    assert len(actions) > 0
