from typing import List, Optional
from pydantic import BaseModel, Field


class LMResponse(BaseModel):
    is_validated: bool = Field(default=False)


class ClassificationResponse(LMResponse):
    labels: List[str]
    extra_params: dict = Field(default={})


class NERResponse(LMResponse):
    entity: List[str]
    entity_type: List[str]
    start_index: Optional[List[int]]
    extra_params: dict = Field(default={})
