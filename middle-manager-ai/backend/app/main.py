from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .models import SessionLocal, init_db
from pydantic import BaseModel
from .agents import run_agent

app = FastAPI(title="Middle-Manager AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()

class ObjectiveCreate(BaseModel):
    title: str
    description: str

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Middle-Manager AI Core. 100+ Skills Loaded."}

@app.post("/objectives/")
def create_objective(objective: ObjectiveCreate, db: Session = Depends(get_db)):
    db_obj = models.StrategicObjective(title=objective.title, description=objective.description)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # Trigger TaskMaster Agent
    run_agent(f"Decompose this objective into tasks: {objective.title} - {objective.description}")
    return db_obj

@app.post("/chat/")
def chat_with_agent(request: ChatRequest):
    """Entry point for both CEO and Employee to chat with Middle-Manager AI."""
    responses = run_agent(request.message)
    return {"responses": responses}

