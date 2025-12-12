from __future__ import annotations

from PyQt6.QtGui import QColor

from weegit.gui.panels.base_signal_panel import BaseSignalPanel


class AnalogueSignalPanel(BaseSignalPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.background_color = QColor(200, 200, 200)

    def get_visible_channel_indexes(self):
        return []
