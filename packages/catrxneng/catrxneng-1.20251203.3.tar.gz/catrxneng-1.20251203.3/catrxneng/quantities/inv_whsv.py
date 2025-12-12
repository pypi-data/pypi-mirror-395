from typing import Optional
from numpy.typing import NDArray
import numpy as np
from .quantity import Quantity
from catrxneng.utils import *


class InvWHSV(Quantity):

    def __init__(
        self,
        avg_mol_weight: Optional[float] = None,
        *,
        si: Optional[float | NDArray] = None,
        molskgcat: Optional[float | NDArray] = None,
        molhgcat: Optional[float | NDArray] = None,
        smLhgcat: Optional[float | NDArray] = None,
        inv_h: Optional[float | NDArray] = None,
        keys: Optional[list] = None,
    ):
        self.avg_mol_weight = avg_mol_weight

        if sum(x is not None for x in [si, molskgcat, molhgcat, smLhgcat, inv_h]) > 1:
            raise ValueError("Only one InvWHSV unit should be specified")
        if si is not None:
            self.si = si
        elif molskgcat is not None:
            self.molskgcat = molskgcat
        elif molhgcat is not None:
            self.molhgcat = molhgcat
        elif smLhgcat is not None:
            self.smLhgcat = smLhgcat
        elif inv_h is not None:
            self.inv_h = inv_h
        else:
            self.si = np.zeros(len(keys)) if keys else 0

        if keys is not None:
            self.keys = keys

        super().__init__(keys=keys)

    @property
    def molskgcat(self):
        return self.si

    @molskgcat.setter
    def molskgcat(self, value):
        self.si = value

    @property
    def molhgcat(self):
        return self.si / 3600 * 1000

    @molhgcat.setter
    def molhgcat(self, value):
        self.si = value * 3600 / 1000

    @property
    def smLhgcat(self):
        return self.si / 3600 / 22.4

    @smLhgcat.setter
    def smLhgcat(self, value):
        self.si = value * 3600 * 22.4

    @property
    def inv_h(self):
        try:
            return self.si / 1000 * self.avg_mol_weight * 3600
        except TypeError:
            raise AttributeError("WHSV has no avg_mol_weight assigned.")

    @inv_h.setter
    def inv_h(self, value):
        try:
            self.si = value * 1000 / self.avg_mol_weight / 3600
        except TypeError:
            raise AttributeError("WHSV has no avg_mol_weight assigned.")
