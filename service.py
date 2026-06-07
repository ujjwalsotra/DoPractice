from typing import List,Dict
from Data.eventEntity import Event, EventType
from repository import EventRepo

class EventService:
    def __init__(self,repo:EventRepo):
        self.repo=repo

    def ingest_events(self,events:List[Event])->dict:
        saved =0
        rejected = 0
        cur_events:Dict[str,Event] ={}
        for event in events:
            if self.repo.exists(event.eventId):
                rejected+=1
                continue
            self.repo.save(event)
            saved+=1
        return {"saved":saved,"rejected":rejected}

    def get_summary(self)->dict:
        events = self.repo.find_all()
        counts = {e.value:0 for e in EventType}
        for event in events:
            counts[event.type.value]+=1
        return counts

    def get_events_by_id(self,event_id:str):
        return self.repo.find_by_id(event_id)