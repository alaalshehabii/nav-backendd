from pydantic import BaseModel

class Flight(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    status: str
