from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.flight import Flight
from schemas.flight import FlightCreate, FlightResponse

router = APIRouter()

# READ all flights
@router.get("/flights", response_model=list[FlightResponse])
def get_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()

# CREATE flight
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

# UPDATE flight
@router.put("/flights/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    updated_flight: FlightCreate,
    db: Session = Depends(get_db)
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    flight.flight_number = updated_flight.flight_number
    flight.origin = updated_flight.origin
    flight.destination = updated_flight.destination
    flight.status = updated_flight.status

    db.commit()
    db.refresh(flight)
    return flight

# DELETE flight
@router.delete("/flights/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()
    return {"message": "Flight deleted successfully"}
