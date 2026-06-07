from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Any, Dict

class EventType(str, Enum):
    CLICK    = "click"
    VIEW     = "view"
    PURCHASE = "purchase"


class Event(BaseModel):
    eventId:str
    source:str
    type:EventType
    timestamp:datetime
    payload:   Dict[str, Any]



