from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class PriorityLevel(PyEnum):
    """Priority levels for wishlist items with consistent naming"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class User(Base):
    """User model with improved field constraints"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    wishlists = relationship("Wishlist", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}>"

class Wishlist(Base):
    """Wishlist model with optimized field types"""
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="wishlists")
    items = relationship("Item", back_populates="wishlist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Wishlist(id={self.id}, title='{self.title[:20]}...')>"

class Item(Base):
    """Item model with enhanced validation"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    photo_id = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    link = Column(String(500), nullable=True)
    priority_level = Column(
        Enum(PriorityLevel, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=PriorityLevel.MEDIUM
    )
    
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    wishlist = relationship("Wishlist", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name[:15]}...', priority={self.priority_level}>"


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

