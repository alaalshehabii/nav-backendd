from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# MODELS 
from models.user import UserModel
from models.flight import Flight
from models.facility import Facility
from models.user_flight import UserFlight   

# ROUTERS
from controllers.users import router as UsersRouter
from controllers.flights import router as FlightsRouter
from controllers.facilities import router as FacilitiesRouter
from controllers.my_flights import router as MyFlightsRouter  

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsersRouter, prefix="/api")
app.include_router(FlightsRouter, prefix="/api")
app.include_router(FacilitiesRouter, prefix="/api")
app.include_router(MyFlightsRouter, prefix="/api") 

@app.get("/")
def home():
    return {"message": "AirNav API running"}
