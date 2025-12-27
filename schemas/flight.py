
from pydantic import BaseModel
from datetime import date, time

class FlightBase(BaseModel):
    flight_number: str
    origin: str
    destination: str
    status: str

    flight_date: date
    departure_time: time
    arrival_time: time
    terminal: str
    gate: str

class FlightCreate(FlightBase):
    pass

class FlightResponse(FlightBase):
    id: int

    class Config:
        from_attributes = True