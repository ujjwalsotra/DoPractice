from fastapi import FastAPI,HTTPException
import logging
from Data.eventEntity import Event, EventType
from exception import NoDataException
from typing import List
from repository import EventRepo
from service import EventService

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

app = FastAPI(title= "DataIngestion")
repo = EventRepo()
service = EventService(repo)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/events/summary")
def get_summary():
   events = repo.find_all()
   counts = {e.value:0 for e in EventType}
   for event in events:
       counts[event.type.value] += 1
   return counts

@app.post("/events",status_code=201)
def ingest_events(events:List[Event]):
    logger.info(f"Ingesting {len(events)} events")
    result = service.ingest_events(events)
    return result


@app.get("/events/{event_id}")
def get_event(event_id:str):
    event = repo.find_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404,detail=f"Event {event_id} not found")
    return event