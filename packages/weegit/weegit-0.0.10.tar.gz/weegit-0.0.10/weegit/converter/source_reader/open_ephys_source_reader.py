from typing import List, Dict
import numpy as np
from open_ephys.analysis import Session, RecordNode
from pathlib import Path
from datetime import datetime
import re

from .abstract_source_reader import AbstractSourceReader, AbstractDataWriter
from weegit.core.header import Header, ChannelInfo


class OpenEphysDataWriter(AbstractDataWriter):
    def __init__(self, channel_names: List[str], nodes, start_record_idx, end_record_idx,
                 start_continuous_idx, end_continuous_idx):
        self._channel_names = channel_names
        self._channels_num = len(self._channel_names)
        self._nodes = nodes
        self._start_record_idx = start_record_idx
        self._end_record_idx = end_record_idx
        self._start_continuous_idx = start_continuous_idx
        self._end_continuous_idx = end_continuous_idx
        self._channels_metadata = {}
        for channel_name in channel_names:
            for node_idx in range(len(nodes)):
                # fixme: we assume no difference in channel names inside the same node
                node_channel_names = nodes[node_idx].recordings[0].continuous[0].metadata["channel_names"]
                if channel_name in node_channel_names:
                    self._channels_metadata[channel_name] = {
                        "node": nodes[node_idx],
                        "channel_idx": node_channel_names.index(channel_name)
                    }
                    break

            else:
                raise ValueError(f"Channel name {channel_name} does not exist in the given nodes")

    def __iter__(self) -> "AbstractDataWriter":
        print(f"{self._start_record_idx=}, {self._end_record_idx=}, {self._start_continuous_idx=}, {self._end_continuous_idx=}")
        self._cur_record_idx = self._start_record_idx
        self._cur_continuous_idx = self._start_continuous_idx
        self._cur_sample_idx = 0
        return self

    def __next__(self) -> np.typing.NDArray[np.int16]:
        # print(f"{self._cur_record_idx=}, {self._cur_continuous_idx=}, {self._cur_sample_idx=}")
        if self._cur_record_idx == self._end_record_idx + 1:
            raise StopIteration

        cur_chunk = []
        try:
            # todo: optimize me
            for channel_name in self._channel_names:
                channel_node = self._channels_metadata[channel_name]["node"]
                cur_channel_idx = self._channels_metadata[channel_name]["channel_idx"]
                channel_data = channel_node.recordings[self._cur_record_idx] \
                    .continuous[self._cur_continuous_idx] \
                    .samples[self._cur_sample_idx][cur_channel_idx]
                cur_chunk.append(channel_data)

            self._cur_sample_idx += 1

        except IndexError:
            self._cur_sample_idx = 0
            self._cur_continuous_idx += 1
            if self._cur_continuous_idx == len(self._nodes[0].recordings[self._cur_record_idx].continuous):
                self._cur_record_idx += 1
                self._cur_continuous_idx = 0

        return np.array(cur_chunk, dtype='int16')

    def total_chunks(self, header: Header):
        return header.number_of_points_per_sweep * header.number_of_sweeps


