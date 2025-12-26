
from sqlalchemy import Column, Integer, String
from database import Base

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    terminal = Column(String, nullable=False)
    location_description = Column(String, nullable=False)
