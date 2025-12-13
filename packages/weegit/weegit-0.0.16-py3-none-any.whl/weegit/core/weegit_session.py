import json
import os
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import numpy as np
from pydantic import BaseModel, Field

from weegit import settings
from weegit.core.header import Header
from weegit.core.commands.base_command import BaseCommand
from weegit.core.conversions.transformations import BaseTransformation
from weegit.core.conversions.filters import BaseFilter
from weegit.core.exceptions import BrokenSessionFileError, SessionAlreadyExistsError
from weegit.converter.weegit_io import WeegitIO


class RightPanelWidgetEnum(Enum):
    EEG_SETTINGS = "eeg_settings"
    INFORMATION = "information"
    LOGS = "logs"


class GuiSetup(BaseModel):
    right_panel_widgets: List[RightPanelWidgetEnum] = Field(default_factory=list)
    filters: List[BaseFilter] = Field(default_factory=list)
    transformations: List[BaseTransformation] = Field(default_factory=list)

    analogue_panel_is_shown: bool = False
    traces_are_shown: bool = True
    csd_is_shown: bool = False

    start_point: int = 0
    duration_ms: int = 10000
    time_step_ms: int = 1000
    scale: float = 1.0
    number_of_dots_to_display: int = settings.EEG_DEFAULT_NUMBER_OF_DOTS_TO_DISPLAY
    number_of_channels_to_show: int = settings.MAX_VISIBLE_CHANNELS
    visible_channel_indexes: List[int] = Field(default_factory=list)

    current_sweep_idx: int = 0

    class Config:
        arbitrary_types_allowed = True


class Event(BaseModel):
    event_name_id: int
    sweep_idx: int
    time_ms: float


class UserSession(BaseModel):
    session_filename: str
    changes_saved: bool = True
    experiment_description: str = ""
    eeg_channel_indexes: List[int] = Field(default_factory=list)
    analogue_input_channel_indexes: List[int] = Field(default_factory=list)
    events_vocabulary: Dict[int, str] = Field(default_factory=dict)
    events: List[Event] = Field(default_factory=list)
    gui_setup: GuiSetup = Field(default_factory=GuiSetup)

    class Config:
        arbitrary_types_allowed = True

    def save_session(self, dest_folder: Path):
        dest_folder.mkdir(exist_ok=True)
        dest_filepath = dest_folder / self.session_filename
        json_dump = self.model_dump_json(exclude={"session_filename", "changes_saved"}, indent=4)
        with open(dest_filepath, "w") as dest_file:
            dest_file.write(json_dump)

    def change_name(self, new_session_name: str):
        self.session_filename = new_session_name + settings.SESSION_EXTENSION

    @staticmethod
    def parse_session_file(session_filepath: Path):
        if session_filepath.exists():
            with open(session_filepath, "r") as prev_session_file:
                try:
                    json_string = prev_session_file.read()
                    session_dict = json.loads(json_string)
                    session_dict["session_filename"] = session_filepath.name
                    return UserSession.model_validate(session_dict)
                except Exception:
                    raise BrokenSessionFileError(session_filepath)

        return None

    @staticmethod
    def load_from_default_folder(weegit_experiment_folder, session_filename: str) -> "UserSession":
        session_filepath = UserSession.sessions_folder(weegit_experiment_folder) / session_filename
        return UserSession.parse_session_file(session_filepath)

    @staticmethod
    def session_name_to_filename(session_name: str) -> str:
        return session_name + settings.SESSION_EXTENSION

    @staticmethod
    def is_session_file(filename: str) -> bool:
        return filename.endswith(settings.SESSION_EXTENSION)

    @staticmethod
    def sessions_folder(weegit_experiment_folder: Path):
        folder = weegit_experiment_folder / settings.OTHER_SESSIONS_FOLDER
        folder.mkdir(exist_ok=True)
        return folder

    def add_event_vocabulary(self, name: str) -> int:
        next_id = max(self.events_vocabulary.keys(), default=-1) + 1
        event_name = name.strip() if name else f"Event {next_id}"
        self.events_vocabulary[next_id] = event_name
        return next_id

    def rename_event_vocabulary(self, event_vocabulary_id: int, name: str):
        if event_vocabulary_id not in self.events_vocabulary:
            return

        new_name = name.strip() or self.events_vocabulary[event_vocabulary_id]
        self.events_vocabulary[event_vocabulary_id] = new_name

    def remove_event_vocabulary(self, event_vocabulary_id: int):
        if event_vocabulary_id not in self.events_vocabulary:
            return

        self.events_vocabulary = {key: value for key, value in self.events_vocabulary.items()
                                  if key != event_vocabulary_id}
        self.clear_events_for_vocabulary_id(event_vocabulary_id)

    def add_event(self, event_name_id: int, sweep_idx: int, time_ms: float) -> Event:
        """Add a new event to the session."""
        new_event = Event(event_name_id=event_name_id, sweep_idx=sweep_idx, time_ms=time_ms)
        self.events.append(new_event)
        return new_event

    def remove_event(self, event: Event):
        """Remove a specific event instance from the session."""
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def clear_events_for_vocabulary_id(self, event_name_id: int):
        """Remove all events that reference the given vocabulary id."""
        self.events = [e for e in self.events if e.event_name_id != event_name_id]


