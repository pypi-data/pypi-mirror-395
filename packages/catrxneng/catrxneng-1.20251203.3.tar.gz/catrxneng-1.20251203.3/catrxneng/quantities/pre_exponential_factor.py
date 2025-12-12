from typing import Optional
from numpy.typing import NDArray
import numpy as np
from .. import utils
from .quantity import Quantity


class PreExponentialFactor(Quantity):
    def __init__(
        self,
        order: Optional[float] = None,
        *,
        si: Optional[float | NDArray] = None,
        molskgcatPa: Optional[float | NDArray] = None,
        molhgcatbar: Optional[float | NDArray] = None,
        keys: Optional[list] = None,
    ):
        self.order = order

        if sum(x is not None for x in [si, molskgcatPa, molhgcatbar]) > 1:
            raise ValueError("Only one pre-exponential factor unit should be specified")
        if si is not None:
            self.si = si
        elif molskgcatPa is not None:
            self.molskgcatPa = molskgcatPa
        elif molhgcatbar is not None:
            self.molhgcatbar = molhgcatbar
        else:
            self.si = np.zeros(len(keys)) if keys else 0

        if keys is not None:
            self.keys = keys

        super().__init__(keys=keys)

    @property
    def molskgcatPa(self):
        return self.si

    @molskgcatPa.setter
    def molskgcatPa(self, value):
        self.si = value

    @property
    def molhgcatbar(self):
        return self.si * 3600 / 1000 * (100000**self.order)

    @molhgcatbar.setter
    def molhgcatbar(self, value):
        self.si = value / 3600 * 1000 / (100000**self.order)
