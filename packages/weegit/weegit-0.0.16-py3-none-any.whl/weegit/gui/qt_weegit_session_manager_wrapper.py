from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Optional, Dict
from pathlib import Path

from weegit.core.conversions.filters import BaseFilter
from weegit.core.conversions.transformations import BaseTransformation
from weegit.core.header import Header
from weegit.core.weegit_session import (
    WeegitSessionManager,
    GuiSetup,
    RightPanelWidgetEnum,
    UserSession,
    Event,
)

def user_session_modification(func):
    def wrapper(self, *args, **kwargs):
        if self._session_manager.current_user_session:
            self._session_manager.current_user_session.changes_saved = False
            return func(self, *args, **kwargs)
        else:
            return None

    return wrapper


class QtWeegitSessionManagerWrapper(QObject):
    # undo_stack: List[BaseCommand] = Field(default_factory=list)
    # redo_stack: List[BaseCommand] = Field(default_factory=list)

    # Signals for RightPanelWidgetEnum list
    right_panel_widgets_changed = pyqtSignal(list)

    # Signals for filter and transformation lists
    filters_changed = pyqtSignal(list)
    transformations_changed = pyqtSignal(list)

    # Signals for boolean flags
    analogue_panel_is_shown_changed = pyqtSignal(bool)
    traces_are_shown_changed = pyqtSignal(bool)
    csd_is_shown_changed = pyqtSignal(bool)

    # Signals for numerical parameters
    start_point_changed = pyqtSignal(int)
    duration_ms_changed = pyqtSignal(int)
    time_step_ms_changed = pyqtSignal(int)
    number_of_dots_to_display_changed = pyqtSignal(int)
    scale_changed = pyqtSignal(float)
    number_of_channels_to_show_changed = pyqtSignal(int)
    current_sweep_idx_changed = pyqtSignal(int)

    # Signals for strings
    experiment_description_changed = pyqtSignal(str)

    # Signals for channel index lists
    eeg_channel_indexes_changed = pyqtSignal(list)
    analogue_input_channel_indexes_changed = pyqtSignal(list)
    visible_channel_indexes_changed = pyqtSignal(list)

    # Session management signals
    session_saved = pyqtSignal()
    session_loaded = pyqtSignal()

    # Event signals
    events_vocabulary_changed = pyqtSignal(dict)
    events_changed = pyqtSignal(list)

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
        if self._session_manager.current_user_session:
            return self._session_manager.current_user_session.gui_setup
        return None

    @property
    def current_user_session(self) -> Optional[GuiSetup]:
        return self._session_manager.current_user_session

    @property
    def events_vocabulary(self) -> Dict[int, str]:
        if self._session_manager.current_user_session:
            return self._session_manager.current_user_session.events_vocabulary

        return {}

    @property
    def events(self) -> List[Event]:
        if self._session_manager.current_user_session:
            return self._session_manager.current_user_session.events

        return []

    @property
    def eeg_channel_indexes(self) -> List[int]:
        if (self._session_manager.current_user_session
                and self._session_manager.current_user_session.eeg_channel_indexes):
            return self._session_manager.current_user_session.eeg_channel_indexes

        return list(range(self.header.number_of_channels))

    @user_session_modification
    def set_right_panel_widgets(self, widgets: List[RightPanelWidgetEnum]):
        self._session_manager.current_user_session.gui_setup.right_panel_widgets = widgets
        self.right_panel_widgets_changed.emit(widgets)

    @user_session_modification
    def set_filters(self, filters: List[BaseFilter]):
        self._session_manager.current_user_session.gui_setup.filters = filters
        self.filters_changed.emit(filters)

    @user_session_modification
    def set_transformations(self, transformations: List[BaseTransformation]):
        self._session_manager.current_user_session.gui_setup.transformations = transformations
        self.transformations_changed.emit(transformations)

    @user_session_modification
    def set_analogue_panel_shown(self, shown: bool):
        self._session_manager.current_user_session.gui_setup.analogue_panel_is_shown = shown
        self.analogue_panel_is_shown_changed.emit(shown)

    @user_session_modification
    def set_traces_shown(self, shown: bool):
        self._session_manager.current_user_session.gui_setup.traces_are_shown = shown
        self.traces_are_shown_changed.emit(shown)

    @user_session_modification
    def set_csd_shown(self, shown: bool):
        self._session_manager.current_user_session.gui_setup.csd_is_shown = shown
        self.csd_is_shown_changed.emit(shown)

    @user_session_modification
    def set_start_point(self, start_point: int):
        # fixme: use duration to shift
        start_point = min(start_point, self.header.number_of_points_per_sweep)
        start_point = max(0, start_point)
        self._session_manager.current_user_session.gui_setup.start_point = start_point
        self.start_point_changed.emit(start_point)

    @user_session_modification
    def set_duration_ms(self, duration_ms: int):
        duration_ms = int(min(duration_ms, self._sweep_duration_ms))
        duration_ms = max(1, duration_ms)
        self._session_manager.current_user_session.gui_setup.duration_ms = duration_ms
        self.duration_ms_changed.emit(duration_ms)

    @user_session_modification
    def set_time_step_ms(self, time_step_ms: int):
        self._session_manager.current_user_session.gui_setup.time_step_ms = time_step_ms
        self.time_step_ms_changed.emit(time_step_ms)

    @user_session_modification
    def set_number_of_dots_to_display(self, number_of_dots_to_display: int):
        self._session_manager.current_user_session.gui_setup.number_of_dots_to_display = number_of_dots_to_display
        self.number_of_dots_to_display_changed.emit(number_of_dots_to_display)

    @user_session_modification
    def set_scale(self, scale: float):
        self._session_manager.current_user_session.gui_setup.scale = scale
        self.scale_changed.emit(scale)

    @user_session_modification
    def set_number_of_channels_to_show(self, count: int):
        self._session_manager.current_user_session.gui_setup.number_of_channels_to_show = count
        self.number_of_channels_to_show_changed.emit(count)

    @user_session_modification
    def set_current_sweep_idx(self, sweep_idx: int):
        self._session_manager.current_user_session.gui_setup.current_sweep_idx = sweep_idx
        self.current_sweep_idx_changed.emit(sweep_idx)

    @user_session_modification
    def set_visible_channel_indexes(self, indexes: List[int]):
        self._session_manager.current_user_session.gui_setup.visible_channel_indexes = indexes
        self.visible_channel_indexes_changed.emit(indexes)

    @user_session_modification
    def set_eeg_channel_indexes(self, indexes: List[int]):
        self._session_manager.current_user_session.eeg_channel_indexes = indexes
        self.eeg_channel_indexes_changed.emit(indexes)

    @user_session_modification
    def set_analogue_input_channel_indexes(self, indexes: List[int]):
        self._session_manager.current_user_session.analogue_input_channel_indexes = indexes
        self.analogue_input_channel_indexes_changed.emit(indexes)

    @user_session_modification
    def set_experiment_description(self, experiment_description: str):
        self._session_manager.current_user_session.experiment_description = experiment_description
        self.experiment_description_changed.emit(experiment_description)

    @user_session_modification
    def add_event_vocabulary(self, name: Optional[str] = None) -> int:
        added_id = self._session_manager.current_user_session.add_event_vocabulary(name)
        self.events_vocabulary_changed.emit(self.events_vocabulary)
        return added_id

    @user_session_modification
    def set_event_vocabulary_name(self, event_vocabulary_id: int, name: str):
        self._session_manager.current_user_session.rename_event_vocabulary(event_vocabulary_id, name)
        self.events_vocabulary_changed.emit(self.events_vocabulary)

    @user_session_modification
    def remove_event_vocabulary(self, event_vocabulary_id: int):
        self._session_manager.current_user_session.remove_event_vocabulary(event_vocabulary_id)
        self.events_vocabulary_changed.emit(self.events_vocabulary)
        self.events_changed.emit(self.events)

    # ---- Events helpers ----
    @user_session_modification
    def add_event(self, event_name_id: int, sweep_idx: int, time_ms: float):
        """Create a new event in the current user session."""
        self._session_manager.current_user_session.add_event(event_name_id, sweep_idx, time_ms)
        self.events_changed.emit(self.events)

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
