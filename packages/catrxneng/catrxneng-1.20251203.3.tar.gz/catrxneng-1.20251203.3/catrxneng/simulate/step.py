import pandas as pd
import numpy as np
from typing import TYPE_CHECKING

from ..reactors import PFR
from ..utils import Time

if TYPE_CHECKING:
    from catrxneng.simulate import Expt
    from ..simulate import Expt


class Step:
    steady_state_step_num: int

    @property
    def lab_notebook_id(self):
        return f"{self.expt.lab_notebook_id}-s{self.steady_state_step_num}"

    def __init__(
        self,
        expt: "Expt",
        step_name: str,
        step_num: int,
        start: Time,
        end: Time,
        reactor: PFR,
    ):
        self.expt = expt
        self.step_name = step_name
        self.step_num = step_num
        self.start = start
        self.end = end
        self.reactor = reactor

    def simulate(self, dt_sec: int, std_dev: dict[str, float] | None = None):
        self.std_dev = std_dev
        if std_dev is None:
            self.std_dev = {"temp": 0.3, "pressure": 0.005, "mfc": 0.005, "gc": 0.005}
        df = pd.DataFrame()
        df["timestamp"] = np.arange(self.start.UET, self.end.UET + dt_sec, dt_sec)
        self.num_points = df["timestamp"].size
        df["step_name"] = self.step_name
        df["step_num"] = self.step_num
        self.reactor.solve()
        df["bed_temp"] = self.reactor.T.C + np.random.normal(
            loc=0, scale=self.std_dev["temp"], size=self.num_points
        )
        df["pressure"] = self.reactor.P.bar * np.random.normal(
            loc=1, scale=self.std_dev["pressure"], size=self.num_points
        )

        for component in self.reactor.y.keys:
            df[f"{component}_gc_conc"] = self.reactor.y[-1][
                component
            ].pct * np.random.normal(
                loc=1, scale=self.std_dev["gc"], size=self.num_points
            )

        df["total_gc_conc"] = df.filter(like="gc_conc").sum(axis=1)
        self.time_series_data = df

        # add additional simulate logic in child class simulate method after calling super().simulate

    def populate_inlet_partial_pressures(self):
        df = self.time_series_data
        for component in self.reactor.kinetic_model_class.comp_list():
            df[f"p_{component}"] = df[f"{component}_gc_conc"] / 100 * df["pressure"]
