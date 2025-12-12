from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Optional
from pathlib import Path

from weegit.core.conversions.filters import BaseFilter
from weegit.core.conversions.transformations import BaseTransformation
from weegit.core.header import Header
from weegit.core.weegit_session import WeegitSessionManager, GuiSetup, RightPanelWidgetEnum


class QtWeegitSessionManagerWrapper(QObject):
    # Signals for RightPanelWidgetEnum list
    right_panel_widgets_changed = pyqtSignal(list)

    # Signals for filter and transformation lists
    filters_changed = pyqtSignal(list)
    transformations_changed = pyqtSignal(list)

    # Signals for boolean flags
    analogue_panel_is_shown_changed = pyqtSignal(bool)

    # Signals for numerical parameters
    start_point_changed = pyqtSignal(int)
    duration_ms_changed = pyqtSignal(int)
    time_step_ms_changed = pyqtSignal(int)
    number_of_dots_to_display_changed = pyqtSignal(int)
    scale_changed = pyqtSignal(float)
    number_of_channels_to_show_changed = pyqtSignal(int)

    # Signals for channel index lists
    eeg_channel_indexes_changed = pyqtSignal(list)
    analogue_input_channel_indexes_changed = pyqtSignal(list)
    visible_channel_indexes_changed = pyqtSignal(list)

    # Session management signals
    session_saved = pyqtSignal()
    session_loaded = pyqtSignal()

    def __init__(self, session_manager: WeegitSessionManager):
        super().__init__()
        self._session_manager = session_manager

    @property
    def header(self) -> Optional[Header]:
        """Get current GUI setup"""
        if self._session_manager.experiment_data:
            return self._session_manager.experiment_data.header

        return None

    @property
    def gui_setup(self) -> Optional[GuiSetup]:
        """Get current GUI setup"""
        if self._session_manager.current_user_session:
            return self._session_manager.current_user_session.gui_setup
        return None

    @property
    def eeg_channel_indexes(self) -> List[int]:
        if self.gui_setup.eeg_channel_indexes:
            return self.gui_setup.eeg_channel_indexes

        return list(range(self.header.number_of_channels))

    def update_gui_setup(self, **kwargs):
        """Update GUI setup parameters and emit corresponding signals"""
        if not self._session_manager.current_user_session:
            return

        old_setup = self._session_manager.current_user_session.gui_setup.copy()
        self._session_manager.current_user_session.gui_setup = old_setup.copy(update=kwargs)
        self._session_manager.current_user_session.changes_saved = False

        new_setup = self._session_manager.current_user_session.gui_setup

        # Emit signals for changed parameters
        self._emit_changed_signals(old_setup, new_setup)

    def _emit_changed_signals(self, old_setup: GuiSetup, new_setup: GuiSetup):
        """Compare old and new setups and emit signals for changed parameters"""
        # Right panel widgets
        if old_setup.right_panel_widgets != new_setup.right_panel_widgets:
            self.right_panel_widgets_changed.emit(new_setup.right_panel_widgets)

        # Filters and transformations
        if old_setup.filters != new_setup.filters:
            self.filters_changed.emit(new_setup.filters)
        if old_setup.transformations != new_setup.transformations:
            self.transformations_changed.emit(new_setup.transformations)

        # Boolean flags
        if old_setup.analogue_panel_is_shown != new_setup.analogue_panel_is_shown:
            self.analogue_panel_is_shown_changed.emit(new_setup.analogue_panel_is_shown)

        # Numerical parameters
        if old_setup.start_point != new_setup.start_point:
            self.start_point_changed.emit(new_setup.start_point)
        if old_setup.duration_ms != new_setup.duration_ms:
            self.duration_ms_changed.emit(new_setup.duration_ms)
        if old_setup.time_step_ms != new_setup.time_step_ms:
            self.time_step_ms_changed.emit(new_setup.time_step_ms)
        if old_setup.number_of_dots_to_display != new_setup.number_of_dots_to_display:
            self.number_of_dots_to_display_changed.emit(new_setup.number_of_dots_to_display)
        if old_setup.scale != new_setup.scale:
            self.scale_changed.emit(new_setup.scale)
        if old_setup.number_of_channels_to_show != new_setup.number_of_channels_to_show:
            self.number_of_channels_to_show_changed.emit(new_setup.number_of_channels_to_show)

        # Channel indexes
        if old_setup.eeg_channel_indexes != new_setup.eeg_channel_indexes:
            self.eeg_channel_indexes_changed.emit(new_setup.eeg_channel_indexes)
        if old_setup.analogue_input_channel_indexes != new_setup.analogue_input_channel_indexes:
            self.analogue_input_channel_indexes_changed.emit(new_setup.analogue_input_channel_indexes)
        if old_setup.visible_channel_indexes != new_setup.visible_channel_indexes:
            self.visible_channel_indexes_changed.emit(new_setup.visible_channel_indexes)

    # Convenience methods for individual parameter updates
    def set_right_panel_widgets(self, widgets: List[RightPanelWidgetEnum]):
        self.update_gui_setup(right_panel_widgets=widgets)

    def set_filters(self, filters: List[BaseFilter]):
        self.update_gui_setup(filters=filters)

    def set_transformations(self, transformations: List[BaseTransformation]):
        self.update_gui_setup(transformations=transformations)

    def set_analogue_panel_shown(self, shown: bool):
        self.update_gui_setup(analogue_panel_is_shown=shown)

    def set_start_point(self, start_point: int):
        # fixme: use duration to shift
        start_point = min(start_point, self.header.number_of_points_per_sweep)
        start_point = max(0, start_point)
        self.update_gui_setup(start_point=start_point)

    def set_duration_ms(self, duration_ms: int):
        duration = int(min(duration_ms, self._sweep_duration_ms))
        self.update_gui_setup(duration_ms=duration)

    def set_time_step_ms(self, time_step_ms: int):
        self.update_gui_setup(time_step_ms=time_step_ms)

    def set_number_of_dots_to_display(self, number_of_dots_to_display: int):
        self.update_gui_setup(number_of_dots_to_display=number_of_dots_to_display)

    def set_scale(self, scale: float):
        self.update_gui_setup(scale=scale)

    def set_number_of_channels_to_show(self, count: int):
        self.update_gui_setup(number_of_channels_to_show=count)

    def set_eeg_channel_indexes(self, indexes: List[int]):
        self.update_gui_setup(eeg_channel_indexes=indexes)

    def set_analogue_input_channel_indexes(self, indexes: List[int]):
        self.update_gui_setup(analogue_input_channel_indexes=indexes)

    def set_visible_channel_indexes(self, indexes: List[int]):
        self.update_gui_setup(visible_channel_indexes=indexes)

    # Session management methods
    def new_user_session(self, session_filename: str):
        self._session_manager.new_user_session(session_filename)
        self.session_loaded.emit()

    def export_current_session(self, destination_path):
        return self._session_manager.export_current_session(destination_path)

    def import_new_session(self, session_to_import):
        self._session_manager.import_new_session(session_to_import)
        self.session_loaded.emit()

    def switch_sessions(self, session_filename: str):
        self._session_manager.switch_sessions(session_filename)
        self.session_loaded.emit()

    def save_user_session(self):
        self._session_manager.save_user_session()
        if self._session_manager.current_user_session:
            self._session_manager.current_user_session.changes_saved = True
        self.session_saved.emit()

    def init_from_folder(self, weegit_experiment_folder: Path):
        self._session_manager.init_from_folder(weegit_experiment_folder)

    def session_name_already_exists(self, session_name: str):
        return self._session_manager.session_name_already_exists(session_name)

    def session_filename_already_exists(self, session_filename: str):
        return self._session_manager.session_filename_already_exists(session_filename)

    # Property forwarding
    @property
    def session_is_active(self):
        return self._session_manager.session_is_active

    @property
    def other_session_filenames(self):
        return self._session_manager.other_session_filenames

    @property
    def user_session(self):
        return self._session_manager.user_session

    @property
    def experiment_data(self):
        return self._session_manager.experiment_data

    @property
    def weegit_experiment_folder(self):
        return self._session_manager.weegit_experiment_folder

    @property
    def _sweep_duration_ms(self):
        return (self.header.sample_interval_microseconds / 10 ** 3) * self.header.number_of_points_per_sweep
