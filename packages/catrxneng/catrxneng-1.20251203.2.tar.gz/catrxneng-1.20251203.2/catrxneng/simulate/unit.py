import requests


class Unit:
    tags: dict[str, dict[str, str | int | float]]

    def __init__(self, test_unit_id: str, unit_class_name: str):
        self.test_unit_id = test_unit_id
        self.unit_class_name = unit_class_name

    def populate_attributes_from_emp(self, host: str):
        url = f"{host}/api/get_unit_data"
        params = {"unit_class_name": self.unit_class_name}
        response = requests.get(url, json=params).json()
        for key, value in response.items():
            setattr(self, key, value)

    def last_expt_number(self, host: str) -> int:
        url = f"{host}/api/get_last_unit_expt_number"
        params = {"test_unit_id": self.test_unit_id}
        response = requests.get(url, json=params).json()
        return response["data"]
