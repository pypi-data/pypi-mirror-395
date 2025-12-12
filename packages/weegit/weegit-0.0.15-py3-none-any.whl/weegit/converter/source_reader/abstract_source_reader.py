from abc import ABC, abstractmethod
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Tuple, List

import numpy as np

from weegit import settings
from weegit.core.header import Header
from ._exceptions import WrongSourceReaderError


class AbstractDataWriter(ABC):
    @abstractmethod
    def __iter__(self) -> "AbstractDataWriter":
        raise NotImplemented

    def __next__(self) -> np.ndarray[np.int16]:
        raise NotImplemented

    def to_dest_folder(self, dest_folder: Path, header: Header) -> List[Path]:
        # fixme: rewrite to NotImeplemented and implement in each class wisely
        total_chunks = self.total_chunks(header)

        channel_filepaths = [dest_folder / settings.LFP_SUBFOLDER / f"{ch_idx}{settings.LFP_EXTENSION}"
                             for ch_idx in range(header.number_of_channels)]
        files = [open(filepath, "wb") for filepath in channel_filepaths]
        for i, chunk in enumerate(self):
            for ch_idx in range(header.number_of_channels):
                files[ch_idx].write(chunk[ch_idx, :])

            yield min(int((i / total_chunks) * 100), 99)

        for file in files:
            file.close()

        return channel_filepaths

    @abstractmethod
    def total_chunks(self, header: Header) -> int:
        raise NotImplemented


class AbstractSourceReader(ABC):
    def __init__(self, experiment_path: Path):
        self._experiment_path = experiment_path

    @classmethod
    def try_to_open(cls, experiment_path):
        try:
            cls._try_to_open(experiment_path)
        except Exception:
            raise WrongSourceReaderError(cls)

    @abstractmethod
    def __iter__(self) -> "AbstractSourceReader":
        raise NotImplemented

    @abstractmethod
    def __next__(self) -> Tuple[Header, AbstractDataWriter]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def _try_to_open(cls, experiment_path):
        raise NotImplemented
