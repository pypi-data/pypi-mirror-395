from __future__ import annotations

import os
import shutil
import subprocess
from copy import copy
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Optional, List, Dict
from enum import Enum

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QGuiApplication
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QSplitter,
    QFileDialog,
    QApplication, QStatusBar, QSizePolicy, QMessageBox, QProgressDialog,
    QFrame, QScrollArea, QSpinBox, QDoubleSpinBox, QPushButton, QStyle,
)

from weegit.gui.mixins.qwidget_mixin import QWidgetMixin
from weegit.gui.panels.analogue_signal_panel import AnalogueSignalPanel
from weegit.core.weegit_session import WeegitSessionManager, RightPanelWidgetEnum, UserSession
from weegit.core.global_storage import GlobalStorageManager
from weegit.converter.weegit_io import WeegitIO
from weegit.gui.dialogs.session_name_dialog import SessionNameDialog
from weegit.gui.dialogs.select_session_dialog import SelectSessionDialog
from weegit.gui.dialogs.events_vocabulary_dialog import EventsVocabularyDialog
from weegit.gui.panels.information_panel import InformationPanel
from weegit.gui.panels.logs_panel import LogsPanel
from weegit.gui.panels.eeg_settings_panel import EegSettingsPanel
from weegit.gui.panels.eeg_signal_panel import EegSignalPanel
from weegit.gui.qt_weegit_session_manager_wrapper import QtWeegitSessionManagerWrapper
from weegit.logger import weegit_logger


class EventCommandTypeEnum(Enum):
    ADD = "add"
    TOGGLE_BAD = "toggle_bad"
    REMOVE = "remove"


