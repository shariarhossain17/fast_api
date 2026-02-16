import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL')


class Base(DeclarativeBase):
    pass


#create database engine

engine=create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)


#create a session

SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False
    autocommit=False
    future=True

)