class OpenEphysSourceReader(AbstractSourceReader):
    """
    Data formats: https://open-ephys.github.io/gui-docs/User-Manual/Data-formats/index.html
    """
    def __init__(self, experiment_path: Path):
        super().__init__(experiment_path)
        self._reader = None
        self._start_record_idx = 0
        self._end_record_idx = 0
        self._start_continuous_idx = 0
        self._end_continuous_idx = 0
        self._nodes = None
        self._settings_changed = False
        self._channel_names = set()

    @classmethod
    def _try_to_open(cls, experiment_path):
        Session(experiment_path)

    def __iter__(self):
        self._reader = Session(self._experiment_path)
        self._start_record_idx = 0
        self._end_record_idx = 0
        self._start_continuous_idx = 0
        self._end_continuous_idx = 0
        self._nodes = self._reader.recordnodes
        self._settings_changed = False
        self._channel_names = set()
        return self

    def __next__(self):
        # fixme: headstage different idxs (A,B) is not tested yet (because there is no exp example)
        # fixme:
        #  - we assume that every recording and continuous has the same length in nodes
        #  - header is the same for now (e.g. sample_rate)

        # fixme: for now we assume that all nodes have the same number of records
        if self._end_record_idx == len(self._nodes[0].recordings):
            raise StopIteration

        while (not self._settings_changed) and self._end_record_idx < len(self._nodes[0].recordings):
            continuous_number = 0
            for node in self._nodes:
                recording = node.recordings[self._end_record_idx]
                # fixme: for now we assume that all synced records in nodes have the same number of continuous
                continuous_number = len(recording.continuous)
                # fixme: for now we assume that all continuous in a recording have the same number of channels
                self._channel_names |= set(recording.continuous[0].metadata["channel_names"])
                # FIXME: when difference between A/B will be known this code must be rewritten
                #  (ch names will be the same [?], but must be different)

            for cur_record_continuous_idx in range(self._start_continuous_idx, continuous_number):
                # fixme: for now we assume that all continuous has the same header settings
                # if changed:
                #   self._end_continuous_idx = cur_record_continuous_idx
                #   self._settings_changed = True
                pass

            if not self._settings_changed:
                self._end_record_idx += 1
                self._end_continuous_idx = continuous_number - 1

        if not self._settings_changed:
            end_record_idx = self._end_record_idx - 1
        else:
            end_record_idx = self._end_record_idx

        sorted_channel_names = self._sorted_channel_names(self._channel_names)
        header = self._init_header(sorted_channel_names, self._nodes, self._start_record_idx, end_record_idx,
                                   self._start_continuous_idx, self._end_continuous_idx)
        data_stream = OpenEphysDataWriter(sorted_channel_names, self._nodes, self._start_record_idx, end_record_idx,
                                          self._start_continuous_idx, self._end_continuous_idx)

        if self._settings_changed:
            self._start_record_idx = self._end_record_idx
            self._start_continuous_idx = self._end_continuous_idx
            self._settings_changed = False
            self._channel_names = set()

        return header, data_stream

    @classmethod
    def _sorted_channel_names(cls, channel_names):
        return sorted(channel_names, key=lambda x: [int(c) if c.isdigit() else c for c in
                                                    re.split('(\d+)', x)])

    def _init_header(self, channel_names: List[str],
                     nodes: List[RecordNode], start_record_idx, end_record_idx,
                     start_continuous_idx, end_continuous_idx):
        channels_number = len(channel_names)
        sample_rate = nodes[0].recordings[0].continuous[0].metadata["sample_rate"]
        units = nodes[0].recordings[0].info["continuous"][0]["channels"][0]["units"]

        points_per_sweep = 0
        for record_idx in range(start_record_idx, end_record_idx + 1):
            # todo: fix bug with points_per_sweep: the value is wrong because samples are taken all over only one node,
            # some channels might not be there and some
            cur_start_continuous_idx = 0
            # fixme: assume the same between nodes
            cur_end_continuous_idx = len(nodes[0].recordings[record_idx].continuous) - 1
            if record_idx == start_record_idx:
                cur_start_continuous_idx = start_continuous_idx
            elif record_idx == end_record_idx:
                cur_end_continuous_idx = end_continuous_idx

            for continuous_idx in range(cur_start_continuous_idx, cur_end_continuous_idx + 1):
                continuous_samples_num = nodes[0].recordings[record_idx].continuous[continuous_idx].samples.shape
                points_per_sweep += continuous_samples_num[0] * continuous_samples_num[1]
        points_per_sweep /= channels_number

        channel_info = ChannelInfo(
            name=channel_names,
            probe=["unknown"] * channels_number,
            units=[units] * channels_number,
            analog_min=[-32768] * channels_number,
            analog_max=[32767] * channels_number,
            digital_min=[-32768] * channels_number,
            digital_max=[32767] * channels_number,
            prefiltering=[""] * channels_number,
            number_of_points_per_channel=[points_per_sweep] * channels_number
        )

        date = ""
        time = ""
        try:
            dt = datetime.strptime(self._experiment_path.name, "%Y-%m-%d_%H-%M-%S")
            date = str(dt.date())
            time = str(dt.time())
        except ValueError:
            pass

        header = Header(
            type_before_conversion="openephys",
            name_before_conversion=self._experiment_path.name,
            creation_date_before_conversion=date,
            creation_time_before_conversion=time,
            sample_interval_microseconds=1e6 / sample_rate,
            number_of_channels=len(channel_names),
            number_of_sweeps=1,
            number_of_points_per_sweep=points_per_sweep,
            channel_info=channel_info
        )

        return header
