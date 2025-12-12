from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..kinetic_models import KineticModel


class Material:
    KINETIC_MODEL_CLASS: type["KineticModel"]
    kinetic_model: "KineticModel"
    kinetic_model_kwargs: dict
    project: str
    common_name: str
    lab_notebook_id: str
