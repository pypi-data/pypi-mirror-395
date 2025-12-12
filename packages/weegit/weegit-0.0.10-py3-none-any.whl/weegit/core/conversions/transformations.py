from abc import abstractmethod
from functools import cached_property

import numpy as np
from pydantic import BaseModel, computed_field


class BaseTransformation(BaseModel):
    @abstractmethod
    def apply_inplace(self, data: np.ndarray):
        raise NotImplemented
