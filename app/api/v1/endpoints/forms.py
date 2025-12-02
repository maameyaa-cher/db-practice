from fastapi import APIRouter
from app.models.urla_2021_v1.urla_2021_v1 import Application

router = APIRouter()


@router.get("/schema/urla_2021_v1", response_model_by_alias=False)
def get_urla_2021_v1_schema():
    """
    Returns the JSON schema for the URLA 2021 v1 dynamic form.
    """
    return Application.model_json_schema()
