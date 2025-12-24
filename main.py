from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from models.flight import Flight  

from controllers.users import router as UsersRouter
from controllers.flights import router as FlightsRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(UsersRouter, prefix="/api")
app.include_router(FlightsRouter, prefix="/api")

@app.get("/")
def home():
    return "Hello World!"
