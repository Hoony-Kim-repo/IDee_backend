from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from googleLogin.user_requests import router as user_router

origins = ["http://localhost:5173"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
