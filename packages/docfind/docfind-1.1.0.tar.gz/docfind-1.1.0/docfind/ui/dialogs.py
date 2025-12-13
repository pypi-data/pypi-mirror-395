"""
Dialog windows for DocFind GUI.

Additional dialogs and UI components.
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QDialogButtonBox,
)
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    """About dialog."""

    def __init__(self, version: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About DocFind")
        self.setModal(True)
        self.init_ui(version)

    def init_ui(self, version: str):
        """Initialize UI."""
        layout = QVBoxLayout()

        title = QLabel(f"<h2>DocFind {version}</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "<p>A cross-platform document indexing and search tool.</p>"
            "<p>Supports PDF, DOCX, XLSX, PPTX, HTML, and more.</p>"
            "<p>&copy; 2025 cmdeniz</p>"
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)


class LogViewerDialog(QDialog):
    """Full log viewer dialog."""

    def __init__(self, log_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Viewer")
        self.setMinimumSize(800, 600)
        self.init_ui(log_text)

    def init_ui(self, log_text: str):
        """Initialize UI."""
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(log_text)
        layout.addWidget(self.text_edit)

        # Buttons
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_log)
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def clear_log(self):
        """Clear log text."""
        self.text_edit.clear()
