from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.flight import Flight
from models.user_flight import UserFlight
from models.user import UserModel

router = APIRouter(prefix="/my-flights", tags=["My Flights"])


@router.get("")
def get_my_flights(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    saved = (
        db.query(UserFlight)
        .filter(UserFlight.user_id == current_user.id)
        .all()
    )

    # safer + modern than .get()
    flight_ids = [s.flight_id for s in saved]
    if not flight_ids:
        return []

    flights = db.query(Flight).filter(Flight.id.in_(flight_ids)).all()
    return flights


@router.post("/{flight_id}")
def save_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check flight exists
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    exists = (
        db.query(UserFlight)
        .filter(
            UserFlight.user_id == current_user.id,
            UserFlight.flight_id == flight_id
        )
        .first()
    )

    if exists:
        raise HTTPException(status_code=400, detail="Flight already saved")

    saved = UserFlight(user_id=current_user.id, flight_id=flight_id)
    db.add(saved)
    db.commit()
    return {"message": "Flight saved"}


@router.delete("/{flight_id}")
def remove_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    saved = (
        db.query(UserFlight)
        .filter(
            UserFlight.user_id == current_user.id,
            UserFlight.flight_id == flight_id
        )
        .first()
    )

    if not saved:
        raise HTTPException(status_code=404, detail="Flight not found")

    db.delete(saved)
    db.commit()
    return {"message": "Flight removed"}

