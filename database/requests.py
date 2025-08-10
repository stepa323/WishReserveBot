from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from database.models import User, Wishlist, async_session

async def get_or_create_user(telegram_id: int, username: str | None = None) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        elif username is not None and user.username != username:
            user.username = username
            await session.commit()
            await session.refresh(user)
        
        return user


async def get_wishlists(user_id: int) -> Optional[list[Wishlist]]:
    async with async_session() as session:
        user = await session.scalar(
            select(User)
            .where(User.telegram_id == user_id)
            .options(selectinload(User.wishlists))
        return user.wishlists if user else []


async def create_or_update_wishlist(
    *,
    wishlist_id: Optional[int] = None,
    user_id: int,
    title: str,
    description: Optional[str] = None,
    event_date: Optional[datetime] = None,
    with_owner: bool = False,
    with_items: bool = False
) -> Wishlist:
    """
    Create or update wishlist
    
    :param wishlist_id: ID existing (None for creating new)
    :param user_id: ID owner (user.telegram_id)
    :param title: Wishlist title
    :param description: Description (optional)
    :param event_date: Event date (optional)
    :param with_owner: Upload owners data
    :param with_items: Upload wishlists items
    :return: Object Wishlist
    """
     async with async_session() as session:
        query = select(Wishlist)
        
        if with_owner:
            query = query.options(joinedload(Wishlist.owner))
        if with_items:
            query = query.options(selectinload(Wishlist.items))
        
        if wishlist_id is not None:
            query = query.where(Wishlist.id == wishlist_id)
            wishlist = await session.scalar(query)
            
            if wishlist:
                if description is not None:
                    wishlist.description = description
                if event_date is not None:
                    wishlist.event_date = event_date
                await session.commit()
                await session.refresh(wishlist)
                return wishlist
        
        if title is None:
            raise ValueError("Title is required for new wishlist")
            
        user = await session.scalar(select(User).where(User.telegram_id == user_id))
        if not user:
            raise ValueError(f"User with telegram_id {user_id} not found")
        
        wishlist = Wishlist(
            title=title,
            description=description,
            event_date=event_date,
            owner_id=user.id
        )
        
        session.add(wishlist)
        await session.commit()
        await session.refresh(wishlist)
        return wishlist
