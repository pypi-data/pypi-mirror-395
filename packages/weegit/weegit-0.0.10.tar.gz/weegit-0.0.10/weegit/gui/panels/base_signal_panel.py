from __future__ import annotations

from typing import Optional

from PyQt6.QtGui import QFont, QFontMetrics, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class BaseSignalPanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Data properties
        # self.data: Optional[np.memmap] = None
        # self.units: Optional[np.ndarray] = None
        # self.analogue_min: Optional[np.ndarray] = None
        # self.analogue_max: Optional[np.ndarray] = None
        # self.digital_min: Optional[np.ndarray] = None
        # self.digital_max: Optional[np.ndarray] = None
        #
        # # Display properties
        # self.start_point: int = 0
        # self.duration: int = 1000  # ms
        # self.si: int = 1000  # microseconds
        # self.visible_channel_indexes: List[int] = []
        # self.scale = 1.0
        # self.channel_height = 100

        # Visual properties
        self.channel_label_padding = 60
        self.channel_spacing = 5
        self.font = QFont("Arial", 8)
        self.font_metrics = QFontMetrics(self.font)
        self.channels_top_padding = 50

        # Colors
        self.background_color = QColor(100, 100, 100)
        self.grid_color = QColor(200, 200, 200)
        self.trace_color = QColor(0, 0, 0)
        self.text_color = QColor(0, 0, 0)

        # Optimization
        self._cached_data = None
        self._cached_rect = None
        self._cached_points = None

        self.update()

    def paintEvent(self, event):
        """Handle widget painting."""
        # if self.data is None or not self.visible_channel_indexes:
        #     return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set up fonts and colors
        painter.setFont(self.font)
        painter.setPen(QPen(self.text_color))

        # Draw background
        painter.fillRect(self.rect(), self.background_color)

        # Draw channel labels and traces
        # dots_number = self._cached_data_from_channels.shape[0]
        # for channel_draw_idx, channel in enumerate(self.visible_channel_indexes):
        #     # Draw channel label
        #     label = f"Ch {channel + 1}"
        #     if channel < len(self.units):
        #         label += f" ({self.units[channel]})"
        #     painter.drawText(10, self.channels_top_padding + channel_draw_idx * (self.channel_height + self.channel_spacing) +
        #                      self.channel_height // 2, label)
        #
        #     # Get and draw channel data
        #     # data = self._cached_data_from_channels[:, channel]
        #     # if len(data) == 0:
        #     #     continue
        #
        #     # Draw grid lines
        #     # painter.setPen(QPen(self.grid_color))
        #     # rect = QRect(self.channel_label_padding, 50 + channel_draw_idx * (self.channel_height + self.channel_spacing),
        #     #              self.width() - self.channel_label_padding, self.channel_height)
        #     # painter.drawRect(rect)
        #
        #     # Draw zero line
        #     # center_y = rect.center().y()
        #     # painter.drawLine(rect.left(), center_y, rect.right(), center_y)
        #
        #     # Draw time markers
        #     # time_step = max(1, int(100 / self.time_scale))  # 100ms steps
        #     # for t in range(0, len(data), time_step):
        #     #     x = int(rect.left() + t * self.time_scale)
        #     #     # painter.drawLine(x, rect.top(), x, rect.bottom())
        #     #     if t % (time_step * 5) == 0:  # Every 500ms
        #     #         time_ms = t * self.si / 1000
        #     #         # painter.drawText(x - 20, rect.bottom() + 15, f"{time_ms}ms")
        #
        #     # Draw trace
        #     points = []
        #     for dot_draw_idx, value in enumerate(self._cached_data_from_channels[:, channel]):
        #         point = self._convert_to_screen(dot_draw_idx, dots_number, value, channel_draw_idx)
        #         points.append(point)
        #         # fixme: an example of spikes drawing
        #         # if point.y() == 120:
        #         #     pen = QPen()
        #         #     pen.setWidth(5)
        #         #     painter.setPen(pen)
        #         #     painter.drawEllipse(point.x(), point.y(), self.channels_top_padding, self.channels_top_padding)
        #
        #     painter.setPen(QPen(self.trace_color))
        #     if len(points) > 1:
        #         painter.drawPolyline(points)
