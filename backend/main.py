from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User
from passlib.context import CryptContext
from gemini_api import obtener_respuesta
from commands import ejecutar_comando_local

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginInput(BaseModel):
    email: str
    password: str

class ChatInput(BaseModel):
    message: str

class RegisterInput(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usuario == data.email).first()
    if user and pwd_context.verify(data.password, user.contraseña):
        return {"success": True}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.post("/chat")
def chat(data: ChatInput):
    try:
        if data.message.startswith('/'):
            response_comando = ejecutar_comando_local(data.message)
            if response_comando:
                return {"response": response_comando}
        
        response = obtener_respuesta(data.message)
        if response:
            return {"response": response}
        else:
            raise HTTPException(status_code=500, detail="Error al obtener la respuesta de Gemini")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register")
def register(data: RegisterInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usuario == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    hashed_password = pwd_context.hash(data.password)

    new_user = User(usuario=data.email, contraseña=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado exitosamente"}
