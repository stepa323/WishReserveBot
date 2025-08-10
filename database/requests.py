from sqlalchemy import select, update
from database.models import User, async_session

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
