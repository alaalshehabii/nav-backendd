
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import relationship
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    flight_number = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    status = Column(String)

    flight_date = Column(Date)
    departure_time = Column(Time)
    arrival_time = Column(Time)
    terminal = Column(String)
    gate = Column(String)

    saved_by = relationship(
        "UserFlight",
        cascade="all, delete",
        backref="flight"
    )