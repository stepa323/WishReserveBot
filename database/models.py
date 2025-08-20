import secrets
import uuid
from email.policy import default

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Enum, Boolean, UUID
from sqlalchemy.orm import relationship, DeclarativeBase

from datetime import datetime, UTC
from enum import Enum as PyEnum
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=False)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.now(UTC))


class PriorityLevel(PyEnum):
    """Priority levels for wishlist items with consistent naming"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SubscriptionStatus(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(Base):
    """User model with improved field constraints"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(50))
    language = Column(String(5), default='en')

    wishlists = relationship("Wishlist", back_populates="owner", cascade="all, delete-orphan")

    subscriptions = relationship(
        "WishlistSubscription",
        back_populates="subscriber",
        foreign_keys="WishlistSubscription.subscriber_id",
        cascade="all, delete-orphan"
    )

    subscription_requests = relationship(
        "WishlistSubscription",
        back_populates="wishlist_owner",
        foreign_keys="WishlistSubscription.wishlist_owner_id",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}>"


class Wishlist(Base):
    """Wishlist model with optimized field types"""
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    is_private = Column(Boolean, nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=True)
    access_uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)

    is_deleted = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="wishlists")
    items = relationship("Item", back_populates="wishlist", cascade="all, delete-orphan")

    subscriptions = relationship(
        "WishlistSubscription",
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )

    def check_access_by_uuid(self, uuid_to_check):
        try:
            return secrets.compare_digest(str(self.access_uuid), str(uuid_to_check))
        except (AttributeError, ValueError):
            return False

    def __repr__(self):
        return f"<Wishlist(id={self.id}, title='{self.title[:20]}...')>"


class WishlistSubscription(Base):
    __tablename__ = "wishlist_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        Enum(SubscriptionStatus, values_callable=lambda x: [e.value for e in x]),
        default=SubscriptionStatus.PENDING,
        nullable=False
    )

    subscriber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscriber = relationship(
        "User",
        back_populates="subscriptions",
        foreign_keys=[subscriber_id]
    )

    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    wishlist = relationship(
        "Wishlist",
        back_populates="subscriptions"
    )

    wishlist_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wishlist_owner = relationship(
        "User",
        back_populates="subscription_requests",
        foreign_keys=[wishlist_owner_id]
    )

    def __repr__(self):
        return f"<Subscription(id={self.id}, status={self.status})>"


class Item(Base):
    """Item model with enhanced validation"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    photo_id = Column(Integer, nullable=True)
    link = Column(String(500), nullable=True)
    price = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    priority_level = Column(
        Enum(PriorityLevel, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=PriorityLevel.MEDIUM
    )

    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)

    wishlist = relationship("Wishlist", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name[:15]}...', priority={self.priority_level}>"


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
