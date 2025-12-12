from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFormLayout, QSpinBox


class SegmentToSavePanel(QWidget):
    """Widget that allows specifying timing for segments to save"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Segment to Save")
        title_label.setStyleSheet("font-weight: bold;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Form layout for timing fields
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 10, 0, 10)

        # Before field
        self.before_spinbox = QSpinBox()
        self.before_spinbox.setRange(0, 9999)
        self.before_spinbox.setValue(5)
        self.before_spinbox.setSuffix(" s")

        # After field
        self.after_spinbox = QSpinBox()
        self.after_spinbox.setRange(0, 9999)
        self.after_spinbox.setValue(5)
        self.after_spinbox.setSuffix(" s")

        form_layout.addRow("Before:", self.before_spinbox)
        form_layout.addRow("After:", self.after_spinbox)

        layout.addLayout(header_layout)
        layout.addLayout(form_layout)
        layout.addStretch(1)

    def get_timing(self) -> tuple[int, int]:
        """Get the before and after timing values"""
        return self.before_spinbox.value(), self.after_spinbox.value()

    def set_timing(self, before: int, after: int):
        """Set the before and after timing values"""
        self.before_spinbox.setValue(before)
        self.after_spinbox.setValue(after)
