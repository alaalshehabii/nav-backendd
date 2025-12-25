from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user_flight import UserFlight
from models.flight import Flight
from models.user import UserModel
from dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/my-flights", tags=["My Flights"])

# ADD flight to my flights
@router.post("/{flight_id}")
def add_to_my_flights(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    existing = db.query(UserFlight).filter(
        UserFlight.user_id == current_user.id,
        UserFlight.flight_id == flight_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Flight already added")

    user_flight = UserFlight(
        user_id=current_user.id,
        flight_id=flight_id
    )

    db.add(user_flight)
    db.commit()

    return {"message": "Flight added to My Flights"}

# GET my flights
@router.get("/")
def get_my_flights(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    flights = (
        db.query(Flight)
        .join(UserFlight)
        .filter(UserFlight.user_id == current_user.id)
        .all()
    )
    return flights

# REMOVE flight
@router.delete("/{flight_id}")
def remove_from_my_flights(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    record = db.query(UserFlight).filter(
        UserFlight.user_id == current_user.id,
        UserFlight.flight_id == flight_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Flight not in My Flights")

    db.delete(record)
    db.commit()

    return {"message": "Flight removed from My Flights"}
