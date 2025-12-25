from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    status = Column(String)

    saved_by = relationship(
        "UserFlight",
        cascade="all, delete",
        backref="flight"
    )
