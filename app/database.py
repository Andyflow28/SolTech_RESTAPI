import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# Render usa URLs que comienzan con postgres://, pero SQLAlchemy necesita postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,  # Reducido para plan free
    max_overflow=10,  # Ajustado para plan free
    connect_args={
        'sslmode': 'require' if 'render.com' in DATABASE_URL else 'prefer'
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para eliminar y recrear tablas (solo para desarrollo)
def recreate_tables():
    from . import models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)