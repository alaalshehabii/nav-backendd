from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserFlight(Base):
    __tablename__ = "user_flights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"))

    user = relationship("UserModel", back_populates="flights")
    flight = relationship("Flight", back_populates="users")
