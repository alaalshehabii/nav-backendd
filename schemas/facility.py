from pydantic import BaseModel

# Shared fields
class FacilityBase(BaseModel):
    name: str
    type: str
    terminal: str
    location_description: str
    opening_hours: str

# For creating facility (NO id)
class FacilityCreate(FacilityBase):
    pass

# For responses (HAS id)
class FacilityResponse(FacilityBase):
    id: int

    class Config:
        from_attributes = True
