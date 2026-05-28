
from sqlalchemy import select, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message

#创建消息
async def create_message(
        db:AsyncSession,
        conversation_id: int,
        role: str,content: str,
        sources: list = None
):
    message = Message(conversation_id=conversation_id,role=role,content=content,sources = sources or [])

    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

#获取会话的所有消息
async def get_all_messages(
        db:AsyncSession,
        conversation_id: int,
        skip: int = 0,
        limit: int = 100
):
    sttm = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at).offset(skip).limit(limit)
    result = await db.execute(sttm)

    return result.scalars().all()

#获取最近的消息
async def get_last_messages(
        db:AsyncSession,
        conversation_id: int,
        count = 10
):
    sttm = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.desc()).limit(count)
    result = await db.execute(sttm)

    return list(reversed(result.scalars().all()))


#删除会话的所有消息
async def delete_message(
        db:AsyncSession,
        conversation_id: int
):
    sttm = delete(Message).where(Message.conversation_id == conversation_id)
    result = await db.execute(sttm)

    await db.commit()
    return result.rowcount

#根据ID删除单条消息
async def delete_message_by_id(
        db: AsyncSession,
        message_id: int
):
    sttm = delete(Message).where(Message.id == message_id)
    result = await db.execute(sttm)

    await db.commit()
    return result.rowcount > 0

