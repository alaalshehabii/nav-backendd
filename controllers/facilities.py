
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.facility import Facility
from schemas.facility import FacilityCreate, FacilityResponse

router = APIRouter()

@router.get("/facilities", response_model=list[FacilityResponse])
def get_facilities(
    terminal: str | None = Query(None, description="Filter by terminal"),
    db: Session = Depends(get_db)
):
    query = db.query(Facility)

    #  Nearby facilities = same terminal
    if terminal:
        query = query.filter(Facility.terminal == terminal)

    return query.all()


@router.post("/facilities", response_model=FacilityResponse)
def create_facility(
    facility: FacilityCreate,
    db: Session = Depends(get_db)
):
    new_facility = Facility(
        name=facility.name,
        type=facility.type,
        terminal=facility.terminal,
        location_description=facility.location_description
    )

    db.add(new_facility)
    db.commit()
    db.refresh(new_facility)
    return new_facility


@router.put("/facilities/{facility_id}", response_model=FacilityResponse)
def update_facility(
    facility_id: int,
    updated_facility: FacilityCreate,
    db: Session = Depends(get_db)
):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()

    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    facility.name = updated_facility.name
    facility.type = updated_facility.type
    facility.terminal = updated_facility.terminal
    facility.location_description = updated_facility.location_description

    db.commit()
    db.refresh(facility)
    return facility


@router.delete("/facilities/{facility_id}")
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(Facility).filter(Facility.id == facility_id).first()

    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    db.delete(facility)
    db.commit()
    return {"message": "Facility deleted successfully"}

