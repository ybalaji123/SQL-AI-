from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import Database as db  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/login")
def login(request: LoginRequest):
    result = db.login_user(request.username, request.password)
    if not result["status"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/register")
def register(request: RegisterRequest):
    result = db.register_user(request.username, request.email, request.password)
    if not result["status"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result