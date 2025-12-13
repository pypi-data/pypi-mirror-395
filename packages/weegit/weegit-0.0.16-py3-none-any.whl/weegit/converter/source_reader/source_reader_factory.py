from ._exceptions import WrongSourceReaderError
from .old_weegit_reader import OldWeegitSourceReader
from .open_ephys_source_reader import OpenEphysSourceReader
from .intan_rhs_source_reader import IntanRhsSourceReader
from .edf_source_reader import EdfSourceReader
from pathlib import Path


class SourceReaderFactory:
    @staticmethod
    def get_reader(experiment_path: Path):
        for reader_class in (OpenEphysSourceReader,
                             IntanRhsSourceReader,
                             OldWeegitSourceReader,):
            try:
                reader_class.try_to_open(experiment_path)
                return reader_class(experiment_path)
            except WrongSourceReaderError:
                pass

        raise ValueError(f"Unsupported experiment format: {experiment_path}")
