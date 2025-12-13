from enum import Enum

import numpy as np
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QPoint, QLineF, QEvent, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QWheelEvent, QMouseEvent, QKeyEvent, QPixmap, QFontMetrics
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollBar, QHBoxLayout, QPushButton
from typing import Optional, List, Dict, Tuple
import math

from weegit import settings
from weegit.gui._utils import milliseconds_to_readable
from weegit.gui.qt_weegit_session_manager_wrapper import QtWeegitSessionManagerWrapper


class TopNavigatorWidget(QWidget):
    """Widget for displaying event names with navigation arrows"""

    event_navigation_requested = pyqtSignal(int)  # Emits new start_point

    def __init__(self, left_margin, right_margin, parent=None):
        super().__init__(parent)
        self._BG_COLOR = QColor(240, 240, 240)  # Same as SignalWidget
        self._TEXT_COLOR = QColor(0, 0, 255)
        self._ARROW_COLOR = QColor(100, 100, 100)
        self._ARROW_HOVER_COLOR = QColor(0, 0, 200)
        self._left_margin = left_margin
        self._right_margin = right_margin

        self._all_events = []
        self._visible_events = []
        self._events_vocabulary: Dict[int, str] = {}
        self._current_sweep_idx: int = 0
        self._start_point = 0
        self._duration_ms = 0.0
        self._sample_rate = 1.0
        self._header_points_per_sweep = 0

        # For hover tracking
        self._hovered_arrow: Optional[Tuple[int, str]] = None  # (event_index, 'left'/'right')
        self.setMouseTracking(True)

        self._font = QFont()
        self._font.setPointSize(12)
        self._font_metrics = QFontMetrics(self._font)

    def update_events(
            self,
            all_events: List,
            visible_events: List,
            events_vocabulary: Dict[int, str],
            sweep_idx: int,
            start_point: int,
            duration_ms: float,
            sample_rate: float,
            header_points_per_sweep: int
    ):
        """Update event data for display"""
        self._all_events = all_events or []
        self._visible_events = visible_events or []
        self._events_vocabulary = events_vocabulary or {}
        self._current_sweep_idx = sweep_idx
        self._start_point = start_point
        self._duration_ms = duration_ms
        self._sample_rate = sample_rate
        self._header_points_per_sweep = header_points_per_sweep
        self.update()

    def paintEvent(self, event):
        if self._duration_ms <= 0:
            return

        painter = QPainter(self)
        painter.fillRect(self.rect(), self._BG_COLOR)
        if not self._visible_events:
            return

        painter.setFont(self._font)
        painter.setPen(self._TEXT_COLOR)

        # Draw events with arrows
        axis_start_x = self._left_margin
        start_time_ms = (self._start_point / self._sample_rate) * 1000
        axis_width = self.width() - self._left_margin

        # Draw arrows
        arrow_size = 10
        arrow_y = 15

        for event in self._visible_events:
            # Draw event name
            name = self._events_vocabulary[event.event_name_id]
            text_width = self._font_metrics.horizontalAdvance(name)
            x = axis_start_x + ((event.time_ms - start_time_ms) / self._duration_ms) * axis_width
            x_pos = int(x)
            text_rect = QRect(int(x_pos - text_width // 2), 5, text_width, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, name)

            # Left arrow
            left_arrow_rect = QRect(int(x_pos - text_width // 2 - arrow_size - 5), arrow_y - arrow_size // 2,
                                    arrow_size, arrow_size)
            self._draw_arrow(painter, left_arrow_rect, 'left',
                             (self._all_events.index(event), 'left') == self._hovered_arrow)

            # Right arrow
            right_arrow_rect = QRect(int(x_pos + text_width // 2 + 5), arrow_y - arrow_size // 2,
                                     arrow_size, arrow_size)
            self._draw_arrow(painter, right_arrow_rect, 'right',
                             (self._all_events.index(event), 'right') == self._hovered_arrow)

    def _draw_arrow(self, painter: QPainter, rect: QRect, direction: str, hovered: bool):
        """Draw an arrow in the given rectangle"""
        color = self._ARROW_HOVER_COLOR if hovered else self._ARROW_COLOR
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw arrow as triangle
        points = []
        if direction == 'left':
            points = [
                QPoint(rect.right(), rect.top()),
                QPoint(rect.left(), rect.center().y()),
                QPoint(rect.right(), rect.bottom())
            ]
        else:  # 'right'
            points = [
                QPoint(rect.left(), rect.top()),
                QPoint(rect.right(), rect.center().y()),
                QPoint(rect.left(), rect.bottom())
            ]

        painter.drawPolygon(points)

    def mouseMoveEvent(self, event):
        """Track mouse movement for arrow hover effects"""
        pos = event.position().toPoint()
        old_hover = self._hovered_arrow
        self._hovered_arrow = None

        axis_start_x = self._left_margin
        start_time_ms = (self._start_point / self._sample_rate) * 1000
        axis_width = self.width() - self._left_margin
        for event in self._visible_events:
            name = self._events_vocabulary[event.event_name_id]
            text_width = self._font_metrics.horizontalAdvance(name)
            x = axis_start_x + ((event.time_ms - start_time_ms) / self._duration_ms) * axis_width
            x_pos = int(x)
            arrow_size = 10

            # Check left arrow
            left_arrow_rect = QRect(int(x_pos - text_width // 2 - arrow_size - 5), 15 - arrow_size // 2,
                                    arrow_size, arrow_size)
            if left_arrow_rect.contains(pos):
                self._hovered_arrow = (self._all_events.index(event), 'left')
                break

            # Check right arrow
            right_arrow_rect = QRect(int(x_pos + text_width // 2 + 5), 15 - arrow_size // 2,
                                     arrow_size, arrow_size)
            if right_arrow_rect.contains(pos):
                self._hovered_arrow = (self._all_events.index(event), 'right')
                break

        if old_hover != self._hovered_arrow:
            self.update()

    def mousePressEvent(self, event):
        """Handle arrow clicks for navigation"""
        if event.button() == Qt.MouseButton.LeftButton and self._hovered_arrow:
            event_idx, direction = self._hovered_arrow
            self._navigate_to_neighbor_event(event_idx, direction)

    def _navigate_to_neighbor_event(self, current_event_idx: int, direction: str):
        """Calculate and emit new start_point to center neighbor event"""
        if not self._all_events:
            return

        current_event = self._all_events[current_event_idx]
        event_name_id = current_event.event_name_id
        sweep_idx = current_event.sweep_idx

        # Find all events with same name in current sweep
        same_name_events = [
            event for event in self._all_events
            if event.event_name_id == event_name_id and event.sweep_idx == sweep_idx
        ]

        if not same_name_events:
            return

        # Find current event in the list
        current_in_list_idx = same_name_events.index(current_event)
        if current_in_list_idx == -1:
            return

        # Get neighbor event
        if direction == 'left':
            neighbor_idx = current_in_list_idx - 1
        else:  # 'right'
            neighbor_idx = current_in_list_idx + 1

        if 0 <= neighbor_idx < len(same_name_events):
            neighbor_event = same_name_events[neighbor_idx]
            # Calculate new start_point to center this event
            new_start_point = self._calculate_start_point_to_center(neighbor_event.time_ms)
            self.event_navigation_requested.emit(new_start_point)

    def _calculate_start_point_to_center(self, target_time_ms: float) -> int:
        """Calculate start_point that centers the target event"""
        # Convert time to samples
        target_samples = int((target_time_ms / 1000.0) * self._sample_rate)

        # Calculate samples for half duration
        half_duration_samples = int((self._duration_ms / 2000.0) * self._sample_rate)

        # Calculate start_point to center the event
        new_start_point = target_samples - half_duration_samples

        # Ensure we don't go out of bounds
        new_start_point = max(0, new_start_point)
        max_start = max(0, self._header_points_per_sweep -
                        int((self._duration_ms / 1000.0) * self._sample_rate))
        new_start_point = min(new_start_point, max_start)

        return new_start_point


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
        self._axis_start_point = 0  # in samples within sweep
        self._axis_duration_ms = 0.0
        self._sample_rate = 1.0
        self._events = []
        self._events_vocabulary: Dict[int, str] = {}
        self._current_sweep_idx: int = 0
        self._traces_are_visible = True
        self._csd_is_visible = False
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
            events=None,
            events_vocabulary: Optional[Dict[int, str]] = None,
            sweep_idx: int = 0,
            traces_are_visible: bool = True,
            csd_is_visible: bool = False,
    ):
        self._axis_start_point = max(0, start_point)
        self._axis_duration_ms = max(0.0, duration_ms)
        self._sample_rate = sample_rate if sample_rate > 0 else 1.0
        self._events = events or []
        self._events_vocabulary = events_vocabulary or {}
        self._current_sweep_idx = sweep_idx
        self._traces_are_visible = traces_are_visible
        self._csd_is_visible = csd_is_visible

        self.pixmap_cache = QPixmap(self.size())

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

            if self._traces_are_visible:
                self.draw_middle_line(painter, channel_rects[channel_idx])

        if self._traces_are_visible:
            for cur_draw_idx, channel_idx in enumerate(visible_channel_indexes):
                self.draw_signal(
                    painter,
                    processed_data[channel_idx],
                    channel_rects[channel_idx],
                    voltage_scale,
                    channel_idx,
                    cur_draw_idx,
                )

        if self._csd_is_visible:
            pass
            # todo: implement
            # self.draw_csd()

        self._draw_time_axis(painter, width, height)
        self._draw_events(painter, width, height, draw_area_height)
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
            text_rect = QRect(int(x) - 50, axis_y + label_offset, 100, 15)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

            time_ms += tick_interval

    def _draw_events(self, painter: QPainter, width: int, height: int, draw_area_height: int):
        """Draw vertical lines for events in the current sweep/time window."""
        if not self._events or self._axis_duration_ms <= 0 or self._sample_rate <= 0:
            return

        axis_start_x = self._left_margin
        axis_end_x = max(axis_start_x, width - self._right_margin)
        axis_width = axis_end_x - axis_start_x
        if axis_width <= 0:
            return

        start_time_ms = (self._axis_start_point / self._sample_rate) * 1000.0
        end_time_ms = start_time_ms + self._axis_duration_ms

        pen = QPen(QColor(0, 0, 255), 1.5)
        painter.setPen(pen)

        for event in self._events:
            if event.sweep_idx != self._current_sweep_idx:
                continue
            if not (start_time_ms <= event.time_ms <= end_time_ms):
                continue

            x = axis_start_x + ((event.time_ms - start_time_ms) / self._axis_duration_ms) * axis_width
            x_int = int(x)
            # Vertical line across signal area (no labels here)
            painter.drawLine(x_int, 0, x_int, draw_area_height)

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

    def draw_csd(self, *args, **kwargs):
        raise NotImplemented

    def get_channel_scale(self, channel_idx: int) -> float:
        return 1.0

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


class OverlayModeEnum(Enum):
    NONE = 0
    TIME_VOLTAGE_BAR = 1
    PICK = 2
    EVENT_ADD = 3


class OverlayWidget(QWidget):
    """Transparent overlay that draws time/voltage scale bars at the cursor."""

    def __init__(self, left_margin, right_margin, bottom_margin, bar_width, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._left_margin = left_margin
        self._right_margin = right_margin
        self._bottom_margin = bottom_margin
        self._bar_width = bar_width

        self._cursor_pos: Optional[QPoint] = None
        self._overlay_mode = OverlayModeEnum.NONE
        self._channel_height = 0
        self._duration_ms = 0.0
        self._scale_value = 1.0
        self._font = QFont()
        self._font.setPointSize(12)
        self._font_metrics = QFontMetrics(self._font)

    def update_state(self, *, cursor_pos: Optional[QPoint], overlay_mode: OverlayModeEnum,
                     channel_height: int, duration_ms: float, scale_value: float):
        self._cursor_pos = cursor_pos
        self._overlay_mode = overlay_mode
        self._channel_height = max(0, channel_height)
        self._duration_ms = max(0.0, duration_ms)
        self._scale_value = scale_value if scale_value > 0 else 1.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._cursor_pos:
            if self._overlay_mode in (OverlayModeEnum.PICK, OverlayModeEnum.EVENT_ADD):
                pen = QPen(Qt.GlobalColor.green, 1, Qt.PenStyle.SolidLine)
                painter.setPen(pen)
                painter.drawLine(0, self._cursor_pos.y(), self.width(), self._cursor_pos.y())
                painter.drawLine(self._cursor_pos.x(), 0, self._cursor_pos.x(), self.height())

            if self._overlay_mode == OverlayModeEnum.TIME_VOLTAGE_BAR:
                painter.setPen(QPen(QColor(255, 0, 0)))
                painter.setFont(self._font)
                self._draw_voltage_scale_bar(painter)
                self._draw_time_scale_bar(painter)

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
        x = max(0, min(x, self.width() - self._right_margin - time_bar_pixels))

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
        self._current_overlay_mode = OverlayModeEnum.NONE
        self._current_mouse_pos = None
        self._BAR_WIDTH = 3
        self._current_event_add_id: Optional[int] = None

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

        # Top navigator widget for event names with arrows
        self.top_navigator_widget = TopNavigatorWidget(self._LEFT_MARGIN, self._RIGHT_MARGIN)
        self.top_navigator_widget.setFixedHeight(self._TOP_MARGIN)
        main_layout.addWidget(self.top_navigator_widget)

        # Connect navigation signal
        self.top_navigator_widget.event_navigation_requested.connect(
            self._session_manager.set_start_point
        )

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
        self.overlay_widget = OverlayWidget(self._LEFT_MARGIN, self._RIGHT_MARGIN,
                                            self._BOTTOM_MARGIN, self._BAR_WIDTH, self.signal_widget, )
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

        self._session_manager.session_loaded.connect(self.on_session_loaded)
        self._session_manager.start_point_changed.connect(self.on_start_point_changed)

    def eventFilter(self, watched, event):
        if watched is self.signal_widget:
            if event.type() == QEvent.Type.MouseMove and isinstance(event, QMouseEvent):
                pos = event.position().toPoint()
                if self.signal_widget.rect().contains(pos):
                    self._current_mouse_pos = pos
                    if not self._current_overlay_mode == OverlayModeEnum.NONE:
                        self.setCursor(Qt.CursorShape.BlankCursor)
                else:
                    self._current_mouse_pos = None
                    self.unsetCursor()

                self._update_overlay_widget()
            elif event.type() == QEvent.Type.Leave:
                self._current_mouse_pos = None
                self.unsetCursor()
                self._update_overlay_widget()
            elif event.type() == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
                if self._current_overlay_mode == OverlayModeEnum.EVENT_ADD:
                    button = event.button()
                    if button == Qt.MouseButton.LeftButton:
                        self._handle_event_add_click(event)
                        return True
                    elif button == Qt.MouseButton.RightButton:
                        self._stop_event_add_mode()
                        return True
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

        # Collect events for current window
        visible_events = self._get_events_for_current_window(gui_setup, sample_rate)

        # Update top navigator widget
        self.top_navigator_widget.update_events(
            all_events=self._session_manager.events,
            visible_events=visible_events,
            events_vocabulary=self._session_manager.events_vocabulary,
            sweep_idx=gui_setup.current_sweep_idx,
            start_point=gui_setup.start_point,
            duration_ms=gui_setup.duration_ms,
            sample_rate=sample_rate,
            header_points_per_sweep=self._session_manager.header.number_of_points_per_sweep
        )

        # Update signal widget (without event labels)
        self.signal_widget.reset_data_and_redraw(
            self._cached_processed_data,
            self.get_visible_channel_indexes(),
            self._session_manager.header.channel_info.name,
            gui_setup.scale,
            start_point=gui_setup.start_point,
            duration_ms=gui_setup.duration_ms,
            sample_rate=sample_rate,
            events=visible_events,
            events_vocabulary=self._session_manager.events_vocabulary,
            sweep_idx=gui_setup.current_sweep_idx,
            traces_are_visible=gui_setup.traces_are_shown,
            csd_is_visible=gui_setup.csd_is_shown,
        )

        self._update_overlay_widget()

    def _get_events_for_current_window(self, gui_setup, sample_rate: float):
        """Return events that fall into the current time window and sweep."""
        if not self._session_manager or not self._session_manager.current_user_session:
            return []

        header = self._session_manager.header
        if not header:
            return []

        # Convert start_point (samples within sweep) to ms
        sample_interval_ms = header.sample_interval_microseconds / 1000.0
        start_time_ms = gui_setup.start_point * sample_interval_ms
        end_time_ms = start_time_ms + gui_setup.duration_ms
        sweep_idx = gui_setup.current_sweep_idx

        events = getattr(self._session_manager, "events", [])
        if not events:
            return []

        return [
            e
            for e in events
            if e.sweep_idx == sweep_idx and start_time_ms <= e.time_ms <= end_time_ms
        ]

    def _update_overlay_widget(self):
        if not hasattr(self, 'overlay_widget') or self.overlay_widget is None:
            return

        gui_setup = self._session_manager.gui_setup if self._session_manager else None
        duration_ms = gui_setup.duration_ms if gui_setup else 0.0
        scale_value = gui_setup.scale if gui_setup else 1.0
        channel_height = self.signal_widget._channel_height or self._channel_height

        self.overlay_widget.update_state(
            cursor_pos=self._current_mouse_pos,
            overlay_mode=self._current_overlay_mode,
            channel_height=channel_height,
            duration_ms=duration_ms,
            scale_value=scale_value
        )

    # ---- Events helper API ----
    def start_event_add_mode(self, event_name_id: int):
        """Enable interactive event placement for the given vocabulary id."""
        self._current_event_add_id = event_name_id
        self._current_overlay_mode = OverlayModeEnum.EVENT_ADD
        self.setCursor(Qt.CursorShape.BlankCursor)
        self._update_overlay_widget()

    def _stop_event_add_mode(self):
        self._current_event_add_id = None
        if self._current_overlay_mode == OverlayModeEnum.EVENT_ADD:
            self._current_overlay_mode = OverlayModeEnum.NONE
            self.unsetCursor()
        self._update_overlay_widget()

    def _handle_event_add_click(self, event: QMouseEvent):
        """Handle left click when in EVENT_ADD mode: compute time_ms and create event."""
        if self._current_event_add_id is None:
            return

        pos = event.position().toPoint()
        # Only allow clicks inside signal area horizontally
        left = self._LEFT_MARGIN
        right = self.signal_widget.width() - self._RIGHT_MARGIN
        if right <= left or pos.x() < left or pos.x() > right:
            return

        gui_setup = self._session_manager.gui_setup
        if not gui_setup:
            return

        sample_rate = self.get_sample_rate()
        start_time_ms = (gui_setup.start_point / sample_rate) * 1000.0
        duration_ms = gui_setup.duration_ms
        if duration_ms <= 0:
            return

        rel = (pos.x() - left) / (right - left)
        rel = max(0.0, min(1.0, rel))
        time_ms = start_time_ms + rel * duration_ms

        self._session_manager.add_event(
            event_name_id=self._current_event_add_id,
            sweep_idx=gui_setup.current_sweep_idx,
            time_ms=time_ms,
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
        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes
        visible_channel_indexes = [ch for ch in eeg_channels if ch in self._current_visible_channel_indexes()]

        total_channels = len(visible_channel_indexes)
        if total_channels > self._session_manager.gui_setup.number_of_channels_to_show:
            self.channel_scrollbar.setMaximum(
                total_channels - self._session_manager.gui_setup.number_of_channels_to_show)
            self.channel_scrollbar.setVisible(True)
        else:
            self.channel_scrollbar.setMaximum(0)
            self.channel_scrollbar.setVisible(False)

    def get_sample_rate(self) -> float:
        """Get sample rate from header"""
        if not self._session_manager.header:
            return 1.0
        sample_interval_seconds = self._session_manager.header.sample_interval_microseconds / 1_000_000.0
        return 1.0 / sample_interval_seconds if sample_interval_seconds > 0 else 1.0

    def get_visible_channel_indexes(self) -> List[int]:
        """Get currently visible channels considering scroll position"""
        if not self._session_manager.current_user_session:
            return []

        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes
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

    def on_start_point_changed(self, value):
        self.time_scrollbar.setValue(value)

    def on_session_loaded(self):
        total_points = self._session_manager.header.number_of_points_per_sweep
        visible_points = int((self._session_manager.gui_setup.duration_ms / 1000.0) * self.get_sample_rate())
        self.time_scrollbar.setMaximum(max(0, total_points - visible_points))
        self.time_scrollbar.setValue(self._session_manager.gui_setup.start_point)

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

    # FOR FUN
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        key = event.key()
        if key in {Qt.Key.Key_M, Qt.Key.Key_P, Qt.Key.Key_Escape}:
            if key == Qt.Key.Key_Escape and self._current_overlay_mode == OverlayModeEnum.EVENT_ADD:
                self._stop_event_add_mode()
                self._update_overlay_widget()
                event.accept()
                return
            if key == Qt.Key.Key_M:
                # Toggle voltage scale bar with 'M' key
                if self._current_overlay_mode == OverlayModeEnum.NONE:
                    self._current_overlay_mode = OverlayModeEnum.TIME_VOLTAGE_BAR
                    self.setCursor(Qt.CursorShape.BlankCursor)
                elif self._current_overlay_mode == OverlayModeEnum.TIME_VOLTAGE_BAR:
                    self._current_overlay_mode = OverlayModeEnum.NONE
                    self.unsetCursor()

            self._update_overlay_widget()
            event.accept()
        else:
            super().keyPressEvent(event)

    def leaveEvent(self, event):
        """Hide scale when mouse leaves"""
        self._update_overlay_widget()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Set focus when clicked"""
        self.setFocus()
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier and self._session_manager.gui_setup:
            cursor_x = event.position().x()
            widget_width = self.width()

            if cursor_x < 0 or cursor_x > widget_width:
                return

            rel_pos = cursor_x / widget_width
            current_zoom = 10000 / self._session_manager.gui_setup.duration_ms
            scale_factor = 2.0 + (0.1 / max(1.0, current_zoom ** 0.5))
            voltage_scale_dif = 0.2
            delta = event.angleDelta().y()
            if delta > 0:  # zoom in
                new_duration = self._session_manager.gui_setup.duration_ms / scale_factor
                new_start_point = (self._session_manager.gui_setup.start_point
                                   + (self._session_manager.gui_setup.duration_ms - new_duration) / 1000.0
                                   * self.get_sample_rate() * rel_pos)
                new_scale = min(self._session_manager.gui_setup.scale + voltage_scale_dif, settings.MAX_SCALE)
            else:  # zoom out
                new_duration = self._session_manager.gui_setup.duration_ms * scale_factor
                new_start_point = (self._session_manager.gui_setup.start_point
                                   - (new_duration - self._session_manager.gui_setup.duration_ms) / 1000.0
                                   * self.get_sample_rate() * rel_pos)
                new_scale = max(self._session_manager.gui_setup.scale - voltage_scale_dif, settings.MIN_SCALE)

            self._session_manager.set_start_point(int(new_start_point))
            self._session_manager.set_duration_ms(int(new_duration))
            self._session_manager.set_scale(new_scale)
            event.accept()
        else:
            super().wheelEvent(event)
