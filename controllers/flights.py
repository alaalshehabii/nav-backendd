
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.flight import Flight
from schemas.flight import FlightCreate, FlightResponse
from dependencies.get_current_user import get_current_user
from models.user import UserModel

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("", response_model=list[FlightResponse])
def get_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()


@router.post("", response_model=FlightResponse)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    new_flight = Flight(
        flight_number=flight.flight_number,
        origin=flight.origin,
        destination=flight.destination,
        status=flight.status,
    )

    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)

    return new_flight


@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight: FlightCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    existing_flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not existing_flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    existing_flight.flight_number = flight.flight_number
    existing_flight.origin = flight.origin
    existing_flight.destination = flight.destination
    existing_flight.status = flight.status

    db.commit()
    db.refresh(existing_flight)

    return existing_flight


@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(flight)
    db.commit()

    return {"message": "Flight deleted successfully"}

