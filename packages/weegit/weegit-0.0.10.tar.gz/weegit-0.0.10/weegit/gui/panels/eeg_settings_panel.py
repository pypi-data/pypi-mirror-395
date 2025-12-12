from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
    QListWidget, QListWidgetItem, QCheckBox, QGroupBox, QPushButton,
    QAbstractItemView, QToolButton
)
from typing import List

from weegit import settings
from weegit.gui._utils import milliseconds_to_readable
from weegit.gui.qt_weegit_session_manager_wrapper import QtWeegitSessionManagerWrapper


class EegSettingsPanel(QWidget):
    """Settings panel for EEG visualization parameters with drag & drop channel management"""

    def __init__(self, session_manager: QtWeegitSessionManagerWrapper, parent=None):
        super().__init__(parent)

        self._session_manager = session_manager
        self._drag_drop_in_progress = False

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Time settings group
        time_group = QGroupBox("Time Settings")
        time_layout = QVBoxLayout(time_group)

        # Start point
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start point index:"))
        self.start_point_spinbox = QSpinBox()
        self.start_point_spinbox.setRange(0, settings.MAX_START_POINT)
        self.start_point_spinbox.setSingleStep(1000)
        start_layout.addWidget(self.start_point_spinbox)
        time_layout.addLayout(start_layout)

        # Duration
        duration_layout = QHBoxLayout()
        self.duration_label = QLabel("Duration (ms):")
        duration_layout.addWidget(self.duration_label)
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(settings.MIN_DURATION, settings.MAX_DURATION)
        self.duration_spinbox.setSingleStep(100)
        self.duration_spinbox.setValue(1000)
        duration_layout.addWidget(self.duration_spinbox)
        time_layout.addLayout(duration_layout)

        # Time step
        time_step_layout = QHBoxLayout()
        self.time_step_label = QLabel("Time step (ms):")
        time_step_layout.addWidget(self.time_step_label)
        self.time_step_spinbox = QSpinBox()
        self.time_step_spinbox.setRange(settings.MIN_TIME_STEP, settings.MAX_TIME_STEP)
        self.time_step_spinbox.setSingleStep(100)
        self.time_step_spinbox.setValue(1000)
        time_step_layout.addWidget(self.time_step_spinbox)
        time_layout.addLayout(time_step_layout)

        # Number of dots to display
        number_of_dots_layout = QHBoxLayout()
        self.number_of_dots_label = QLabel("Number of dots to display:")
        number_of_dots_layout.addWidget(self.number_of_dots_label)
        self.number_of_dots_spinbox = QSpinBox()
        self.number_of_dots_spinbox.setRange(settings.MIN_NUMBER_OF_DOTS_TO_DISPLAY,
                                             settings.MAX_NUMBER_OF_DOTS_TO_DISPLAY)
        self.number_of_dots_spinbox.setSingleStep(100)
        self.number_of_dots_spinbox.setValue(settings.EEG_DEFAULT_NUMBER_OF_DOTS_TO_DISPLAY)
        number_of_dots_layout.addWidget(self.number_of_dots_spinbox)
        time_layout.addLayout(number_of_dots_layout)

        # Scale
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Voltage scale:"))
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(settings.MIN_SCALE, settings.MAX_SCALE)
        self.scale_spinbox.setSingleStep(0.1)
        self.scale_spinbox.setValue(1.0)
        scale_layout.addWidget(self.scale_spinbox)
        time_layout.addLayout(scale_layout)

        layout.addWidget(time_group)

        # Channel management group
        channel_group = QGroupBox("Channel Management")
        channel_layout = QVBoxLayout(channel_group)

        # Instructions
        instructions = QLabel("Use buttons to move channels. Check/uncheck to show/hide. Use arrows to reorder.")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray; font-size: 9pt;")
        channel_layout.addWidget(instructions)

        number_of_channels_to_show_layout = QHBoxLayout()
        number_of_channels_to_show_layout.addWidget(QLabel("Number of channels to show:"))
        self.number_of_channel_spinbox = QSpinBox()
        self.number_of_channel_spinbox.setRange(settings.MIN_VISIBLE_CHANNELS, settings.MAX_VISIBLE_CHANNELS)
        self.number_of_channel_spinbox.setSingleStep(1)
        self.number_of_channel_spinbox.setValue(settings.MAX_VISIBLE_CHANNELS)
        number_of_channels_to_show_layout.addWidget(self.number_of_channel_spinbox)
        channel_layout.addLayout(number_of_channels_to_show_layout)

        # Channel lists container
        lists_container = QVBoxLayout()

        # EEG Channels list
        eeg_group = QGroupBox("EEG Channels")
        eeg_layout = QVBoxLayout(eeg_group)
        self.eeg_list = QListWidget()
        self.eeg_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.eeg_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.eeg_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.eeg_list.setDragEnabled(True)
        self.eeg_list.setAcceptDrops(True)
        self.eeg_list.setMinimumHeight(200)
        self.eeg_list.setMaximumHeight(200)
        eeg_layout.addWidget(self.eeg_list)
        eeg_button_layout = QHBoxLayout()
        self.select_all_eeg_btn = QPushButton("Select All EEG")
        self.deselect_all_eeg_btn = QPushButton("Deselect All EEG")
        eeg_button_layout.addWidget(self.select_all_eeg_btn)
        eeg_button_layout.addWidget(self.deselect_all_eeg_btn)
        eeg_layout.addLayout(eeg_button_layout)
        lists_container.addWidget(eeg_group)

        # Analog Channels list
        analog_group = QGroupBox("Analog Channels")
        analog_layout = QVBoxLayout(analog_group)
        self.analog_list = QListWidget()
        self.analog_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.analog_list.setMinimumHeight(200)
        self.analog_list.setMaximumHeight(200)
        self.analog_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.analog_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.analog_list.setDragEnabled(True)
        self.analog_list.setAcceptDrops(True)
        analog_layout.addWidget(self.analog_list)
        analog_button_layout = QHBoxLayout()
        self.select_all_analog_btn = QPushButton("Select All Analog")
        self.deselect_all_analog_btn = QPushButton("Deselect All Analog")
        analog_button_layout.addWidget(self.select_all_analog_btn)
        analog_button_layout.addWidget(self.deselect_all_analog_btn)
        analog_layout.addLayout(analog_button_layout)

        lists_container.addWidget(analog_group)

        channel_layout.addLayout(lists_container)

        layout.addWidget(channel_group)
        layout.addStretch(1)

    def connect_signals(self):
        """Connect all signals to their handlers"""
        # Time parameter changes
        self.start_point_spinbox.valueChanged.connect(self.on_start_point_changed)
        self.duration_spinbox.valueChanged.connect(self.on_duration_ms_changed)
        self.time_step_spinbox.valueChanged.connect(self.on_time_step_changed)
        self.number_of_dots_spinbox.valueChanged.connect(self.on_number_of_dots_changed)
        self.scale_spinbox.valueChanged.connect(self.on_scale_changed)
        self.number_of_channel_spinbox.valueChanged.connect(self.on_number_of_channels_changed)

        # Button clicks
        self.select_all_eeg_btn.clicked.connect(self.select_all_eeg)
        self.deselect_all_eeg_btn.clicked.connect(self.deselect_all_eeg)
        self.select_all_analog_btn.clicked.connect(self.select_all_analog)
        self.deselect_all_analog_btn.clicked.connect(self.deselect_all_analog)

        # Connect drag & drop completion signals
        self.eeg_list.model().rowsMoved.connect(self.on_eeg_rows_moved)
        self.analog_list.model().rowsMoved.connect(self.on_analog_rows_moved)

        # Weegit session
        self._session_manager.session_loaded.connect(self.on_session_loaded)
        self._session_manager.start_point_changed.connect(self.on_session_start_point_changed)
        self._session_manager.time_step_ms_changed.connect(self.on_session_time_step_ms_changed)
        self._session_manager.duration_ms_changed.connect(self.on_session_duration_ms_changed)
        self._session_manager.scale_changed.connect(self.on_session_scale_changed)
        self._session_manager.number_of_channels_to_show_changed.connect(self.on_session_number_of_channels_changed)
        self._session_manager.eeg_channel_indexes_changed.connect(self.on_eeg_channels_changed)
        self._session_manager.analogue_input_channel_indexes_changed.connect(self.on_analog_channels_changed)
        self._session_manager.visible_channel_indexes_changed.connect(self.on_visible_channels_changed)

    def on_eeg_rows_moved(self, parent, start, end, destination, row):
        """Handle when EEG rows are moved via drag & drop"""
        if self._drag_drop_in_progress:
            return

        self._drag_drop_in_progress = True
        try:
            # Get current order from the list
            new_order = []
            for i in range(self.eeg_list.count()):
                item = self.eeg_list.item(i)
                channel_idx = item.data(Qt.ItemDataRole.UserRole)
                new_order.append(channel_idx)

            # Update session manager with new order
            if self._session_manager.gui_setup:
                self._session_manager.set_eeg_channel_indexes(new_order)
        finally:
            self._drag_drop_in_progress = False

    def on_analog_rows_moved(self, parent, start, end, destination, row):
        """Handle when Analog rows are moved via drag & drop"""
        if self._drag_drop_in_progress:
            return

        self._drag_drop_in_progress = True
        try:
            # Get current order from the list
            new_order = []
            for i in range(self.analog_list.count()):
                item = self.analog_list.item(i)
                channel_idx = item.data(Qt.ItemDataRole.UserRole)
                new_order.append(channel_idx)

            # Update session manager with new order
            if self._session_manager.gui_setup:
                self._session_manager.set_analogue_input_channel_indexes(new_order)
        finally:
            self._drag_drop_in_progress = False

    def on_session_loaded(self):
        if not self._session_manager.gui_setup or not self._session_manager.header:
            return

        # Block signals to prevent recursive updates
        self.start_point_spinbox.blockSignals(True)
        self.duration_spinbox.blockSignals(True)
        self.time_step_spinbox.blockSignals(True)
        self.number_of_dots_spinbox.blockSignals(True)
        self.scale_spinbox.blockSignals(True)
        self.number_of_channel_spinbox.blockSignals(True)

        # Update time parameters
        self.start_point_spinbox.setValue(self._session_manager.gui_setup.start_point)
        self.duration_spinbox.setValue(self._session_manager.gui_setup.duration_ms)
        self.duration_label.setText(
            f"Duration (ms) {milliseconds_to_readable(self._session_manager.gui_setup.duration_ms)}")
        self.time_step_spinbox.setValue(self._session_manager.gui_setup.time_step_ms)
        self.time_step_label.setText(
            f"Time Step (ms) {milliseconds_to_readable(self._session_manager.gui_setup.time_step_ms)}")
        self.number_of_dots_spinbox.setValue(self._session_manager.gui_setup.number_of_dots_to_display)
        self.scale_spinbox.setValue(self._session_manager.gui_setup.scale)
        self.number_of_channel_spinbox.setValue(self._session_manager.gui_setup.number_of_channels_to_show)

        # Unblock signals
        self.start_point_spinbox.blockSignals(False)
        self.duration_spinbox.blockSignals(False)
        self.time_step_spinbox.blockSignals(False)
        self.number_of_dots_spinbox.blockSignals(False)
        self.scale_spinbox.blockSignals(False)
        self.number_of_channel_spinbox.blockSignals(False)

        # Update channel lists
        self.update_channel_lists()

    def on_session_start_point_changed(self, value):
        self.start_point_spinbox.blockSignals(True)
        self.start_point_spinbox.setValue(value)
        self.start_point_spinbox.blockSignals(False)

    def on_session_time_step_ms_changed(self, value):
        self.time_step_spinbox.blockSignals(True)
        self.time_step_spinbox.setValue(value)
        self.time_step_label.setText(
            f"Time Step (ms) {milliseconds_to_readable(self._session_manager.gui_setup.time_step_ms)}")
        self.time_step_spinbox.blockSignals(False)

    def on_session_duration_ms_changed(self, value):
        self.duration_spinbox.blockSignals(True)
        self.duration_spinbox.setValue(value)
        self.duration_label.setText(
            f"Duration (ms) {milliseconds_to_readable(self._session_manager.gui_setup.duration_ms)}")
        self.duration_spinbox.blockSignals(False)

    def on_session_scale_changed(self, value):
        self.scale_spinbox.blockSignals(True)
        self.scale_spinbox.setValue(value)
        self.scale_spinbox.blockSignals(False)

    def on_session_number_of_channels_changed(self, value):
        self.number_of_channel_spinbox.blockSignals(True)
        self.number_of_channel_spinbox.setValue(value)
        self.number_of_channel_spinbox.blockSignals(False)

    def on_eeg_channels_changed(self, channels: List[int]):
        """Update EEG channels when changed externally"""
        # Only update if not currently in a drag & drop operation
        if not self._drag_drop_in_progress:
            self.update_channel_lists()

    def on_analog_channels_changed(self, channels: List[int]):
        """Update analog channels when changed externally"""
        # Only update if not currently in a drag & drop operation
        if not self._drag_drop_in_progress:
            self.update_channel_lists()

    def on_visible_channels_changed(self, channels: List[int]):
        """Update visibility checkboxes when changed externally"""
        self.update_channel_visibility(channels)

    def update_channel_lists(self):
        """Update the EEG and Analog channel lists"""
        if not self._session_manager.gui_setup or not self._session_manager.header:
            return

        # Block drag & drop signals while updating
        self._drag_drop_in_progress = True

        try:
            # Clear existing lists
            self.eeg_list.clear()
            self.analog_list.clear()

            # Create EEG channel items in the exact order from session manager
            for channel_idx in self._session_manager.current_user_session.eeg_channel_indexes:
                if channel_idx < len(self._session_manager.header.channel_info.name):
                    self.add_eeg_channel_item(channel_idx)

            # Create Analog channel items in the exact order from session manager
            for channel_idx in self._session_manager.current_user_session.analogue_input_channel_indexes:
                if channel_idx < len(self._session_manager.header.channel_info.name):
                    self.add_analog_channel_item(channel_idx)

            # Update visibility based on current settings
            if self._session_manager.gui_setup:
                self.update_channel_visibility(self._session_manager.gui_setup.visible_channel_indexes)
        finally:
            self._drag_drop_in_progress = False

    def update_channel_visibility(self, visible_channels: List[int]):
        """Update checkboxes based on visible channels list"""
        # Update EEG list visibility
        for i in range(self.eeg_list.count()):
            item = self.eeg_list.item(i)
            channel_idx = item.data(Qt.ItemDataRole.UserRole)
            widget = self.eeg_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(channel_idx in visible_channels)
                    checkbox.blockSignals(False)

        # Update Analog list visibility
        for i in range(self.analog_list.count()):
            item = self.analog_list.item(i)
            channel_idx = item.data(Qt.ItemDataRole.UserRole)
            widget = self.analog_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(channel_idx in visible_channels)
                    checkbox.blockSignals(False)

    def add_eeg_channel_item(self, channel_idx: int):
        """Add a channel item to the EEG list with move to analog button and reordering arrows"""
        channel_name = self.get_channel_name(channel_idx)

        # Create custom widget for list item
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(2, 2, 2, 2)

        # Checkbox for visibility
        checkbox = QCheckBox()
        checkbox.setChecked(channel_idx in self._session_manager.gui_setup.visible_channel_indexes)
        checkbox.stateChanged.connect(lambda state, idx=channel_idx: self.on_channel_visibility_changed(idx, state))

        # Channel label
        label = QLabel(channel_name)
        label.setToolTip(f"Channel {channel_idx}: {channel_name}")

        # Up button
        up_btn = QToolButton()
        up_btn.setText("↑")
        up_btn.setMaximumWidth(20)
        up_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_eeg_channel_up(idx))

        # Down button
        down_btn = QToolButton()
        down_btn.setText("↓")
        down_btn.setMaximumWidth(20)
        down_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_eeg_channel_down(idx))

        # Move to analog button
        move_btn = QPushButton("→ Analog")
        move_btn.setMaximumWidth(70)
        move_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_channel_to_analog(idx))

        item_layout.addWidget(checkbox)
        item_layout.addWidget(label)
        item_layout.addStretch(1)
        item_layout.addWidget(up_btn)
        item_layout.addWidget(down_btn)
        item_layout.addWidget(move_btn)

        # Create list item
        item = QListWidgetItem(self.eeg_list)
        item.setData(Qt.ItemDataRole.UserRole, channel_idx)  # Store channel index
        item.setSizeHint(item_widget.sizeHint())

        self.eeg_list.addItem(item)
        self.eeg_list.setItemWidget(item, item_widget)

    def add_analog_channel_item(self, channel_idx: int):
        """Add a channel item to the Analog list with move to EEG button and reordering arrows"""
        channel_name = self.get_channel_name(channel_idx)

        # Create custom widget for list item
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(2, 2, 2, 2)

        # Checkbox for visibility
        checkbox = QCheckBox()
        checkbox.setChecked(channel_idx in self._session_manager.gui_setup.visible_channel_indexes)
        checkbox.stateChanged.connect(lambda state, idx=channel_idx: self.on_channel_visibility_changed(idx, state))

        # Channel label
        label = QLabel(channel_name)
        label.setToolTip(f"Channel {channel_idx}: {channel_name}")

        # Up button
        up_btn = QToolButton()
        up_btn.setText("↑")
        up_btn.setMaximumWidth(20)
        up_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_analog_channel_up(idx))

        # Down button
        down_btn = QToolButton()
        down_btn.setText("↓")
        down_btn.setMaximumWidth(20)
        down_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_analog_channel_down(idx))

        # Move to EEG button
        move_btn = QPushButton("→ EEG")
        move_btn.setMaximumWidth(70)
        move_btn.clicked.connect(lambda checked, idx=channel_idx: self.move_channel_to_eeg(idx))

        item_layout.addWidget(checkbox)
        item_layout.addWidget(label)
        item_layout.addStretch(1)
        item_layout.addWidget(up_btn)
        item_layout.addWidget(down_btn)
        item_layout.addWidget(move_btn)

        # Create list item
        item = QListWidgetItem(self.analog_list)
        item.setData(Qt.ItemDataRole.UserRole, channel_idx)  # Store channel index
        item.setSizeHint(item_widget.sizeHint())

        self.analog_list.addItem(item)
        self.analog_list.setItemWidget(item, item_widget)

    def move_channel_to_analog(self, channel_idx: int):
        """Move a channel from EEG to Analog list and update session manager"""
        if not self._session_manager.gui_setup:
            return

        # Get current lists
        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes.copy()
        analog_channels = self._session_manager.current_user_session.analogue_input_channel_indexes.copy()

        # Remove from EEG and add to Analog (preserving order)
        if channel_idx in eeg_channels:
            eeg_channels.remove(channel_idx)
            analog_channels.insert(0, channel_idx)  # Add to end of analog list

        # Update session manager
        self._session_manager.set_eeg_channel_indexes(eeg_channels)
        self._session_manager.set_analogue_input_channel_indexes(analog_channels)

    def move_channel_to_eeg(self, channel_idx: int):
        """Move a channel from Analog to EEG list and update session manager"""
        if not self._session_manager.gui_setup:
            return

        # Get current lists
        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes.copy()
        analog_channels = self._session_manager.current_user_session.analogue_input_channel_indexes.copy()

        # Remove from Analog and add to EEG (preserving order)
        if channel_idx in analog_channels:
            analog_channels.remove(channel_idx)
            eeg_channels.insert(0, channel_idx)  # Add to end of EEG list

        # Update session manager
        self._session_manager.set_eeg_channel_indexes(eeg_channels)
        self._session_manager.set_analogue_input_channel_indexes(analog_channels)

    def move_eeg_channel_up(self, channel_idx: int):
        """Move EEG channel up in the list"""
        if not self._session_manager.gui_setup:
            return

        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes.copy()
        if channel_idx in eeg_channels:
            index = eeg_channels.index(channel_idx)
            if index > 0:  # Can move up
                # Swap with previous channel
                eeg_channels[index], eeg_channels[index - 1] = eeg_channels[index - 1], eeg_channels[index]
                self._session_manager.set_eeg_channel_indexes(eeg_channels)

    def move_eeg_channel_down(self, channel_idx: int):
        """Move EEG channel down in the list"""
        if not self._session_manager.gui_setup:
            return

        eeg_channels = self._session_manager.current_user_session.eeg_channel_indexes.copy()
        if channel_idx in eeg_channels:
            index = eeg_channels.index(channel_idx)
            if index < len(eeg_channels) - 1:  # Can move down
                # Swap with next channel
                eeg_channels[index], eeg_channels[index + 1] = eeg_channels[index + 1], eeg_channels[index]
                self._session_manager.set_eeg_channel_indexes(eeg_channels)

    def move_analog_channel_up(self, channel_idx: int):
        """Move Analog channel up in the list"""
        if not self._session_manager.gui_setup:
            return

        analog_channels = self._session_manager.current_user_session.analogue_input_channel_indexes.copy()
        if channel_idx in analog_channels:
            index = analog_channels.index(channel_idx)
            if index > 0:  # Can move up
                # Swap with previous channel
                analog_channels[index], analog_channels[index - 1] = analog_channels[index - 1], analog_channels[index]
                self._session_manager.set_analogue_input_channel_indexes(analog_channels)

    def move_analog_channel_down(self, channel_idx: int):
        """Move Analog channel down in the list"""
        if not self._session_manager.gui_setup:
            return

        analog_channels = self._session_manager.current_user_session.analogue_input_channel_indexes.copy()
        if channel_idx in analog_channels:
            index = analog_channels.index(channel_idx)
            if index < len(analog_channels) - 1:  # Can move down
                # Swap with next channel
                analog_channels[index], analog_channels[index + 1] = analog_channels[index + 1], analog_channels[index]
                self._session_manager.set_analogue_input_channel_indexes(analog_channels)

    def get_channel_name(self, channel_idx: int) -> str:
        """Get channel name from header, fallback to index"""
        if (self._session_manager.header and self._session_manager.header.channel_info and
                self._session_manager.header.channel_info.name and
                channel_idx < len(self._session_manager.header.channel_info.name)):
            return self._session_manager.header.channel_info.name[channel_idx]

        return f"Channel {channel_idx}"

    def get_current_visible_channel_indexes(self):
        """Get currently visible channels from checkboxes"""
        visible_channel_indexes = []

        # Check EEG list
        for i in range(self.eeg_list.count()):
            item = self.eeg_list.item(i)
            widget = self.eeg_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    channel_idx = item.data(Qt.ItemDataRole.UserRole)
                    visible_channel_indexes.append(channel_idx)

        # Check Analog list
        for i in range(self.analog_list.count()):
            item = self.analog_list.item(i)
            widget = self.analog_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    channel_idx = item.data(Qt.ItemDataRole.UserRole)
                    visible_channel_indexes.append(channel_idx)

        return visible_channel_indexes

    def on_start_point_changed(self, value):
        self._session_manager.set_start_point(value)

    def on_duration_ms_changed(self, value):
        self._session_manager.set_duration_ms(value)

    def on_time_step_changed(self, value: int):
        self._session_manager.set_time_step_ms(value)

    def on_number_of_dots_changed(self, value: int):
        self._session_manager.set_number_of_dots_to_display(value)

    def on_scale_changed(self, value: int):
        self._session_manager.set_scale(value)

    def on_number_of_channels_changed(self, value: int):
        self._session_manager.set_number_of_channels_to_show(value)

    def on_channel_visibility_changed(self, channel_idx: int, state: int):
        visible_channel_indexes = self.get_current_visible_channel_indexes()
        self._session_manager.set_visible_channel_indexes(visible_channel_indexes)

    def select_all_eeg(self):
        """Select all EEG channels"""
        self.set_all_eeg_visibility(True)

    def deselect_all_eeg(self):
        """Deselect all EEG channels"""
        self.set_all_eeg_visibility(False)

    def select_all_analog(self):
        """Select all Analog channels"""
        self.set_all_analog_visibility(True)

    def deselect_all_analog(self):
        """Deselect all Analog channels"""
        self.set_all_analog_visibility(False)

    def set_all_eeg_visibility(self, visible: bool):
        """Set visibility for all EEG channels"""
        for i in range(self.eeg_list.count()):
            item = self.eeg_list.item(i)
            widget = self.eeg_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(visible)
        # Update session manager
        visible_channel_indexes = self.get_current_visible_channel_indexes()
        self._session_manager.set_visible_channel_indexes(visible_channel_indexes)

    def set_all_analog_visibility(self, visible: bool):
        """Set visibility for all Analog channels"""
        for i in range(self.analog_list.count()):
            item = self.analog_list.item(i)
            widget = self.analog_list.itemWidget(item)
            if widget:
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(visible)
        # Update session manager
        visible_channel_indexes = self.get_current_visible_channel_indexes()
        self._session_manager.set_visible_channel_indexes(visible_channel_indexes)
