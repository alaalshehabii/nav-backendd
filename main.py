from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.users import router as UsersRouter
from controllers.flights import router as FlightsRouter

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
