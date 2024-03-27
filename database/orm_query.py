from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserMessages


async def orm_get_messages(session: AsyncSession):
    query = select(UserMessages.message_id)
    res = await session.execute(query)
    return res.scalars().all()


async def orm_get_message_state(message_id: int, session: AsyncSession):
    query = select(UserMessages.state).where(UserMessages.message_id == message_id)
    res = await session.execute(query)
    return res.scalar()


async def orm_add_message(message_id: int, state: bool, session: AsyncSession):
    obj = UserMessages(
        message_id=message_id,
        state=state
    )
    session.add(obj)
    await session.commit()


async def orm_update_message_state(message_id: int, state: bool, session: AsyncSession):
    query = update(UserMessages).where(UserMessages.message_id == message_id).values(state=state)
    await session.execute(query)
    await session.commit()


async def orm_delete_message(message_id: int, session: AsyncSession):
    query = delete(UserMessages).where(UserMessages.id == message_id)
    await session.execute(query)
    await session.commit()
