from sqlalchemy import Column, Integer, String
from database import Base

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    terminal = Column(String)
    location_description = Column(String)
    opening_hours = Column(String)