class ExperimentData(BaseModel):
    header: Header
    data_memmaps: Tuple[np.memmap, ...]

    class Config:
        arbitrary_types_allowed = True

    def process_data_pipeline(self, params: GuiSetup, sweep_idx: int, channel_indexes: List[int],
                              output_number_of_dots: int) -> Dict[int, np.ndarray[np.float64]]:
        """
        Process data pipeline using multithreading for each visible channel.
        Returns array of shape (len(visible_channel_indexes), number_of_time_points)
        """
        cur_swift_start = self.header.number_of_points_per_sweep * sweep_idx
        cur_swift_end = self.header.number_of_points_per_sweep * (1 + sweep_idx)
        start_sample = params.start_point + cur_swift_start
        end_sample = min(
            start_sample + int(params.duration_ms * 1000 / self.header.sample_interval_microseconds),
            cur_swift_end
        )
        each_point = max(1, int((end_sample - start_sample) / output_number_of_dots))

        # Collect results by waiting for each future to complete
        results = {}
        if channel_indexes:
            # Use ThreadPoolExecutor to process channels in parallel
            with ThreadPoolExecutor(max_workers=len(channel_indexes)) as executor:
                # Submit all tasks and store futures
                future_to_channel = {}
                for channel_idx in channel_indexes:
                    future = executor.submit(
                        self._process_single_channel,
                        channel_idx,
                        sweep_idx,
                        start_sample,
                        end_sample,
                        each_point
                    )
                    future_to_channel[future] = channel_idx

                for future, channel_idx in future_to_channel.items():
                    try:
                        channel_data = future.result()  # This blocks until the thread completes
                        results[channel_idx] = channel_data
                    except Exception as exc:
                        print(f"Channel {channel_idx} generated an exception: {exc}")
                        # Fallback: return zeros if processing fails
                        results[channel_idx] = np.zeros(output_number_of_dots, dtype=np.float64)

        return results

    def _process_single_channel(self, channel_idx: int, sweep_idx: int,
                                start_sample: int, end_sample: int,
                                each_point: int) -> np.ndarray[np.float64]:
        """
        Process a single channel's data pipeline.
        This method runs in a separate thread for each channel.
        """
        # Read only the required data for this specific channel
        channel_data = self.data_memmaps[channel_idx][sweep_idx, start_sample:end_sample:each_point].astype(np.float64)

        # Convert to voltage
        channel_data = self.from_int16_to_voltage_val(channel_data, channel_idx)

        # Apply filters and transformations if needed
        # You can add your filter and transformation logic here

        return channel_data

    def from_int16_to_voltage_val(self, data: np.ndarray, channel_idx: int):
        return np.multiply(self.channel_scale(self.header.channel_info.analog_max[channel_idx],
                                              self.header.channel_info.analog_min[channel_idx],
                                              self.header.channel_info.digital_max[channel_idx],
                                              self.header.channel_info.digital_min[channel_idx]),
                           data)
        # if self.header.type_before_conversion == "rhs":
        #     return np.multiply(0.195, data)
        # elif self.header.type_before_conversion == "daq":
        #     pass
        # else:
        #     raise NotImplementedError(f"from_int16_to_voltage_val is not implemented for "
        #                               f"{self.header.type_before_conversion}")

    @staticmethod
    @lru_cache(maxsize=1024)
    def channel_scale(analog_max, analog_min, digital_max, digital_min):
        return 1000.0 * (analog_max - analog_min) / (digital_max - digital_min)


