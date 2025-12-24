from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.flight import Flight
from schemas.flight import FlightCreate, FlightResponse

router = APIRouter()

@router.get("/flights", response_model=list[FlightResponse])
def get_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()

@router.post("/flights", response_model=FlightResponse)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    new_flight = Flight(
        flight_number=flight.flight_number,
        origin=flight.origin,
        destination=flight.destination,
        status=flight.status
    )
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight
