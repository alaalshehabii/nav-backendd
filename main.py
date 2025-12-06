from fastapi import FastAPI
from controllers.teas import router as TeasRouter
from controllers.users import router as UsersRouter  # Import users router

app = FastAPI()

app.include_router(TeasRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")  # Include users router

@app.get('/')
def home():
    return 'Hello World!'
