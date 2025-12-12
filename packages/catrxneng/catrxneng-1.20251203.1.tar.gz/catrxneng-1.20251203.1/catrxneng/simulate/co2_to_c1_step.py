import numpy as np

from .step import Step


class Co2ToC1Step(Step):

    def simulate(self, dt_sec, std_dev=None):
        super().simulate(dt_sec, std_dev)
        df = self.time_series_data
        df["n2_mfc"] = self.reactor.F0["inert"].smLmin * np.random.normal(
            loc=1, scale=std_dev["mfc"], size=self.num_points
        )
        df["co2_mfc"] = self.reactor.F0["co2"].smLmin * np.random.normal(
            loc=1, scale=std_dev["mfc"], size=self.num_points
        )
        df["h2_mfc"] = self.reactor.F0["h2"].smLmin * np.random.normal(
            loc=1, scale=std_dev["mfc"], size=self.num_points
        )

        self.populate_inlet_partial_pressures()
        df = df.rename(columns={"inert_gc_conc": "n2_gc_conc", "p_inert": "p_n2"})
        df["dme_gc_conc"] = 0.0
        if "ch4_gc_conc" not in df.columns:
            df["ch4_gc_conc"] = 0.0
        self.time_series_data = df
