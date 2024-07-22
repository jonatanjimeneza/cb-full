from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, protected
import logging
from app.routes import flow


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

# Configura CORS
origins = [
    "http://localhost:3000",  # URL de tu frontend React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(protected.router, tags=["protected"])
app.include_router(flow.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}