import logging
import uuid
from datetime import datetime
from typing import Optional, Union
from sqlalchemy import select, func, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload
from database.models import User, Wishlist, async_session, Item, WishlistSubscription

logger = logging.getLogger(__name__)


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


async def get_wishlists(user_id: int) -> list[Wishlist]:
    """Get all active wishlists for specified user"""
    async with async_session() as session:
        result = await session.execute(
            select(Wishlist)
            .where(Wishlist.owner_id == user_id)
            .where(Wishlist.is_deleted == False)
            .order_by(Wishlist.created_at.desc())
        )
        return result.scalars().all() or []


async def get_friends_wishlists(user_id: int) -> Optional[list[Wishlist]]:
    async with async_session() as session:
        result = await session.execute(
            select(Wishlist)
            .join(Wishlist.subscriptions)
            .where(WishlistSubscription.subscriber_id == user_id)
            .where(Wishlist.is_deleted == False)
            .order_by(Wishlist.created_at.desc())
        )
        return result.scalars().unique().all() or []


async def create_or_update_wishlist(
        *,
        wishlist_id: Optional[int] = None,
        user_id: int,
        title: str,
        is_private: bool,
        description: Optional[str] = None,
        event_date: Optional[datetime] = None,
        with_owner: bool = False,
        with_items: bool = False
) -> Wishlist:
    """
    Create or update wishlist
    
    :param is_private: Wishlist privacy
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

        user: User = await get_or_create_user(user_id)

        wishlist = Wishlist(
            title=title,
            is_private=is_private,
            description=description,
            event_date=event_date,
            owner_id=user.id
        )

        session.add(wishlist)
        await session.commit()
        await session.refresh(wishlist)
        return wishlist


async def get_wishlist(
        wishlist_identifier: Union[int, str, uuid.UUID],
        *,
        with_owner: bool = False,
        with_items: bool = False,
        with_subscriptions: bool = False,
        only_active: bool = True
) -> Optional[Wishlist]:
    """
    Retrieve a wishlist by ID or UUID with optional relationships

    Args:
        wishlist_identifier: Can be:
            - int: Wishlist ID
            - str/UUID: Wishlist access UUID
        with_owner: Load owner relationship
        with_items: Load items relationship (uses selectinload for better performance)
        with_subscriptions: Load subscriptions relationship
        only_active: Exclude deleted wishlists

    Returns:
        Wishlist object if found, None otherwise

    Raises:
        ValueError: If invalid identifier type provided
    """
    async with async_session() as session:
        # Build base query
        query = select(Wishlist)

        # Handle different identifier types
        if isinstance(wishlist_identifier, int):
            query = query.where(Wishlist.id == wishlist_identifier)
        elif isinstance(wishlist_identifier, (str, uuid.UUID)):
            try:
                uuid_obj = uuid.UUID(str(wishlist_identifier)) if isinstance(wishlist_identifier,
                                                                             str) else wishlist_identifier
                query = query.where(Wishlist.access_uuid == uuid_obj)
            except ValueError:
                return None
        else:
            raise ValueError("wishlist_identifier must be int or UUID/str")

        # Filter out deleted wishlists if needed
        if only_active:
            query = query.where(Wishlist.is_deleted == False)

        # Eager loading for relationships
        load_options = []

        if with_owner:
            load_options.append(joinedload(Wishlist.owner))
        if with_items:
            load_options.append(selectinload(Wishlist.items))
        if with_subscriptions:
            load_options.append(selectinload(Wishlist.subscriptions))

        if load_options:
            query = query.options(*load_options)

        # Execute query
        result = await session.execute(query)
        wishlist = result.scalars().unique().first()

        return wishlist


async def get_stats() -> tuple[int, int, int]:
    """
    Counts users that use bot and their wishlists and gifts

    :return: Tuple containing (users_count, wishlists_count, gifts_count)
    :rtype: tuple[int, int, int]
    """
    async with async_session() as session:
        # Count users
        users_query = select(func.count()).select_from(User)
        users_count = (await session.execute(users_query)).scalar_one()

        # Count wishlists
        wishlists_query = select(func.count()).select_from(Wishlist)
        wishlists_count = (await session.execute(wishlists_query)).scalar_one()

        # Count gifts
        gifts_query = select(func.count()).select_from(Item)
        gifts_count = (await session.execute(gifts_query)).scalar_one()

        return users_count, wishlists_count, gifts_count


async def get_all_users_id() -> list[int]:
    """
    Gets all users telegram id

    :return: List of ids
    """
    async with async_session() as session:
        query = select(User.telegram_id)
        result = await session.execute(query)
        return result.scalars().all()


async def delete_wishlist_db(wishlist_id: int) -> bool:
    """
    Soft delete wishlist by marking it as deleted
    """
    async with async_session() as session:
        try:
            result = await session.execute(
                update(Wishlist)
                .where(Wishlist.id == wishlist_id)
                .values(is_deleted=True)
            )
            await session.commit()
            return result.rowcount > 0  # Returns True if any row was affected
        except SQLAlchemyError as e:
            logger.error(f"Error deleting wishlist {wishlist_id}: {e}")
            await session.rollback()
            return False