class MainWindow(QMainWindow, QWidgetMixin):
    """Main window for EEG analysis application.

    - Resizable window with initial size 800x600.
    - Menu bar with File, View, Filters.
    - Header with filename label and four action buttons.
    - Vertical splitter with main EEG panel and optional Analogue panel.
    - Right panel for additional widgets like Logs and Information.
    """

    def __init__(self, session_manager: QtWeegitSessionManagerWrapper, global_storage_manager: GlobalStorageManager):
        super().__init__()
        self.setWindowTitle("Weegit")
        self.setMinimumSize(800, 600)

        # Get the primary screen object
        screen = QGuiApplication.primaryScreen()
        # Get the available geometry (excluding taskbars, etc.)
        available_geometry = screen.availableGeometry()
        self.resize(available_geometry.width(), available_geometry.height())

        self.session_manager: QtWeegitSessionManagerWrapper = session_manager
        self.global_storage_manager = global_storage_manager
        self._processed_channels_data_cache: Dict[int, np.ndarray[np.float64]] = {}

        # Menu bar and actions
        self.setup_ui()
        self.build_menus()
        self.connect_signals()

    def setup_ui(self):
        # Track widgets in right panel
        self.right_panel_widgets: List[RightPanelWidgetEnum] = []
        self.logs_panel = LogsPanel()
        self.info_panel = InformationPanel(self.session_manager)
        self.eeg_settings_panel = EegSettingsPanel(self.session_manager)

        # Central contents
        central = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(8)
        central.setLayout(central_layout)
        self.setCentralWidget(central)

        # Header bar
        header = QWidget(self)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 8, 8, 0)
        header_layout.setSpacing(8)
        header.setLayout(header_layout)

        self.status_label = QLabel("")
        self.current_session_label = QLabel("No session loaded", header)
        self.current_session_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.sweep_spinbox = QSpinBox()
        self.sweep_spinbox.setRange(1, 1)
        self.sweep_spinbox.setSuffix(" sweep")
        self.sweep_spinbox.setSingleStep(1)

        self.btn_plus = QToolButton(header)
        self.btn_plus.setText("+")
        self.btn_plus.setToolTip("Zoom in / Increase scale")

        self.btn_minus = QToolButton(header)
        self.btn_minus.setText("-")
        self.btn_minus.setToolTip("Zoom out / Decrease scale")

        self.btn_right_panel_toggle = QToolButton(header)
        # self.btn_right_panel_toggle.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton))
        self.btn_right_panel_toggle.setText("Panel")
        self.btn_minus.setToolTip("Toggle right panel")

        self.btn_question = QToolButton(header)
        self.btn_question.setText("?")
        self.btn_question.setToolTip("Help / About")

        header_layout.addWidget(self.sweep_spinbox)
        header_layout.addWidget(self.btn_plus)
        header_layout.addWidget(self.btn_minus)
        header_layout.addWidget(self.btn_right_panel_toggle)
        header_layout.addWidget(self.btn_question)
        header_layout.addWidget(self.current_session_label, 1)

        # Ensure header does not expand vertically
        header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        header.setMaximumHeight(header.sizeHint().height())

        # Main horizontal splitter for left content and right panel
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Left side: existing vertical splitter with EEG and analogue panels
        self.vertical_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.eeg_panel = EegSignalPanel(self.session_manager, self)
        self.analogue_panel = AnalogueSignalPanel(self)
        self.vertical_splitter.addWidget(self.eeg_panel)
        self.vertical_splitter.setChildrenCollapsible(False)
        self.vertical_splitter.setStretchFactor(0, 6)
        self.vertical_splitter.setStretchFactor(1, 1)
        self.vertical_splitter.setStretchFactor(2, 3)

        # Start with only EEG panel present; analogue panel will be added on demand
        self.analogue_panel.setVisible(False)
        if self.vertical_splitter.indexOf(self.analogue_panel) != -1:
            self.analogue_panel.setParent(None)

        # Right panel - now with scroll area
        self.right_panel_scroll = QScrollArea(self)
        self.right_panel_scroll.setVisible(False)
        self.right_panel_scroll.setWidgetResizable(True)
        self.right_panel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.right_panel_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create the container widget for the scroll area
        self.right_panel_container = QWidget()
        self.right_panel_layout = QVBoxLayout(self.right_panel_container)
        self.right_panel_layout.setContentsMargins(5, 5, 5, 5)
        self.right_panel_layout.setSpacing(8)

        # Add a stretch to push widgets to the top when there's empty space
        self.right_panel_layout.addStretch(1)

        # Set the container as the scroll area's widget
        self.right_panel_scroll.setWidget(self.right_panel_container)

        # Style the scroll area frame
        self.right_panel_scroll.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_panel_scroll.setStyleSheet("QFrame { border-left: 1px solid gray; }")

        # Add both to main splitter
        self.main_splitter.addWidget(self.vertical_splitter)
        self.main_splitter.addWidget(self.right_panel_scroll)

        # Set initial sizes: 80% for main content, 20% for right panel
        self.main_splitter.setSizes([800, 200])
        self.main_splitter.setStretchFactor(0, 4)  # Main content gets 4/5 of space
        self.main_splitter.setStretchFactor(1, 1)  # Right panel gets 1/5 of space

        # Assemble central layout
        central_layout.addWidget(header)
        central_layout.addWidget(self.main_splitter, 1)

        # Status bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.addWidget(self.status_label)

    def build_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        self.act_open = QAction("Open", self)
        file_menu.addAction(self.act_open)

        self.menu_open_recent = file_menu.addMenu("Open Recent")
        self.__update_recent_dirs()

        file_menu.addSection("Session")
        self.act_save_session = QAction("Save", self)
        self.act_save_session.setShortcut("Ctrl+S")
        file_menu.addAction(self.act_save_session)
        self.act_import_session = QAction("Import", self)
        file_menu.addAction(self.act_import_session)
        self.act_export_session = QAction("Export", self)
        file_menu.addAction(self.act_export_session)
        self.act_open_session_in_explorer = QAction("Open in Explorer", self)
        file_menu.addAction(self.act_open_session_in_explorer)
        self.menu_sessions = file_menu.addMenu("Other Sessions")

        file_menu.addSeparator()
        self.act_exit = QAction("Exit", self)
        file_menu.addAction(self.act_exit)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        self.undo_action = QAction("Undo", self)
        self.redo_action = QAction("Redo", self)
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        # View menu (checkable)
        view_menu = menubar.addMenu("View")
        view_menu.addSection("EEG")
        self.view_traces = QAction("Traces", self, checkable=True, checked=True)
        self.view_spikes = QAction("Spikes", self, checkable=True, checked=False)
        self.view_events = QAction("Events", self, checkable=True, checked=False)
        self.view_analog = QAction("Analog input", self, checkable=True, checked=False)
        self.view_csd = QAction("CSD", self, checkable=True, checked=False)
        self.view_spike_density = QAction("Spike density", self, checkable=True, checked=False)
        for action in (
                self.view_traces,
                self.view_spikes,
                self.view_events,
                self.view_analog,
                self.view_csd,
                self.view_spike_density,
        ):
            view_menu.addAction(action)

        view_menu.addSection("Tools")
        self.view_eeg_settings_panel = QAction("EEG Settings", self, checkable=True, checked=False)
        self.view_info_panel = QAction("Information", self, checkable=True, checked=False)
        self.view_logs_panel = QAction("Logs", self, checkable=True, checked=False)
        for action in (
                self.view_eeg_settings_panel,
                self.view_info_panel,
                self.view_logs_panel,
        ):
            view_menu.addAction(action)

        # Filters menu (checkable)
        filters_menu = menubar.addMenu("Filters")
        self.filter_highpass = QAction("Highpass", self, checkable=True)
        self.filter_lowpass = QAction("Lowpass", self, checkable=True)
        self.filter_bandpass = QAction("Bandpass", self, checkable=True)

        filters_menu.addAction(self.filter_highpass)
        filters_menu.addAction(self.filter_lowpass)
        filters_menu.addAction(self.filter_bandpass)

        # Events menu
        events_menu = menubar.addMenu("Events")
        self.events_show_all_action = QAction("Show table", self)
        self.events_add_action = QAction("Add", self)
        self.events_set_bad_event_action = QAction("Set bad event", self)
        self.events_unset_bad_event_action = QAction("Unset bad event", self)
        self.events_remove_action = QAction("Remove", self)
        events_menu.addAction(self.events_show_all_action)
        events_menu.addAction(self.events_add_action)
        events_menu.addAction(self.events_set_bad_event_action)
        events_menu.addAction(self.events_unset_bad_event_action)
        events_menu.addAction(self.events_remove_action)

    def connect_signals(self):
        # Buttons
        self.sweep_spinbox.valueChanged.connect(self.on_cur_sweep_idx_changed)
        self.btn_plus.clicked.connect(self.on_plus_clicked)
        self.btn_minus.clicked.connect(self.on_minus_clicked)
        self.btn_right_panel_toggle.clicked.connect(self.toggle_right_panel)
        self.btn_question.clicked.connect(self.on_question_clicked)

        # Menus
        self.act_open.triggered.connect(self.on_open)
        self.act_save_session.triggered.connect(self.on_save_session)
        self.act_import_session.triggered.connect(self.on_import_session)
        self.act_export_session.triggered.connect(self.on_export_session)
        self.act_open_session_in_explorer.triggered.connect(self.on_open_session_in_explorer)
        self.act_exit.triggered.connect(self.on_exit)
        self.undo_action.triggered.connect(self.on_undo)
        self.redo_action.triggered.connect(self.on_redo)
        self.view_traces.triggered.connect(self.on_view_traces)
        self.view_spikes.triggered.connect(self.on_view_spikes)
        self.view_events.triggered.connect(self.on_view_events)
        self.view_analog.triggered.connect(self.on_view_analog)
        self.view_csd.triggered.connect(self.on_view_csd)
        self.view_spike_density.triggered.connect(self.on_view_spike_density)
        self.view_eeg_settings_panel.triggered.connect(self.on_view_eeg_settings_panel)
        self.view_info_panel.triggered.connect(self.on_view_info_panel)
        self.view_logs_panel.triggered.connect(self.on_view_logs_panel)
        self.filter_highpass.triggered.connect(self.on_filter_highpass)
        self.filter_lowpass.triggered.connect(self.on_filter_lowpass)
        self.filter_bandpass.triggered.connect(self.on_filter_bandpass)
        self.events_show_all_action.triggered.connect(self.on_show_events)
        self.events_add_action.triggered.connect(self.on_add_event)
        self.events_set_bad_event_action.triggered.connect(self.on_set_bad_event)
        self.events_unset_bad_event_action.triggered.connect(self.on_unset_bad_event)
        self.events_remove_action.triggered.connect(self.on_remove_event)

        # Different signal params changed
        self.session_manager.number_of_dots_to_display_changed.connect(self.on_number_of_dots_to_display_changed)
        self.session_manager.number_of_channels_to_show_changed.connect(self.on_number_of_channels_to_show_changed)
        self.session_manager.scale_changed.connect(self.on_scale_changed)
        self.session_manager.visible_channel_indexes_changed.connect(self.on_visible_channel_indexes_changed)
        self.session_manager.eeg_channel_indexes_changed.connect(self.on_visible_channel_indexes_changed)
        self.session_manager.analogue_input_channel_indexes_changed.connect(self.on_visible_channel_indexes_changed)
        self.session_manager.start_point_changed.connect(self.on_time_window_changed)
        self.session_manager.duration_ms_changed.connect(self.on_time_window_changed)
        self.session_manager.traces_are_shown_changed.connect(self.on_view_categories_changed)
        self.session_manager.csd_is_shown_changed.connect(self.on_view_categories_changed)

        # Events changed
        self.session_manager.events_changed.connect(self.on_events_changed)

        # From panels
        self.eeg_panel.channel_scroll_changed.connect(self.on_visible_channel_indexes_changed)

        # todo: Events
        # 2.1. If event view draw them.
        # ...

        # todo: View changed
        # On change visibility from View tab: only draw necessary

    # ---------- Callbacks session manager ----------
    def on_number_of_channels_to_show_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def on_number_of_dots_to_display_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def on_scale_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=False, )

    def on_visible_channel_indexes_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def on_view_categories_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=False, )

    def on_time_window_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def on_sweep_idx_changed(self):
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def __recalculate_and_redraw_necessary_signals(self, recalculate_data: bool = True, ):
        channel_indexes = (self.eeg_panel.get_visible_channel_indexes()
                           + self.analogue_panel.get_visible_channel_indexes())
        if recalculate_data:
            self._processed_channels_data_cache = self.session_manager.experiment_data.process_data_pipeline(
                params=self.session_manager.gui_setup,
                sweep_idx=self.session_manager.gui_setup.current_sweep_idx,
                channel_indexes=channel_indexes,
                output_number_of_dots=self.session_manager.gui_setup.number_of_dots_to_display,
            )

        self.eeg_panel.reset_data_and_redraw(self._processed_channels_data_cache)

    # ---------- Right Panel Management ----------
    def toggle_right_panel(self):
        """Toggle the visibility of the right panel"""
        is_visible = self.right_panel_scroll.isVisible()
        self.right_panel_scroll.setVisible(not is_visible)

        # Adjust splitter sizes based on visibility
        if not is_visible:
            # Show right panel - set to 20% width
            total_width = self.main_splitter.width()
            main_width = int(total_width * 0.8)
            panel_width = int(total_width * 0.2)
            self.main_splitter.setSizes([main_width, panel_width])
        else:
            # Hide right panel - give all space to main content
            total_width = self.main_splitter.width()
            self.main_splitter.setSizes([total_width, 0])

    def add_widget_to_right_panel(self, widget_type: RightPanelWidgetEnum, update_session: bool = True):
        widget = self.__get_panel_by_type(widget_type)
        self.remove_widget_from_right_panel(widget_type)
        self.right_panel_layout.insertWidget(self.right_panel_layout.count() - 1, widget)
        self.right_panel_widgets.append(widget_type)
        self.__set_panel_checked_by_type(widget_type, checked=True)

        if not self.right_panel_scroll.isVisible():
            self.toggle_right_panel()

        if update_session:
            self.session_manager.set_right_panel_widgets(self.right_panel_widgets)

    def remove_widget_from_right_panel(self, widget_type: RightPanelWidgetEnum, update_session: bool = True):
        """Remove a widget from the right panel"""
        if widget_type in self.right_panel_widgets:
            widget = self.__get_panel_by_type(widget_type)
            self.right_panel_layout.removeWidget(widget)
            widget.setParent(None)
            self.right_panel_widgets.remove(widget_type)
            self.__set_panel_checked_by_type(widget_type, checked=False)

        if not self.right_panel_widgets and self.right_panel_scroll.isVisible():
            self.toggle_right_panel()

        if update_session:
            self.session_manager.set_right_panel_widgets(self.right_panel_widgets)

    # ---------- Callbacks menu ----------
    def on_open(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select a directory", "",
            options=QFileDialog.Option.ShowDirsOnly)

        if dir_path:
            experiment_path = Path(dir_path)
            # fixme: we assume for now that only one folder will be created
            is_weegit, weegit_experiment_folder_path = WeegitIO.weegit_dir_of_experiment(experiment_path)
            if not is_weegit and not WeegitIO.is_valid_weegit_folder(weegit_experiment_folder_path):
                reply = QMessageBox.question(
                    self,
                    "Confirmation",
                    f"Weegit is going to create folder {weegit_experiment_folder_path} with the required files. "
                    f"Do you want to proceed?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No  # Default button
                )

                if reply == QMessageBox.StandardButton.Yes:
                    progress = QProgressDialog("Converting to weegit data...", "Cancel", 0, 100, self)
                    progress.setWindowModality(Qt.WindowModality.WindowModal)  # Block the entire app
                    progress.setWindowTitle("Please Wait")
                    progress.show()
                    for convertion_progress_percents in WeegitIO.convert_from_source_to_weegit(
                            experiment_path, weegit_experiment_folder_path):
                        if progress.wasCanceled():
                            shutil.rmtree(weegit_experiment_folder_path)
                            return

                        progress.setValue(convertion_progress_percents)

            self.__load_session(weegit_experiment_folder_path)

    def on_open_recent_experiment(self, experiment_path: Path):
        try:
            self.__load_session(experiment_path)
        except FileNotFoundError:
            self.global_storage_manager.update_recent_experiments_list(experiment_path, to_delete=True)
            self.__update_recent_dirs()
            self.__set_status("Recent experiment folder does not exist")

    def on_open_another_session(self, session_filename: str):
        try:
            self.__switch_to_session(session_filename)
        except Exception as e:
            self.__set_status(repr(e))
        else:
            self.__set_status("Session was switched to " + self.session_manager.user_session.session_filename)

    def on_save_session(self):
        if self.session_manager.session_is_active:
            self.session_manager.save_user_session()
            self.__set_status("Session was saved successfully")

    def on_import_session(self):
        if self.session_manager.session_is_active:
            file_to_import, _ = QFileDialog.getOpenFileName(self, "Select a session file")

            if file_to_import:
                session_to_import = WeegitSessionManager.parse_session_file(Path(file_to_import))
                if session_to_import is not None:
                    while self.session_manager.session_filename_already_exists(session_to_import.session_filename):
                        new_session_name = self.__new_unique_session_name()
                        if new_session_name is None:
                            return

                        session_to_import.change_name(new_session_name)

                    self.session_manager.import_new_session(session_to_import)
                    self.__update_sessions()
                    self.__set_status("Imported successfully as " + session_to_import.session_filename)
                else:
                    self.__set_status("Corrupted session file")
        else:
            self.__set_status("Warning: there is no active weegit folder to import to")

    def on_export_session(self):
        destination_dir = QFileDialog.getExistingDirectory(
            self, "Select a destination directory", "",
            options=QFileDialog.Option.ShowDirsOnly)

        if destination_dir:
            destination_path = Path(destination_dir)
            export_name = self.session_manager.export_current_session(destination_path)
            self.__set_status("Session was exported successfully to \"" + export_name + "\"")

    def on_open_session_in_explorer(self):
        if self.session_manager.session_is_active:
            if os.name == 'nt':  # Windows
                subprocess.run(['explorer', self.session_manager.weegit_experiment_folder])
            elif os.name == 'posix':  # macOS or Linux
                subprocess.run(['open', self.session_manager.weegit_experiment_folder])  # For macOS
                # For Linux, you might need 'xdg-open' or a specific file manager command
                # subprocess.run(['xdg-open', folder_path])
        else:
            self.__set_status("Warning: weegit session is not active")

    def closeEvent(self, event):
        if (self.session_manager.session_is_active
                and self.session_manager.user_session
                and not self.session_manager.user_session.changes_saved):
            result = QMessageBox.warning(
                self,
                "Session not saved",
                "Some changes in the session was not saved. Are you sure you want to exit?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if result == QMessageBox.StandardButton.Cancel:
                event.ignore()
            else:
                event.accept()

    def on_exit(self):
        if (self.session_manager.session_is_active
                and self.session_manager.user_session
                and not self.session_manager.user_session.changes_saved):
            result = QMessageBox.warning(
                self,
                "Session not saved",
                "Some changes in the session was not saved. Are you sure you want to exit?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if result == QMessageBox.StandardButton.Cancel:
                return

        QApplication.instance().quit()

    def on_undo(self):
        pass

    def on_redo(self):
        pass

    def on_view_traces(self, checked: bool, *args, **kwargs):
        if self.session_manager.session_is_active:
            self.session_manager.set_traces_shown(checked)

    def on_view_spikes(self, checked: bool, *args, **kwargs):
        pass

    def on_view_events(self, checked: bool, *args, **kwargs):
        pass

    def on_view_analog(self, checked: bool, *args, **kwargs):
        if self.session_manager.session_is_active:
            self.session_manager.set_analogue_panel_shown(checked)

        # Toggle analogue panel visibility
        self.analogue_panel.setVisible(checked)
        if checked:
            if self.vertical_splitter.indexOf(self.analogue_panel) == -1:
                self.vertical_splitter.addWidget(self.analogue_panel)
            # Allocate approximately 3/4 to EEG and 1/4 to analogue
            total = max(4, sum(max(1, s) for s in self.vertical_splitter.sizes()))
            self.vertical_splitter.setSizes([int(total * 0.75), int(total * 0.25)])
        else:
            if self.vertical_splitter.indexOf(self.analogue_panel) != -1:
                self.analogue_panel.setParent(None)
            # Ensure EEG takes all space after removal
            self.vertical_splitter.setSizes([1])

    def on_view_csd(self, checked: bool, *args, **kwargs):
        if self.session_manager.session_is_active:
            self.session_manager.set_csd_shown(checked)

    def on_view_spike_density(self, checked: bool, *args, **kwargs):
        pass

    def on_view_eeg_settings_panel(self, checked: bool, *args, **kwargs):
        if checked:
            self.add_widget_to_right_panel(RightPanelWidgetEnum.EEG_SETTINGS)
        else:
            self.remove_widget_from_right_panel(RightPanelWidgetEnum.EEG_SETTINGS)

    def on_view_info_panel(self, checked: bool, *args, **kwargs):
        if checked:
            self.add_widget_to_right_panel(RightPanelWidgetEnum.INFORMATION)
        else:
            self.remove_widget_from_right_panel(RightPanelWidgetEnum.INFORMATION)

    def on_view_logs_panel(self, checked: bool, *args, **kwargs):
        if checked:
            self.add_widget_to_right_panel(RightPanelWidgetEnum.LOGS)
        else:
            self.remove_widget_from_right_panel(RightPanelWidgetEnum.LOGS)

    def on_filter_highpass(self, checked: bool, *args, **kwargs):
        pass

    def on_filter_lowpass(self, checked: bool, *args, **kwargs):
        pass

    def on_filter_bandpass(self, checked: bool, *args, **kwargs):
        pass

    def on_events_changed(self, *args, **kwargs):
        """Redraw EEG panel when events list changes."""
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=False)

    def on_show_events(self):
        if not self.session_manager.session_is_active:
            self.__set_status("Warning: weegit session is not active")
            return

        EventsVocabularyDialog(self.session_manager, self).exec()

    def on_add_event(self):
        if not self.session_manager.session_is_active:
            self.__set_status("Warning: weegit session is not active")
            return

        dialog = EventsVocabularyDialog(self.session_manager, self)
        if dialog.exec():
            selected_id = dialog.get_selected_event_vocabulary_id()
            if selected_id is None:
                return

            # Enter interactive event placement mode on EEG panel
            self.eeg_panel.start_event_add_mode(selected_id)

    def on_set_bad_event(self):
        pass

    def on_unset_bad_event(self):
        pass

    def on_remove_event(self):
        pass

    def on_cur_sweep_idx_changed(self, value):
        value_idx = value - 1
        self.session_manager.set_current_sweep_idx(value_idx)

    def on_plus_clicked(self, *args, **kwargs):
        weegit_logger().info("Plus clicked")

    def on_minus_clicked(self, *args, **kwargs):
        weegit_logger().error("Minus clicked")

    def on_question_clicked(self, *args, **kwargs):
        weegit_logger().warning(
            "Question clicked. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

    def on_time_range_changed(self, start_ms: int, duration_ms: int):
        print(f"Time range changed: {start_ms}ms to {start_ms + duration_ms}ms")

    def __load_session(self, weegit_experiment_folder_path: Path):
        self.session_manager.init_from_folder(weegit_experiment_folder_path)
        sessions = self.session_manager.other_session_filenames
        selected_session = None
        if len(sessions) == 1:
            selected_session = sessions[0]
        elif len(sessions) > 1:
            selected_session = SelectSessionDialog(sessions).get_selected_item()

        if selected_session is None:
            selected_session = UserSession.session_name_to_filename(self.__new_unique_session_name())
            self.session_manager.new_user_session(selected_session)

        self.__switch_to_session(selected_session)
        self.global_storage_manager.update_recent_experiments_list(weegit_experiment_folder_path)
        self.__set_status("Session is loaded successfully")

    def __switch_to_session(self, selected_session):
        self.session_manager.switch_sessions(selected_session)
        if self.session_manager.user_session.gui_setup.right_panel_widgets:
            for cur_right_panel_widget in copy(self.right_panel_widgets):
                self.remove_widget_from_right_panel(cur_right_panel_widget, update_session=False)
            for right_panel_widget in self.session_manager.user_session.gui_setup.right_panel_widgets:
                self.add_widget_to_right_panel(right_panel_widget, update_session=False)

        self.__update_recent_dirs()
        self.__update_sessions()
        self.__update_menu()
        self.__redraw_header()
        self.__recalculate_and_redraw_necessary_signals(recalculate_data=True, )

    def __update_recent_dirs(self):
        self.menu_open_recent.clear()
        for recent in self.global_storage_manager.recent_experiments:
            act_open_recent = QAction(str(recent), self)
            act_open_recent.triggered.connect(partial(self.on_open_recent_experiment, recent))
            self.menu_open_recent.addAction(act_open_recent)

    def __update_sessions(self):
        self.menu_sessions.clear()
        for session_filename in self.session_manager.other_session_filenames:
            act_open_session = QAction(session_filename, self)
            act_open_session.triggered.connect(partial(self.on_open_another_session, session_filename))
            self.menu_sessions.addAction(act_open_session)

    def __update_menu(self):
        self.view_analog.setChecked(self.session_manager.gui_setup.analogue_panel_is_shown)
        self.view_traces.setChecked(self.session_manager.gui_setup.traces_are_shown)
        self.view_csd.setChecked(self.session_manager.gui_setup.csd_is_shown)

    def __redraw_header(self):
        session_filename = self.session_manager.weegit_experiment_folder.name
        if self.session_manager.user_session is not None:
            session_filename += ":" + self.session_manager.user_session.session_filename
        self.current_session_label.setText(session_filename)

        self.sweep_spinbox.setRange(1, self.session_manager.experiment_data.header.number_of_sweeps)
        self.sweep_spinbox.setValue(self.session_manager.user_session.gui_setup.current_sweep_idx)

    def __set_status(self, text: str):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        self.status_label.setText(f"{formatted_time} " + text)
        weegit_logger().info(text)

    def __new_unique_session_name(self) -> Optional[str]:
        is_created = False
        while not is_created:
            dialog = SessionNameDialog(self)
            if dialog.exec():
                session_name = dialog.line_edit.text()
                if self.session_manager.session_name_already_exists(session_name):
                    QMessageBox.warning(self, "Warning",
                                        f"Session with the name {session_name} already exists.")
                else:
                    return session_name
            else:
                return None

    def __get_panel_by_type(self, widget_type: RightPanelWidgetEnum):
        if widget_type == RightPanelWidgetEnum.EEG_SETTINGS:
            return self.eeg_settings_panel
        elif widget_type == RightPanelWidgetEnum.LOGS:
            return self.logs_panel
        elif widget_type == RightPanelWidgetEnum.INFORMATION:
            return self.info_panel
        else:
            raise ValueError("Unknown widget_type")

    def __set_panel_checked_by_type(self, widget_type: RightPanelWidgetEnum, checked: bool):
        if widget_type == RightPanelWidgetEnum.EEG_SETTINGS:
            self.view_eeg_settings_panel.setChecked(checked)
        elif widget_type == RightPanelWidgetEnum.LOGS:
            self.view_logs_panel.setChecked(checked)
        elif widget_type == RightPanelWidgetEnum.INFORMATION:
            self.view_info_panel.setChecked(checked)
        else:
            raise ValueError("Unknown widget_type")
