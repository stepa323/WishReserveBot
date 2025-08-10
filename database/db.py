from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, update, delete
from typing import List, Optional, Union
from datetime import datetime
from .models import User, Wishlist, Item, PriorityLevel
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database operations handler with async SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    # ========== USER OPERATIONS ==========
    async def get_or_create_user(self, telegram_id: int, username: str = None) -> User:
        """Get existing user or create new one"""
        try:
            user = await self.get_user(telegram_id)
            if not user:
                user = User(telegram_id=telegram_id, username=username)
                self.session.add(user)
                await self.session.commit()
                logger.info(f"Created new user: {telegram_id}")
            return user
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error in get_or_create_user: {e}")
            raise

    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    # ========== WISHLIST OPERATIONS ==========
    async def create_wishlist(
        self,
        owner_id: int,
        title: str,
        description: str = None,
        event_date: datetime = None
    ) -> Wishlist:
        """Create new wishlist with validation"""
        if not title:
            raise ValueError("Wishlist title cannot be empty")
            
        wishlist = Wishlist(
            title=title,
            description=description,
            event_date=event_date,
            owner_id=owner_id
        )
        self.session.add(wishlist)
        await self.session.commit()
        await self.session.refresh(wishlist)
        logger.info(f"Created wishlist: {wishlist.id} for user: {owner_id}")
        return wishlist

    async def get_wishlist(self, wishlist_id: int) -> Optional[Wishlist]:
        """Get single wishlist by ID"""
        result = await self.session.execute(
            select(Wishlist).where(Wishlist.id == wishlist_id)
        )
        return result.scalar_one_or_none()

    async def get_user_wishlists(self, owner_id: int) -> List[Wishlist]:
        """Get all wishlists for a user"""
        result = await self.session.execute(
            select(Wishlist)
            .where(Wishlist.owner_id == owner_id)
            .order_by(Wishlist.created_at.desc())
        )
        return result.scalars().all()

    async def update_wishlist(
        self,
        wishlist_id: int,
        title: str = None,
        description: str = None,
        event_date: datetime = None
    ) -> bool:
        """Update wishlist details"""
        update_data = {}
        if title: update_data["title"] = title
        if description is not None: update_data["description"] = description
        if event_date is not None: update_data["event_date"] = event_date

        if not update_data:
            return False

        result = await self.session.execute(
            update(Wishlist)
            .where(Wishlist.id == wishlist_id)
            .values(**update_data)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def delete_wishlist(self, wishlist_id: int) -> bool:
        """Delete wishlist and its items (cascade)"""
        result = await self.session.execute(
            delete(Wishlist).where(Wishlist.id == wishlist_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    # ========== ITEM OPERATIONS ==========
    async def add_item(
        self,
        wishlist_id: int,
        name: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        description: str = None,
        photo_id: str = None,
        price: float = None,
        link: str = None
    ) -> Item:
        """Add item to wishlist with validation"""
        if not name:
            raise ValueError("Item name cannot be empty")

        item = Item(
            name=name,
            description=description,
            photo_id=photo_id,
            price=price,
            link=link,
            priority_level=priority,
            wishlist_id=wishlist_id
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        logger.info(f"Added item: {item.id} to wishlist: {wishlist_id}")
        return item

    async def get_item(self, item_id: int) -> Optional[Item]:
        """Get single item by ID"""
        result = await self.session.execute(
            select(Item).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_wishlist_items(
        self,
        wishlist_id: int,
        priority: PriorityLevel = None
    ) -> List[Item]:
        """Get items in wishlist, optionally filtered by priority"""
        query = select(Item).where(Item.wishlist_id == wishlist_id)
        
        if priority:
            query = query.where(Item.priority_level == priority)
            
        query = query.order_by(
            Item.priority_level.desc(),
            Item.created_at.desc()
        )
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_item(
        self,
        item_id: int,
        name: str = None,
        description: str = None,
        photo_id: str = None,
        price: float = None,
        link: str = None,
        priority: PriorityLevel = None
    ) -> bool:
        """Update item details"""
        update_data = {}
        if name: update_data["name"] = name
        if description is not None: update_data["description"] = description
        if photo_id is not None: update_data["photo_id"] = photo_id
        if price is not None: update_data["price"] = price
        if link is not None: update_data["link"] = link
        if priority: update_data["priority_level"] = priority

        if not update_data:
            return False

        result = await self.session.execute(
            update(Item)
            .where(Item.id == item_id)
            .values(**update_data)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def delete_item(self, item_id: int) -> bool:
        """Delete item from wishlist"""
        result = await self.session.execute(
            delete(Item).where(Item.id == item_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    # ========== SEARCH OPERATIONS ==========
    async def search_items(
        self,
        user_id: int,
        query: str,
        priority: PriorityLevel = None
    ) -> List[Item]:
        """Search items across user's wishlists"""
        search_query = f"%{query}%"
        
        stmt = (
            select(Item)
            .join(Wishlist)
            .where(Wishlist.owner_id == user_id)
            .where(
                or_(
                    Item.name.ilike(search_query),
                    Item.description.ilike(search_query)
                )
            )
        )
        
        if priority:
            stmt = stmt.where(Item.priority_level == priority)
            
        stmt = stmt.order_by(
            Item.priority_level.desc(),
            Item.created_at.desc()
        )
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
