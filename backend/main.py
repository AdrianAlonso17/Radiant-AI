from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai  # Necesitarás la librería de OpenAI para interactuar con su API
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User
from passlib.context import CryptContext

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de la API de OpenAI
openai.api_key = 'AIzaSyC2PsI56K9xohffAoZN33N7wmXq-CvLlHg'  # Reemplaza con tu clave API de OpenAI

# Modelo para el login
class LoginInput(BaseModel):
    email: str
    password: str

# Modelo para el chat
class ChatInput(BaseModel):
    message: str
    
class RegisterInput(BaseModel):
    email: str
    password: str

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de login
@app.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usuario == data.email).first()
    if user and pwd_context.verify(data.password, user.contraseña):
        return {"success": True}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Ruta para el chat
@app.post("/chat")
def chat(data: ChatInput):
    try:
        # Llamamos a la función de Gemini para obtener la respuesta
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



