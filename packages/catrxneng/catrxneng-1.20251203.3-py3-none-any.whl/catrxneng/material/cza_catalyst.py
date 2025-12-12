import numpy as np


from .. import kinetic_models, quantities as quant
from . import Material


class CzaCatalyst(Material):
    KINETIC_MODEL_CLASS = kinetic_models.co2_to_c1.PowerLawCzaSim

    def __init__(
        self,
        project: str,
        T_cal: quant.Temperature,
        ZnO_wtpct: float,
        co2_order: float = 0.5,
        h2_order: float = 0.5,
        common_name: str | None = None,
    ):
        self.project = project
        self.T_cal = T_cal
        self.ZnO_wtpct = ZnO_wtpct
        self.T_cal_norm = (T_cal.C - 320) / 60
        self.ZnO_norm = (ZnO_wtpct - 25) / 10
        self.co2_order = co2_order
        self.h2_order = h2_order
        self.order = co2_order + h2_order
        if common_name is None:
            self.common_name = f"60Cu{ZnO_wtpct:.0f}/Al2O3-{T_cal.C:.0f}"
        else:
            self.common_name = common_name
        self.kinetic_model_kwargs = {"kref": self.kref_molhgcatbar, "Ea": self.Ea_kJmol}

    def to_dict(self):
        return {
            "material_class_name": "CzaCatalyst",
            "common_name": self.common_name,
            "kinetic_model": "co2_to_meoh.PowerLawCzaSim",
            "project": self.project,
            "T_cal_C": self.T_cal.C,
            "ZnO_wtpct": self.ZnO_wtpct,
            "kref_molhgcatbar": self.kref_molhgcatbar,
            "Ea_kJmol": self.Ea_kJmol,
            "co2_order": self.co2_order,
            "h2_order": self.h2_order,
        }

    @property
    def kref_molhgcatbar(self):
        """
        Reference rate constant for CO2 hydrogenation to methanol at 250°C

        Power law kinetics: r = k · P_CO2^α · P_H2^β · (1 - Q/K_eq)

        Parameters:
        -----------
        T_calc : float or array
                Calcination temperature in °C (range: 260-380°C)
        ZnO_wt : float or array
                ZnO weight percentage (range: 15-35 wt%)
        noise_level : float
                Relative noise to add (default 8%)

        Returns:
        --------
        k_ref : float or array
                Reference rate constant in mol/(g_cat·h·bar^(α+β)) at 250°C
                With α=0.5, β=0.5: units are mol/(g_cat·h·bar)
        """

        try:
            return self._kref_molhgcatbar_cache

        except AttributeError:
            # Coefficients for realistic range
            # Peak activity ~2e-4 mol/(g·h·bar) at optimal conditions
            # beta_0 = 6.5e-4
            # beta_1 = -2e-6
            # beta_2 = 3e-5
            # beta_3 = -2.5e-4
            # beta_4 = -3e-4
            # beta_5 = -2e-5
            # multiplier = 0.5
            beta_0 = 1.5e-4
            beta_1 = -2e-5
            beta_2 = 3e-5
            beta_3 = -5e-5
            beta_4 = -4e-5
            beta_5 = -2e-5
            multiplier = 1

            # Linear combination
            self._kref_molhgcatbar_cache = (
                beta_0
                + beta_1 * self.T_cal_norm
                + beta_2 * self.ZnO_norm
                + beta_3 * self.T_cal_norm**2
                + beta_4 * self.ZnO_norm**2
                + beta_5 * self.T_cal_norm * self.ZnO_norm
            ) * multiplier

            # Physical bounds
            # k_ref = np.clip(k_ref, 1e-5, 3e-4)

            return self._kref_molhgcatbar_cache

    @property
    def Ea_kJmol(self):
        """
        Activation energy for CO2-to-methanol in kJ/mol

        Literature range: 75-105 kJ/mol
        """
        try:
            return self.Ea_kJmol_cache

        except AttributeError:
            # Coefficients
            gamma_0 = 88.0
            gamma_1 = 2.0
            gamma_2 = -1.5
            gamma_3 = 5.5
            gamma_4 = 6.5
            gamma_5 = 2.5

            self.Ea_kJmol_cache = (
                gamma_0
                + gamma_1 * self.T_cal_norm
                + gamma_2 * self.ZnO_norm
                + gamma_3 * self.T_cal_norm**2
                + gamma_4 * self.ZnO_norm**2
                + gamma_5 * self.T_cal_norm * self.ZnO_norm
            )

            # Ea = np.clip(Ea, 75, 105)
            return self.Ea_kJmol_cache

    @staticmethod
    def K_eq_methanol(T):
        """
        Equilibrium constant for CO2 + 3H2 ⇌ CH3OH + H2O

        Based on Graaf et al. (1988)

        Parameters:
        -----------
        T : float or array
                Temperature in K

        Returns:
        --------
        K_eq : float or array
                Equilibrium constant (bar^-2 basis for fugacity/pressure)
        """
        # Graaf correlation
        log10_K_eq = -3066 / T + 10.592
        K_eq = 10**log10_K_eq

        return K_eq

    def reaction_rate_methanol(
        self,
        P_CO2,
        P_H2,
        P_H2O,
        P_MeOH,
        k_ref,
        Ea,
        T,
        alpha=0.5,
        beta=0.5,
        T_ref=523.15,
    ):
        """
        Power law rate expression with approach to equilibrium factor

        CO2 + 3H2 ⇌ CH3OH + H2O

        r = k(T) · P_CO2^α · P_H2^β · (1 - Q/K_eq)

        Parameters:
        -----------
        P_CO2, P_H2, P_H2O, P_MeOH : float or array
                Partial pressures in bar
        k_ref : float
                Rate constant at reference T in mol/(g_cat·h·bar^(α+β))
        Ea : float
                Activation energy in kJ/mol
        T : float or array
                Temperature in K
        alpha : float
                Reaction order for CO2 (default 0.5)
        beta : float
                Reaction order for H2 (default 0.5)
        T_ref : float
                Reference temperature in K (default 523.15 K = 250°C)

        Returns:
        --------
        r : float or array
                Reaction rate in mol/(g_cat·h)
        """
        R = 8.314e-3  # kJ/(mol·K)

        # Arrhenius temperature dependence
        k = k_ref * np.exp(-Ea / R * (1 / T - 1 / T_ref))

        # Forward rate with power law
        r_forward = k * P_CO2**alpha * P_H2**beta

        # Equilibrium constant
        K_eq = self.K_eq_methanol(T)

        # Reaction quotient Q = (P_MeOH · P_H2O) / (P_CO2 · P_H2^3)
        Q = (P_MeOH * P_H2O) / (P_CO2 * P_H2**3 + 1e-10)

        # Approach to equilibrium factor (beta factor)
        beta_factor = 1 - Q / K_eq

        # Net rate
        r = r_forward * beta_factor

        # Ensure non-negative (only consider forward reaction)
        r = np.maximum(r, 0.0)

        return r
