from typing import Dict,Optional
from Data.eventEntity import Event

class EventRepo:
    def __init__(self):
        self._store: Dict[str,Event]={}

    def save(self,event:Event)->bool:
        if event.eventId in self._store:
            return False
        self._store[event.eventId]=event
        return True
    def find_by_id(self,event_id:str)->Optional[Event]:
        return self._store.get(event_id)
    def find_all(self)->list[Event]:
        return list(self._store.values())
    def exists(self,event_id:str)->bool:
        return event_id in self._store