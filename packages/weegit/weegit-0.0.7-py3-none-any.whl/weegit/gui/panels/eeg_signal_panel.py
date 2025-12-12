import numpy as np
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QPoint, QLineF, QEvent
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QWheelEvent, QMouseEvent, QKeyEvent, QPixmap, QFontMetrics
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollBar, QHBoxLayout, QPushButton
from typing import Optional, List, Dict
import math

from weegit import settings
from weegit.gui._utils import milliseconds_to_readable
from weegit.gui.qt_weegit_session_manager_wrapper import QtWeegitSessionManagerWrapper


class SignalWidget(QWidget):
    """Custom widget for signal display that handles its own paint events"""

    def __init__(self, left_margin, right_margin, bottom_margin, parent=None):
        super().__init__(parent)
        self.pixmap_cache = QPixmap()
        self._BG_COLOR = QColor(240, 240, 240)
        self._GRID_COLOR = QColor(200, 200, 200)
        self._SIGNAL_COLOR = QColor(0, 0, 0)
        self._TEXT_COLOR = QColor(0, 0, 0)
        self._AXIS_COLOR = QColor(100, 100, 100)
        self._CHANNEL_SPACING = 5
        self._left_margin = left_margin
        self._right_margin = right_margin
        self._bottom_margin = bottom_margin

        self._channel_height = 0
        self._cached_x_coords: Optional[np.ndarray] = None
        self._cached_x_width: int = -1
        self._cached_x_points: int = -1
        self._lines_cache: Dict[int, List[QLineF]] = {}
        self._axis_start_point = 0
        self._axis_duration_ms = 0.0
        self._sample_rate = 1.0
        self._overlay_widget: Optional['OverlayWidget'] = None

    def set_overlay_widget(self, overlay_widget: Optional['OverlayWidget']):
        """Attach an overlay widget that mirrors the signal widget geometry."""
        self._overlay_widget = overlay_widget
        if self._overlay_widget:
            self._overlay_widget.setParent(self)
            self._overlay_widget.setGeometry(self.rect())
            self._overlay_widget.raise_()

    def reset_data_and_redraw(
        self,
        processed_data,
        visible_channel_indexes,
        channel_names,
        voltage_scale,
        *,
        start_point: int,
        duration_ms: float,
        sample_rate: float,
    ):
        self._axis_start_point = max(0, start_point)
        self._axis_duration_ms = max(0.0, duration_ms)
        self._sample_rate = sample_rate if sample_rate > 0 else 1.0

        self.pixmap_cache = QPixmap(self.size())
        # self.pixmap_cache.fill(Qt.GlobalColor.white)  # Qt.GlobalColor.transparent

        width = self.width()
        height = self.height()
        painter = QPainter(self.pixmap_cache)
        painter.fillRect(0, 0, width, height, self._BG_COLOR)

        draw_area_height = max(0, height - self._bottom_margin)

        if processed_data and visible_channel_indexes:
            self._channel_height = int(((draw_area_height) / len(visible_channel_indexes)) - self._CHANNEL_SPACING)

        # Draw channel backgrounds and names
        channel_rects = {}
        for cur_draw_idx, channel_idx in enumerate(visible_channel_indexes):
            y_pos = cur_draw_idx * (self._channel_height + self._CHANNEL_SPACING)
            channel_rects[channel_idx] = QRect(
                self._left_margin,
                y_pos,
                width - self._left_margin - self._right_margin,
                self._channel_height,
            )

        for cur_draw_idx, channel_idx in enumerate(visible_channel_indexes):
            self.draw_channel_info(painter, channel_idx, channel_rects[channel_idx], channel_names)
            self.draw_middle_line(painter, channel_rects[channel_idx])

        for cur_draw_idx, channel_idx in enumerate(visible_channel_indexes):
            self.draw_signal(
                painter,
                processed_data[channel_idx],
                channel_rects[channel_idx],
                voltage_scale,
                channel_idx,
                cur_draw_idx,
            )

        self._draw_time_axis(painter, width, height)
        self.update()  # Trigger paint event

    def _draw_time_axis(self, painter: QPainter, width: int, height: int):
        if self._axis_duration_ms <= 0:
            return

        axis_rect_top = max(0, height - self._bottom_margin)
        axis_y = axis_rect_top + min(5, self._bottom_margin // 6)
        axis_start_x = self._left_margin
        axis_end_x = max(axis_start_x, width - self._right_margin)
        axis_width = axis_end_x - axis_start_x
        if axis_width <= 0:
            return

        painter.fillRect(0, axis_rect_top, width, height - axis_rect_top, self._BG_COLOR)

        pen = QPen(self._AXIS_COLOR, 2)
        painter.setPen(pen)
        painter.drawLine(axis_start_x, axis_y, axis_end_x, axis_y)

        visible_points = int((self._axis_duration_ms / 1000.0) * self._sample_rate)
        if visible_points <= 0:
            return

        start_time_ms = (self._axis_start_point / self._sample_rate) * 1000
        end_time_ms = start_time_ms + self._axis_duration_ms
        total_time_ms = end_time_ms - start_time_ms
        if total_time_ms <= 0:
            return

        target_ticks = 8
        rough_interval = total_time_ms / target_ticks
        if rough_interval <= 0:
            return

        exponent = math.floor(math.log10(rough_interval))
        mantissa = rough_interval / (10 ** exponent)

        if mantissa < 1.5:
            tick_interval = 10 ** exponent
        elif mantissa < 3:
            tick_interval = 2 * 10 ** exponent
        elif mantissa < 7:
            tick_interval = 5 * 10 ** exponent
        else:
            tick_interval = 10 ** (exponent + 1)

        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(self._AXIS_COLOR)

        time_ms = math.ceil(start_time_ms / tick_interval) * tick_interval
        label_offset = 8
        while time_ms <= end_time_ms:
            x = axis_start_x + ((time_ms - start_time_ms) / self._axis_duration_ms) * axis_width
            painter.drawLine(int(x), axis_y, int(x), axis_y + 6)

            label = milliseconds_to_readable(time_ms, wrap=False)
            # label = f"{time_ms:.0f}ms" if time_ms < 1000 else f"{time_ms / 1000:.1f}s"
            text_rect = QRect(int(x) - 50, axis_y + label_offset, 100, 15)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

            time_ms += tick_interval

    def draw_channel_info(self, painter: QPainter, channel_idx: int, channel_rect: QRect, channel_names):
        """Draw channel name and index on the left"""
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(self._TEXT_COLOR)

        channel_name = channel_names[channel_idx]
        text_rect = QRect(5, channel_rect.top(), self._left_margin - 10, channel_rect.height())

        # Draw channel index and name
        text = f"{channel_idx} [{channel_name}]"
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def draw_middle_line(self, painter, channel_rect):
        zero_y = channel_rect.top() + channel_rect.height() // 2
        pen = QPen(self._GRID_COLOR, 2, Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.drawLine(channel_rect.left(), zero_y, channel_rect.right(), zero_y)

    def draw_signal(self, painter: QPainter, channel_data: np.ndarray, channel_rect: QRect,
                    voltage_scale, channel_idx: int, cur_draw_idx: int):
        """Draw EEG signal for a single channel while keeping every sample."""
        if channel_data is None or len(channel_data) < 2:
            return

        pen = QPen(self._SIGNAL_COLOR, 1.5)
        painter.setPen(pen)

        n_points = len(channel_data)
        x_coords = self._get_cached_x_coords(channel_rect, n_points)

        scale_factor = self.get_channel_scale(channel_idx)
        full_scale = voltage_scale * settings.EEG_VOLTAGE_SCALE * scale_factor
        channel_mid_y = channel_rect.top() + channel_rect.height() / 2.0
        y_offsets = channel_data * full_scale
        y_coords = channel_mid_y - y_offsets

        line_buffer = self._get_line_buffer(cur_draw_idx, n_points - 1)
        for i in range(n_points - 1):
            line_buffer[i].setLine(
                float(x_coords[i]),
                float(y_coords[i]),
                float(x_coords[i + 1]),
                float(y_coords[i + 1])
            )

        painter.drawLines(line_buffer[:n_points - 1])

    def get_channel_scale(self, channel_idx: int) -> float:
        # fixme: implement me
        return 1.0
        # """Get scale factor for a specific channel"""
        # if (self._header and self._header.channel_info and
        #         self._header.channel_info.analog_max and
        #         self._header.channel_info.analog_min and
        #         channel_idx < len(self._header.channel_info.analog_max)):
        #     analog_max = self._header.channel_info.analog_max[channel_idx]
        #     analog_min = self._header.channel_info.analog_min[channel_idx]
        #     voltage_range = analog_max - analog_min
        #     return 1.0 / voltage_range if voltage_range != 0 else 1.0
        #
        # return 1.0  # Default scale

    def _value_to_pixel_voltage(self, value, voltage_scale, channel_idx: Optional[int] = None):
        if channel_idx is not None:
            scale_factor = self.get_channel_scale(channel_idx)
        else:
            scale_factor = 1.0

        return value * voltage_scale * settings.EEG_VOLTAGE_SCALE * scale_factor

    def _get_cached_x_coords(self, channel_rect: QRect, n_points: int) -> np.ndarray:
        """Cache evenly-spaced X coordinates for a given width/data length."""
        width = channel_rect.width()
        if (self._cached_x_coords is not None and
                self._cached_x_width == width and
                self._cached_x_points == n_points):
            return self._cached_x_coords

        if n_points < 2 or width <= 0:
            coords = np.array([float(channel_rect.left())], dtype=np.float32)
        else:
            x0 = channel_rect.left()
            coords = x0 + np.linspace(0.0, 1.0, n_points, dtype=np.float32) * (width - 1)

        self._cached_x_coords = coords
        self._cached_x_width = width
        self._cached_x_points = n_points
        return coords

    def _get_line_buffer(self, cur_draw_idx: int, required: int) -> List[QLineF]:
        """Ensure a reusable QLineF buffer exists for the channel."""
        buffer = self._lines_cache.setdefault(cur_draw_idx, [])
        missing = required - len(buffer)
        if missing > 0:
            buffer.extend(QLineF() for _ in range(missing))
        return buffer

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._overlay_widget:
            self._overlay_widget.setGeometry(self.rect())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap_cache)


class OverlayWidget(QWidget):
    """Transparent overlay that draws time/voltage scale bars at the cursor."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._cursor_pos: Optional[QPoint] = None
        self._show_scale = False
        self._left_margin = 0
        self._right_margin = 0
        self._bottom_margin = 0
        self._channel_height = 0
        self._bar_width = 3
        self._duration_ms = 0.0
        self._scale_value = 1.0
        self._font = QFont()
        self._font.setPointSize(12)
        self._font_metrics = QFontMetrics(self._font)

    def update_state(self, *, cursor_pos: Optional[QPoint], show_scale: bool,
                     left_margin: int, right_margin: int, bottom_margin: int,
                     channel_height: int, bar_width: int,
                     duration_ms: float, scale_value: float):
        self._cursor_pos = cursor_pos
        self._show_scale = show_scale
        self._left_margin = left_margin
        self._right_margin = right_margin
        self._bottom_margin = bottom_margin
        self._channel_height = max(0, channel_height)
        self._bar_width = max(1, bar_width)
        self._duration_ms = max(0.0, duration_ms)
        self._scale_value = scale_value if scale_value > 0 else 1.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self._show_scale or self._cursor_pos is None:
            return
        if not self._cursor_in_signal_area():
            return

        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.setFont(self._font)
        self._draw_voltage_scale_bar(painter)
        self._draw_time_scale_bar(painter)

    def _cursor_in_signal_area(self) -> bool:
        if self._cursor_pos is None:
            return False
        within_x = self._left_margin <= self._cursor_pos.x() <= self.width() - self._right_margin
        within_y = 0 <= self._cursor_pos.y() <= self.height() - self._bottom_margin
        return within_x and within_y

    def _signal_width(self) -> int:
        return max(0, self.width() - self._left_margin - self._right_margin)

    def _draw_voltage_scale_bar(self, painter: QPainter):
        bar_height = min(50, self._channel_height // 4)
        if bar_height <= 0:
            return

        x = self._cursor_pos.x() - self._bar_width // 2
        y = self._cursor_pos.y() - bar_height

        painter.fillRect(int(x), int(y), self._bar_width, bar_height, QColor(255, 0, 0))

        voltage_value = (bar_height / settings.EEG_VOLTAGE_SCALE) / self._scale_value
        label_text = f"{voltage_value:.1f} µV"
        x_size = self._font_metrics.horizontalAdvance(label_text) + 10
        label_rect = QRect(int(x) - x_size, int(y + bar_height // 2), x_size, 16)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, label_text)

    def _draw_time_scale_bar(self, painter: QPainter):
        signal_width = self._signal_width()
        if signal_width <= 0 or self._duration_ms <= 0:
            return

        time_bar_pixels = max(10, min(signal_width // 10, 120))
        y = self._cursor_pos.y() - self._bar_width
        x = self._cursor_pos.x()
        x = max(self._left_margin, min(x, self.width() - self._right_margin - time_bar_pixels))

        painter.fillRect(int(x), int(y), time_bar_pixels, self._bar_width, QColor(255, 0, 0))

        time_value_ms = (time_bar_pixels / signal_width) * self._duration_ms
        if time_value_ms < 1000:
            label_text = f"{time_value_ms:.1f} ms"
        else:
            label_text = f"{time_value_ms / 1000:.2f} s"

        label_rect = QRect(int(x), int(y) + self._bar_width + 2, time_bar_pixels, 16)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, label_text)


class EegSignalPanel(QWidget):
    """High-performance EEG signal visualization panel with scrolling and optimization"""
    channel_scroll_changed = pyqtSignal()

    def __init__(self, session_manager, parent=None):
        super().__init__(parent)

        self._session_manager: QtWeegitSessionManagerWrapper = session_manager
        self._cached_processed_data: Dict[int, np.ndarray[np.float64]] = {}

        # Scale bar
        self._show_voltage_scale = False
        self._current_mouse_pos = None
        self._BAR_WIDTH = 3

        # UI constants
        self._TOP_MARGIN = 30  # Space for future graphics
        self._BOTTOM_MARGIN = 30  # Space for time axis
        self._LEFT_MARGIN = 80  # Space for channel names
        self._RIGHT_MARGIN = 20
        self._CHANNEL_SPACING = 5

        self._channel_height = 60

        # Scroll state
        self._channel_scroll_offset = 0

        # Colors and styles
        self._bg_color = QColor(240, 240, 240)
        self._grid_color = QColor(200, 200, 200)
        self._SIGNAL_COLOR = QColor(0, 0, 0)
        self._text_color = QColor(0, 0, 0)
        self._axis_color = QColor(100, 100, 100)

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Setup the UI with scrollbars"""
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top graphics area (reserved space)
        self.top_graphics_widget = QWidget()
        self.top_graphics_widget.setFixedHeight(self._TOP_MARGIN)
        main_layout.addWidget(self.top_graphics_widget)

        # Main content area with scrollbars
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left vertical scrollbar for channels
        self.channel_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        self.channel_scrollbar.setSingleStep(1)
        self.channel_scrollbar.setPageStep(1)
        content_layout.addWidget(self.channel_scrollbar)

        # Signal display area
        self.signal_widget = SignalWidget(self._LEFT_MARGIN, self._RIGHT_MARGIN, self._BOTTOM_MARGIN)
        self.signal_widget.setMouseTracking(True)
        self.signal_widget.installEventFilter(self)
        self.overlay_widget = OverlayWidget(self.signal_widget)
        self.signal_widget.set_overlay_widget(self.overlay_widget)
        content_layout.addWidget(self.signal_widget, 1)

        main_layout.addLayout(content_layout, 1)

        # Bottom time axis and horizontal scrollbar
        bottom_layout = QHBoxLayout()

        # Double left arrow
        self.btn_double_left = QPushButton("<<")
        self.btn_double_left.setFixedWidth(40)
        bottom_layout.addWidget(self.btn_double_left)

        # Single left arrow
        self.btn_single_left = QPushButton("<")
        self.btn_single_left.setFixedWidth(30)
        bottom_layout.addWidget(self.btn_single_left)

        # Horizontal scrollbar
        self.time_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        bottom_layout.addWidget(self.time_scrollbar, 1)

        # Single right arrow
        self.btn_single_right = QPushButton(">")
        self.btn_single_right.setFixedWidth(30)
        bottom_layout.addWidget(self.btn_single_right)

        # Double right arrow
        self.btn_double_right = QPushButton(">>")
        self.btn_double_right.setFixedWidth(40)
        bottom_layout.addWidget(self.btn_double_right)

        main_layout.addLayout(bottom_layout)

    def connect_signals(self):
        """Connect all signals to their handlers"""
        # Time parameter changes
        self.channel_scrollbar.valueChanged.connect(self.on_channel_scroll)
        self.btn_double_left.clicked.connect(self.on_double_left_click)
        self.btn_single_left.clicked.connect(self.on_single_left_click)
        self.time_scrollbar.valueChanged.connect(self.on_time_scroll)
        self.btn_single_right.clicked.connect(self.on_single_right_click)
        self.btn_double_right.clicked.connect(self.on_double_right_click)

    def eventFilter(self, watched, event):
        if watched is self.signal_widget:
            if event.type() == QEvent.Type.MouseMove and isinstance(event, QMouseEvent):
                pos = event.position().toPoint()
                if self.signal_widget.rect().contains(pos):
                    self._current_mouse_pos = pos
                else:
                    self._current_mouse_pos = None
                self._update_overlay_widget()
            elif event.type() == QEvent.Type.Leave:
                self._current_mouse_pos = None
                self._update_overlay_widget()
        return super().eventFilter(watched, event)

    def reset_data_and_redraw(self, processed_data):
        self._cached_processed_data = processed_data
        self._redraw_data()

    def _redraw_data(self):
        if not self._cached_processed_data:
            return

        gui_setup = self._session_manager.gui_setup
        if not gui_setup:
            return

        self.update_scrollbars()

        sample_rate = self.get_sample_rate()

        self.signal_widget.reset_data_and_redraw(
            self._cached_processed_data,
            self.get_visible_channel_indexes(),
            self._session_manager.header.channel_info.name,
            gui_setup.scale,
            start_point=gui_setup.start_point,
            duration_ms=gui_setup.duration_ms,
            sample_rate=sample_rate,
        )

        self._update_overlay_widget()

    def _update_overlay_widget(self):
        if not hasattr(self, 'overlay_widget') or self.overlay_widget is None:
            return

        gui_setup = self._session_manager.gui_setup if self._session_manager else None
        duration_ms = gui_setup.duration_ms if gui_setup else 0.0
        scale_value = gui_setup.scale if gui_setup else 1.0
        channel_height = self.signal_widget._channel_height or self._channel_height
        cursor_pos = self._current_mouse_pos if (self._show_voltage_scale and self._current_mouse_pos is not None) else None

        self.overlay_widget.update_state(
            cursor_pos=cursor_pos,
            show_scale=self._show_voltage_scale,
            left_margin=self._LEFT_MARGIN,
            right_margin=self._RIGHT_MARGIN,
            bottom_margin=self._BOTTOM_MARGIN,
            channel_height=channel_height,
            bar_width=self._BAR_WIDTH,
            duration_ms=duration_ms,
            scale_value=scale_value
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._redraw_data()

    def _current_visible_channel_indexes(self):
        visible_indexes = self._session_manager.gui_setup.visible_channel_indexes
        if not visible_indexes:
            visible_indexes = list(range(self._session_manager.header.number_of_channels))

        return visible_indexes

    def update_scrollbars(self):
        """Update scrollbar ranges based on current data and settings"""
        if not self._session_manager.header or not self._session_manager.gui_setup:
            return

        # Channel scrollbar
        eeg_channels = self._session_manager.eeg_channel_indexes
        visible_channel_indexes = [ch for ch in eeg_channels if ch in self._current_visible_channel_indexes()]

        total_channels = len(visible_channel_indexes)
        if total_channels > self._session_manager.gui_setup.number_of_channels_to_show:
            self.channel_scrollbar.setMaximum(
                total_channels - self._session_manager.gui_setup.number_of_channels_to_show)
            self.channel_scrollbar.setVisible(True)
        else:
            self.channel_scrollbar.setMaximum(0)
            self.channel_scrollbar.setVisible(False)

        # Time scrollbar
        total_points = self._session_manager.header.number_of_points_per_sweep
        visible_points = int((self._session_manager.gui_setup.duration_ms / 1000.0) * self.get_sample_rate())
        self.time_scrollbar.setMaximum(max(0, total_points - visible_points))
        # self.time_scrollbar.setValue(min(0, self.time_scrollbar.maximum()))

    def get_sample_rate(self) -> float:
        """Get sample rate from header"""
        if not self._session_manager.header:
            return 1.0
        sample_interval_seconds = self._session_manager.header.sample_interval_microseconds / 1_000_000.0
        return 1.0 / sample_interval_seconds if sample_interval_seconds > 0 else 1.0

    def get_visible_channel_indexes(self) -> List[int]:
        """Get currently visible channels considering scroll position"""
        if not self._session_manager.gui_setup:
            return []

        eeg_channels = self._session_manager.gui_setup.eeg_channel_indexes
        visible_channel_indexes = [ch for ch in eeg_channels if ch in self._current_visible_channel_indexes()]

        start_idx = self._channel_scroll_offset
        end_idx = start_idx + self._session_manager.gui_setup.number_of_channels_to_show
        return visible_channel_indexes[start_idx:end_idx]

    def on_channel_scroll(self, value):
        """Handle channel scrollbar movement"""
        self._channel_scroll_offset = value
        self.channel_scroll_changed.emit()

    def on_time_scroll(self, value):
        """Handle time scrollbar movement"""
        self._session_manager.set_start_point(value)

    def on_single_left_click(self):
        """Handle single left arrow click"""
        self.time_scrollbar.setValue(
            self._session_manager.gui_setup.start_point
            - int((self._session_manager.gui_setup.time_step_ms * 1000)
                  / self._session_manager.header.sample_interval_microseconds)
        )

    def on_single_right_click(self):
        self.time_scrollbar.setValue(
            self._session_manager.gui_setup.start_point
            + int((self._session_manager.gui_setup.time_step_ms * 1000)
                  / self._session_manager.header.sample_interval_microseconds)
        )

    def on_double_right_click(self):
        pass

    def on_double_left_click(self):
        pass

    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for horizontal scrolling"""
        # if event.angleDelta().y() != 0:
        # step = self.time_scrollbar.singleStep() * 2
        # if event.angleDelta().y() > 0:
        #     new_value = max(0, self.time_scrollbar.value() - step)
        # else:
        #     new_value = min(self.time_scrollbar.maximum(),
        #                     self.time_scrollbar.value() + step)
        # self.time_scrollbar.setValue(new_value)
        # event.accept()
        # else:
        super().wheelEvent(event)

    # FOR FUN
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        key = event.key()

        if key == Qt.Key.Key_M:
            # Toggle voltage scale bar with 'M' key
            self._show_voltage_scale = not self._show_voltage_scale
            if not self._show_voltage_scale:
                self._current_mouse_pos = None
                self.unsetCursor()
            else:
                self.setCursor(Qt.CursorShape.BlankCursor)

            self._update_overlay_widget()
            event.accept()
        else:
            # Your existing key handling code...
            super().keyPressEvent(event)

    def leaveEvent(self, event):
        """Hide scale when mouse leaves"""
        self._current_mouse_pos = None
        self._update_overlay_widget()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Set focus when clicked"""
        self.setFocus()
        super().mousePressEvent(event)

    # def _on_eeg_scrolled(self, x_scroll: int, x_pos: float, x_window_width: int, y_scroll: int):
    #     """Handle step size change."""
    #     if x_scroll != 0:
    #         if x_scroll > 0:
    #             self.session_manager.user_session.gui_setup.start_point = (
    #                 max(0, self.session_manager.user_session.gui_setup.start_point
    #                     - self.session_manager.user_session.gui_setup.time_step_ms))
    #         elif x_scroll < 0:
    #             self.session_manager.user_session.gui_setup.start_point = (
    #                     self.session_manager.user_session.gui_setup.start_point
    #                     + self.session_manager.user_session.gui_setup.time_step_ms)
    #         self.start_spin.setValue(self.session_manager.user_session.gui_setup.start_point)
    #     # if first third: start_time same, duration cut twice?
    #     # if middle: only duration cut twice
    #     # if third third: start_time += duration / 2, duration cut twice
    #     if y_scroll != 0:
    #         if y_scroll > 0:  # zoom in
    #             self.session_manager.user_session.gui_setup.start_point = min(int(self._MAX_DURATION - self.session_manager.user_session.gui_setup.duration_ms),
    #                                   self.start_time + 2 * int(self.session_manager.user_session.gui_setup.duration_ms * (x_pos / x_window_width)))
    #             # self.eeg_start_channel = max(0, self.eeg_start_channel - 1)
    #         elif y_scroll < 0:  # zoom out
    #             self.session_manager.user_session.gui_setup.start_point = max(0, self.session_manager.user_session.gui_setup.start_point - int(self.session_manager.user_session.gui_setup.duration_ms * (x_pos / x_window_width)))
    #             # if zoom_right_part:
    #             #     self.start_time = max(0, self.start_time - self.zoom_step)
    #             # else:
    #             #     self.start_time += self.zoom_step
    #             # self.eeg_start_channel = min(self.header.nCh - self.eeg_channels_to_show, self.eeg_start_channel + 1)
    #         self.start_spin.setValue(self.session_manager.user_session.gui_setup.start_point)
    #         self.duration_spin.setValue(self.session_manager.user_session.gui_setup.duration_ms)
    #         # self.eeg_panel.set_visible_channel_indexes(list(range(self.eeg_start_channel,
    #         #                                           self.eeg_start_channel + self.eeg_channels_to_show)))
    #
    # def _on_prev_clicked(self):
    #     """Handle previous button click."""
    #     self.session_manager.user_session.gui_setup.start_point = max(0, self.session_manager.user_session.gui_setup.start_point - self.session_manager.user_session.gui_setup.time_step_ms)
    #     self.start_spin.setValue(self.session_manager.user_session.gui_setup.start_point)
    #     self.__update_eeg_panel()
    #
    # def _on_next_clicked(self):
    #     """Handle next button click."""
    #     # if self.data is not None:
    #     #     max_start = self.data.shape[0] / self.sampling_rate * 1000 - self.duration
    #     # self.start_time = min(max_start, self.start_time + self.time_step)
    #     self.session_manager.user_session.gui_setup.start_point = self.session_manager.user_session.gui_setup.start_point + self.session_manager.user_session.gui_setup.time_step_ms
    #     self.start_spin.setValue(self.session_manager.user_session.gui_setup.start_point)
    #     self.__update_eeg_panel()