def weegit_experiment_folder_required(method):
    def wrapper(self, *args, **kwargs):
        if self.weegit_experiment_folder is None:
            raise ValueError("Select weegit experiment folder first'")
        return method(self, *args, **kwargs)
    return wrapper


class WeegitSessionManager(BaseModel):
    weegit_experiment_folder: Optional[Path] = None
    current_user_session: Optional[UserSession] = None
    experiment_data: Optional[ExperimentData] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def user_session(self) -> UserSession:
        if self.current_user_session is None:
            raise ValueError("Select weegit experiment folder first")

        return self.current_user_session

    def session_name_already_exists(self, session_name: str):
        return self.session_filename_already_exists(UserSession.session_name_to_filename(session_name))

    def session_filename_already_exists(self, session_filename: str):
        return (session_filename in self.other_session_filenames
                or self.current_user_session is not None
                and session_filename == self.current_user_session.session_filename)

    def new_user_session(self, session_filename: str):
        if self.session_filename_already_exists(session_filename):
            raise SessionAlreadyExistsError

        all_channels = list(range(self.experiment_data.header.number_of_channels))
        self.current_user_session = UserSession(session_filename=session_filename,
                                                eeg_channel_indexes=all_channels,
                                                gui_setup=GuiSetup(visible_channel_indexes=all_channels))
        self.save_user_session()

    def export_current_session(self, destination_path: Path) -> str:
        self.current_user_session.save_session(destination_path)
        return self.current_user_session.session_filename

    @weegit_experiment_folder_required
    def import_new_session(self, user_session: UserSession):
        user_session.save_session(UserSession.sessions_folder(self.weegit_experiment_folder))

    @weegit_experiment_folder_required
    def switch_sessions(self, session_filename: str):
        self.current_user_session = UserSession.load_from_default_folder(self.weegit_experiment_folder,
                                                                         session_filename)

    @staticmethod
    def parse_session_file(session_filepath: Path):
        return UserSession.parse_session_file(session_filepath)

    @weegit_experiment_folder_required
    def save_user_session(self):
        self.current_user_session.save_session(UserSession.sessions_folder(self.weegit_experiment_folder))

    def init_from_folder(self, weegit_experiment_folder: Path):
        sessions_folder = UserSession.sessions_folder(weegit_experiment_folder)
        sessions_folder.mkdir(exist_ok=True)
        header, data_memmaps = WeegitIO.read_weegit(weegit_experiment_folder)
        self.experiment_data = ExperimentData(header=header, data_memmaps=data_memmaps)
        self.weegit_experiment_folder = weegit_experiment_folder

    @property
    def session_is_active(self):
        return self.weegit_experiment_folder is not None

    @property
    @weegit_experiment_folder_required
    def other_session_filenames(self):
        session_filenames = []
        if self.weegit_experiment_folder:
            sessions_folder = UserSession.sessions_folder(self.weegit_experiment_folder)
            for file in os.listdir(sessions_folder):
                if UserSession.is_session_file(file):
                    session_filenames.append(file)

        return session_filenames

    def update_right_panel_widgets(self, right_panel_widgets: List):
        if self.current_user_session is not None:
            self.current_user_session.gui_setup.right_panel_widgets = right_panel_widgets
