from fastapi import APIRouter
from models.flight import Flight

router = APIRouter()

flights: list[Flight] = []

@router.get("/flights")
def get_flights():
    return flights

@router.post("/flights")
def add_flight(flight: Flight):
    flights.append(flight)
    return flight
