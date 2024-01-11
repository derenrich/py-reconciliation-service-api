from typing import Dict, List, Literal, Optional, Union

from pydantic import RootModel
from pydantic.types import PositiveInt

from . import BaseSchema


class CompositePropertyValue(BaseSchema):
    id: str
    name: Optional[str] = None


PropertyValue = Union[str, float, int, bool, CompositePropertyValue]


class ReconciliationQueryProperty(BaseSchema):
    pid: str
    v: Union[List[PropertyValue], PropertyValue]


class ReconciliationQuery(BaseSchema):
    query: str
    type: Optional[Union[str, List[str]]] = None
    limit: Optional[PositiveInt] = None
    properties: Optional[List[ReconciliationQueryProperty]] = None
    type_strict: Optional[Literal["should", "all", "any"]] = None


class BatchReconciliationQuery(RootModel):
    root: Dict[str, ReconciliationQuery]


class ReconciliationFeature(BaseSchema):
    id: str
    value: Union[bool, float, int]


class ReconciliationType(BaseSchema):
    id: str
    name: Optional[str] = None


class ReconciliationCandidate(BaseSchema):
    id: str
    name: str
    score: float
    features: Optional[List[ReconciliationFeature]] = None
    match: Optional[bool] = None
    type: Optional[List[Union[str, ReconciliationType]]] = None


class ReconciliationResult(BaseSchema):
    result: List[ReconciliationCandidate]


class BatchReconciliationResult(RootModel):
    root: Dict[str, ReconciliationResult]
