from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for SQLite"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    wishlists = relationship("Wishlist", back_populates="owner")

class Wishlist(Base):
    """Wishlist model for SQLite"""
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
  
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(String, nullable=True)
  
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="wishlists")
    items = relationship("Item", back_populates="wishlist")

class Item(Base):
    """Wishlist item model for SQLite"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
  
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    photo_id = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    link = Column(String, nullable=True)
    priority_level = Column(String, nullable=False)
  
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    wishlist = relationship("Wishlist", back_populates="items")
