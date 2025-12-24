from pydantic import BaseModel

# Shared fields
class FlightBase(BaseModel):
    flight_number: str
    origin: str
    destination: str
    status: str

# Used when creating a flight (NO id)
class FlightCreate(FlightBase):
    pass

# Used when returning data (HAS id)
class FlightResponse(FlightBase):
    id: int

    class Config:
        from_attributes = True
