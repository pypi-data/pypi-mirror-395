from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit


class InformationPanel(QWidget):
    """Widget that represents an editable large text input"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Information")
        title_label.setStyleSheet("font-weight: bold;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter information here...")

        layout.addLayout(header_layout)
        layout.addWidget(self.text_edit)

    def set_text(self, text: str):
        """Set the text content"""
        self.text_edit.setText(text)

    def get_text(self) -> str:
        """Get the text content"""
        return self.text_edit.toPlainText()

    def clear_text(self):
        """Clear the text content"""
        self.text_edit.clear()
