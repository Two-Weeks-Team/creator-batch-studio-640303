import os
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# ---------------------------------------------------------------------------
# DATABASE ENGINE CONFIGURATION
# ---------------------------------------------------------------------------
_db_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))
# Normalize known async prefixes to the synchronous psycopg driver
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

# Add SSL requirement for non‑local connections (except SQLite)
if not _db_url.startswith("sqlite") and "localhost" not in _db_url and "127.0.0.1" not in _db_url:
    # Ensure sslmode is present; if already present we keep it
    if "sslmode" not in _db_url:
        connector = "?" if "?" not in _db_url else "&"
        _db_url = f"{_db_url}{connector}sslmode=require"

engine = create_engine(_db_url, connect_args={"sslmode": "require"} if not _db_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------------------------------------------------------------------------
# TABLE NAME PREFIX (prevents collisions in shared DB)
# ---------------------------------------------------------------------------
_PREFIX = "cbs_"

# ---------------------------------------------------------------------------
# SQLAlchemy MODELS
# ---------------------------------------------------------------------------
class Batch(Base):
    __tablename__ = f"{_PREFIX}batch"
    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String, nullable=False)
    idea = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships (no type annotations as per constraints)
    hooks = relationship("Hook", back_populates="batch", cascade="all, delete-orphan")
    shots = relationship("Shot", back_populates="batch", cascade="all, delete-orphan")
    lanes = relationship("Lane", back_populates="batch", cascade="all, delete-orphan")
    publish_items = relationship("PublishItem", back_populates="batch", cascade="all, delete-orphan")

class Hook(Base):
    __tablename__ = f"{_PREFIX}hook"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey(f"{_PREFIX}batch.id"), nullable=False)
    platform = Column(String, nullable=False)
    text = Column(Text, nullable=False)

    batch = relationship("Batch", back_populates="hooks")

class Shot(Base):
    __tablename__ = f"{_PREFIX}shot"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey(f"{_PREFIX}batch.id"), nullable=False)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)

    batch = relationship("Batch", back_populates="shots")

class Lane(Base):
    __tablename__ = f"{_PREFIX}lane"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey(f"{_PREFIX}batch.id"), nullable=False)
    platform = Column(String, nullable=False)
    duration = Column(String, nullable=False)  # e.g. "15 s"
    hook_text = Column(Text, nullable=False)

    batch = relationship("Batch", back_populates="lanes")

class PublishItem(Base):
    __tablename__ = f"{_PREFIX}publish_item"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey(f"{_PREFIX}batch.id"), nullable=False)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)

    batch = relationship("Batch", back_populates="publish_items")

# ---------------------------------------------------------------------------
# CREATE SCHEMA & INSERT SEED DATA
# ---------------------------------------------------------------------------
def _seed_data():
    with SessionLocal() as db:
        if db.query(Batch).first():
            return  # already seeded
        # Sample batch: Coffee Hack
        coffee = Batch(batch_name="Coffee Hack", idea="3‑minute coffee hack to boost energy")
        db.add(coffee)
        db.flush()  # obtain coffee.id
        hooks = [
            Hook(batch_id=coffee.id, platform="TikTok", text="Boost your morning in 3 min – coffee hack!"),
            Hook(batch_id=coffee.id, platform="Reels", text="Quick coffee trick for all‑day energy 🌟"),
            Hook(batch_id=coffee.id, platform="Shorts", text="3‑minute coffee boost – try it now!"),
        ]
        shots = [
            Shot(batch_id=coffee.id, description="Intro – creator on kitchen counter", order=1),
            Shot(batch_id=coffee.id, description="Close‑up of coffee beans", order=2),
            Shot(batch_id=coffee.id, description="Pour water & stir", order=3),
            Shot(batch_id=coffee.id, description="Taste test reaction", order=4),
            Shot(batch_id=coffee.id, description="Call‑to‑action overlay", order=5),
        ]
        lanes = [
            Lane(batch_id=coffee.id, platform="TikTok", duration="15 s", hook_text=hooks[0].text),
            Lane(batch_id=coffee.id, platform="Reels", duration="30 s", hook_text=hooks[1].text),
            Lane(batch_id=coffee.id, platform="Shorts", duration="60 s", hook_text=hooks[2].text),
        ]
        publish_items = [
            PublishItem(batch_id=coffee.id, description="Record shots 1‑5", order=1),
            PublishItem(batch_id=coffee.id, description="Edit TikTok version", order=2),
            PublishItem(batch_id=coffee.id, description="Edit Reel version", order=3),
            PublishItem(batch_id=coffee.id, description="Edit Shorts version", order=4),
            PublishItem(batch_id=coffee.id, description="Upload & schedule", order=5),
        ]
        db.add_all(hooks + shots + lanes + publish_items)
        db.commit()

Base.metadata.create_all(bind=engine)
_seed_data()
