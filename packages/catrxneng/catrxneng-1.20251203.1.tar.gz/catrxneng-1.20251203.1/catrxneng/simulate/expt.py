import os, requests, pandas as pd
from typing import List, Any

from .. import utils
from .. import quantities as quant
from .step import Step
from ..reactors import PFR
from .unit import Unit
from ..material import Material


class Expt:

    @property
    def steady_state_steps(self) -> List[Step]:
        return [step for step in self.steps if step.step_name == "steadyState"]

    @property
    def date_str(self):
        return self.steps[0].start.date_str

    def __init__(
        self,
        expt_class_name: str,
        reactor_class: type[PFR],
        step_class: type[Step],
        material: Material,
        sample_mass: quant.Mass,
        unit: Unit,
        lab_notebook_id: str,
        project: str,
    ):
        self.expt_class_name = expt_class_name
        self.step_class = step_class
        self.reactor_class = reactor_class
        self.material = material
        self.sample_mass = sample_mass
        self.unit = unit
        self.lab_notebook_id = lab_notebook_id
        self.project = project
        self.steps: List[Step] = []

    def add_step(
        self,
        step_name: str,
        duration: quant.TimeDelta,
        T: quant.Temperature,
        p0: quant.Pressure,
        whsv: quant.WHSV | None = None,
        F0: quant.MolarFlowRate | None = None,
        start: utils.Time | None = None,
    ):
        if start is None:
            start = self.steps[-1].end
        end = start + duration
        reactor = self.reactor_class(
            T=T,
            kinetic_model_class=self.material.KINETIC_MODEL_CLASS,
            kinetic_model_kwargs=self.material.kinetic_model_kwargs,
            p0=p0,
            whsv=whsv,
            F0=F0,
            mcat=self.sample_mass,
        )
        step = self.step_class(
            self, step_name, len(self.steps) + 1, start, end, reactor
        )
        self.steps.append(step)

    def simulate(self, dt_sec: int, std_dev: dict[str, float] = None):
        for step in self.steps:
            step.simulate(dt_sec, std_dev)
        dataframes = [step.time_series_data for step in self.steps]
        self.time_series_data = pd.concat(dataframes, ignore_index=True)
        self._compute_tos()
        for index, step in enumerate(self.steady_state_steps):
            step.steady_state_step_num = index + 1

    def upload_data_to_influx(self, bucket: str, measurement: str):
        influx = utils.Influx(
            url=os.getenv("INFLUXDB_URL"),
            org=os.getenv("INFLUXDB_ORG"),
            bucket=bucket,
            measurement=measurement,
        )
        tag_map = {key: value["tag"] for key, value in self.unit.tags.items()}
        df = self.time_series_data.rename(columns=tag_map)
        influx.upload_dataframe(dataframe=df, token=os.getenv("INFLUXDB_TOKEN"))

    def _compute_tos(self):
        for step in self.steps:
            if step.step_name == "steadyState":
                start = step.start.UET
                break
        self.tos_sec = self.time_series_data["timestamp"] - start
        self.tos_hr = self.tos_sec / 3600.0

    def upload_to_emp(self, host: str, dt_sec: int, notes: str = "") -> dict[str, Any]:
        endpoint = f"/api/create_simulated_expt/{self.project}"
        url = host + endpoint
        params = {
            "expt_class": self.expt_class_name,
            "lab_notebook_id": self.lab_notebook_id,
            "test_unit": self.test_unit_id,
            "material__common_name": self.catalyst_common_name,
            "sample_mass": self.sample_mass.g,
            "start__ET_str": self.steps[0].start.ET_str,
            "end__ET_str": self.steps[-1].end.ET_str,
            "dt_sec": dt_sec,
            "notes": notes,
        }
        self.delete_from_emp(host)
        resp = requests.post(url, json=params, timeout=10)

        if not resp.ok:
            try:
                error_data = resp.json()
                return {"status_code": resp.status_code, "error": error_data}
            except ValueError:
                return {"status_code": resp.status_code, "body": resp.text}

        try:
            return resp.json()
        except ValueError:
            return {"status_code": resp.status_code, "body": resp.text}

    def delete_from_emp(self, host: str):
        endpoint = f"/api/delete_expt/{self.project}"
        if not host.startswith("http://") and not host.startswith("https://"):
            host = "http://" + host
        url = host + endpoint
        params = {"lab_notebook_id": self.lab_notebook_id, "project": self.project}
        resp = requests.delete(url, json=params, timeout=10)

        if not resp.ok:
            try:
                error_data = resp.json()
                return {"status_code": resp.status_code, "error": error_data}
            except ValueError:
                return {"status_code": resp.status_code, "body": resp.text}

        try:
            return resp.json()
        except ValueError:
            return {"status_code": resp.status_code, "body": resp.text}

    def compute_inlet_partial_pressures(self) -> pd.DataFrame:
        df = self.time_series_data.copy()
        mask = [col for col in df.columns if "_mfc" in col]
        total_inlet_flow_molh = df[mask].sum(axis=1)
        for col in mask:
            y = df[col] / total_inlet_flow_molh
            p_col_id = f"p_{col.split('_mfc')[0]}_bar"
            df[p_col_id] = y * df["pressure"]
        return df
