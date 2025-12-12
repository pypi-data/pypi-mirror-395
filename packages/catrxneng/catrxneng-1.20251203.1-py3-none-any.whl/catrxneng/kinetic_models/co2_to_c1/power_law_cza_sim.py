import numpy as np
from numpy.typing import NDArray
from typing import TYPE_CHECKING

from ..kinetic_model import KineticModel
from ...reactions import Co2ToMeoh
from ... import species as species
from ... import quantities as quant

if TYPE_CHECKING:
    from ...reactors import Reactor


class PowerLawCzaSim(KineticModel):
    LIMITING_REACTANT = "co2"
    T_REF = quant.Temperature(C=250)
    REACTANTS = {
        "co2": species.CO2,
        "h2": species.H2,
    }
    PRODUCTS = {
        "ch3oh": species.CH3OH,
        "h2o": species.H2O,
    }
    REACTIONS = {
        "co2_to_meoh": Co2ToMeoh,
    }
    H2_ORDER = 0.5
    CO2_ORDER = 0.5
    ORDER = np.array([H2_ORDER + CO2_ORDER])
    STOICH_COEFF = np.array(
        [
            [-1, -3, 1, 1, 0],
        ]
    )
    KREF = np.array([0.000373])
    EA = np.array([100])
    KREF_UNITS = "molhgcatbar"
    EA_UNITS = "kJmol"

    def compute_temp_dependent_constants(self):
        self.Keq_co2_to_meoh = Co2ToMeoh.Keq(self.T)
        self.Keq = np.array([self.Keq_co2_to_meoh])
        self.k = self.compute_rate_constants()

    def rate_equations(self, p_array: NDArray) -> np.ndarray:
        """
        Pressure in bar
        Rates in mol/h/gcat
        """

        p_co2 = p_array[0]  # co2
        p_h2 = p_array[1]  # h2
        p_ch3oh = p_array[2]  # ch3oh
        p_h2o = p_array[3]  # h2o

        # Reaction 1: CO2 + 3H2 -> CH3OH + H2O (CO2-to-MeOH)
        p_h2_3 = p_h2 * p_h2 * p_h2
        beta = 1 / self.Keq_co2_to_meoh * p_ch3oh * p_h2o / p_co2 / p_h2_3
        r1 = self.k[0] * p_h2**self.H2_ORDER * p_co2**self.CO2_ORDER * (1 - beta)

        return np.array(
            [
                -r1,  # co2
                -3 * r1,  # h2
                r1,  # ch3oh
                r1,  # h2o
                0.0 * r1,  # inert
            ]
        )

    @classmethod
    def compute_yield(cls, reactor: "Reactor") -> dict[str, NDArray]:
        yld = {
            prod_id: (reactor.F[prod_id].molh - reactor.F0[prod_id].molh)
            / reactor.F0[cls.LIMITING_REACTANT].molh
            for prod_id in cls.PRODUCTS
        }
        return yld

    def compute_equilibrium_yield(self) -> dict[str, quant.Fraction]:
        yld = {
            prod_id: self.eq_delta_moles[prod_id]
            / self.initial_moles[self.LIMITING_REACTANT]
            for prod_id in self.PRODUCTS
        }
        return yld  # type: ignore
