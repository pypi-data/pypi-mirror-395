from .abstract_source_reader import AbstractSourceReader, AbstractDataWriter
from weegit.core.header import Header, ChannelInfo
# import mne
from pathlib import Path
import datetime
from typing import Any, Tuple
import numpy as np


class EdfDataWriter(AbstractDataWriter):
    def __init__(self, raw):
        self._raw = raw
        self._n_channels = raw.info['nchan']
        self._n_times = raw.n_times
        self._n_sweeps = 1  # EDF files are single sweep

    def __iter__(self) -> "AbstractDataWriter":
        # Support [ch, t, sw] slicing, but sw is always 0
        # mne expects channel indices or names, and time indices
        self._start = 1
        self._end = 10
        data, _ = self._raw[self._start, self._end]
        # Add sweep dimension
        data = np.expand_dims(data, axis=-1)  # shape: (n_channels, n_times, 1)
        yield data


class EdfSourceReader(AbstractSourceReader):
    def __init__(self, experiment_path: Path):
        super().__init__(experiment_path)
        # self._raw = mne.io.read_raw_edf(experiment_path, preload=True)

    @classmethod
    def _try_to_open(cls, experiment_path):
        pass
        # mne.io.read_raw_edf(experiment_path)

    def __iter__(self) -> "AbstractSourceReader":
        return self

    def __next__(self) -> Tuple[Header, AbstractDataWriter]:
        pass

    def _init_header(self):
        info = self._raw.info
        n_channels = info['nchan']
        sample_rate = info['sfreq']
        ch_names = info['ch_names']
        n_points = self._raw.n_times
        # Placeholders for fields not available
        now = datetime.datetime.now()
        channelinfo = ChannelInfo(
            name=ch_names,
            probe=["unknown"] * n_channels,
            analogmin=[float('nan')] * n_channels,
            analogmax=[float('nan')] * n_channels,
            digitalmin=[-32768] * n_channels,
            digitalmax=[32767] * n_channels,
            prefiltering=[""] * n_channels,
            number_of_points_per_channel=[n_points] * n_channels
        )
        header = Header(
            type_before_conversion="edf",
            name_before_conversion=self._experiment_path.name,
            creation_date_before_conversion=now.strftime("%Y-%m-%d"),
            creation_time_before_conversion=now.strftime("%H:%M:%S"),
            sample_interval_microseconds=1e6 / sample_rate if sample_rate else 0,
            number_of_channels=n_channels,
            number_of_sweeps=1,
            number_of_points_per_sweep=n_points,
            channelinfo=channelinfo
        )
        return header

    def get_data_stream(self) -> AbstractDataWriter:
        return EdfDataWriter(self._raw)
