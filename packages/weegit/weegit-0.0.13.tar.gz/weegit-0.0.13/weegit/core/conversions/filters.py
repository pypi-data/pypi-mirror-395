from abc import abstractmethod
from functools import cached_property

import numpy as np
from pydantic import BaseModel, computed_field


class BaseFilter(BaseModel):
    @abstractmethod
    def apply_inplace(self, data: np.ndarray):
        raise NotImplemented


# todo: implement chebishev
class LowPassFilter(BaseFilter):
    var: float = 0

    def apply_inplace(self, data: np.ndarray):
        print(self, " filter applied")

    # @computed_field
    # @cached_property
    # def var2(self):
    #     return self.var + 1


class HighPassFilter(BaseFilter):
    var: float = 0

    def apply_inplace(self, data: np.ndarray):
        print(self, " filter applied")


class BandPassFilter(BaseFilter):
    var: float = 0

    def apply_inplace(self, data: np.ndarray):
        print(self, " filter applied")
