
from pydantic import BaseModel

# Shared fields
class FacilityBase(BaseModel):
    name: str
    type: str
    terminal: str
    location_description: str  # e.g. "Near Gate A3"

# For creating facility
class FacilityCreate(FacilityBase):
    pass

# For responses
class FacilityResponse(FacilityBase):
    id: int

    class Config:
        from_attributes = True
