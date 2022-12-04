from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Float

class Alunos(Base):
    __tablename__ = "alunos"
    matricula = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    idade = Column(Integer)
    curso = Column(String(60), nullable=False)
    nota = Column(Float)


