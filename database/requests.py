from sqlalchemy import select, update, delete, desc

from database.models import User, async_session

async def get_or_create_user(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user

