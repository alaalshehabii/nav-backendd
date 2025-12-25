from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class UserFlight(Base):
    __tablename__ = "user_flights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)