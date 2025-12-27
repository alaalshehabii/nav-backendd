from sqlalchemy import Column, Integer, String
from database import Base

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)  # Gate / Security / Facility / General
    status = Column(String, nullable=False)    # Info / Delay / Closed
    message = Column(String, nullable=False)

