from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True)
    contraseña = Column(String)
