import uuid
from datetime import datetime

from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.conversation import Conversation

#根据对话id获取对话:前端返回
async def get_conversations_by_session_id(
        db: AsyncSession,
        session_id: str
):
    sttm =  select(Conversation).where(Conversation.session_id == session_id)
    result = await db.execute(sttm)

    return result.scalar_one_or_none()

#根据id获取会话
async def get_conversation_by_id(
        db: AsyncSession,
        conversation_id: int
):
    sttm = select(Conversation).where(Conversation.id == conversation_id)
    result = await db.execute(sttm)

    return result.scalar_one_or_none()

#获取用户的所有会话
async def get_all_conversations(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
):
    sttm = select(Conversation).where(Conversation.user_id == user_id).order_by(desc(Conversation.updated_at)).offset(skip).limit(limit)
    result = await db.execute(sttm)

    return result.scalars().all()

#创建新会话
async def create_conversation(
        db: AsyncSession,
        user_id: str,
        title: str = "新对话"
):
    session_id = str(uuid.uuid4())
    conversation = Conversation(session_id=session_id, user_id=user_id, title=title)

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation

#更新会话标题
async def update_conversation_title(
        db: AsyncSession,
        conversation_id: int,
        title: str
):
    conversation = await get_conversation_by_id(db, conversation_id)

    if conversation:
        conversation.title = title
        conversation.updated_at = datetime.now()

        await db.commit()
        await db.refresh(conversation)
    return conversation

#删除会话
async def delete_conversation(
        db: AsyncSession,
        conversation_id: int
):
    conversation = await get_conversation_by_id(db, conversation_id)

    if conversation:
        await db.delete(conversation)
        await db.commit()
        return True
    return False


# 更新会话消息缓存
async def update_message_cache(
        db: AsyncSession,
        conversation_id: int,
        messages: list
):
    conversation = await get_conversation_by_id(db, conversation_id)

    if conversation:
        conversation.messages = messages
        conversation.total_messages = len(messages)
        conversation.updated_at = datetime.now()
        await db.commit()
        await db.refresh(conversation)
    return conversation

#增加工具调用次数
async def add_tool_calls(
    db: AsyncSession,
    conversation_id: int,
    increment: int = 1
):
    sttm=update(Conversation).where(Conversation.id == conversation_id).values(tool_calls_count=Conversation.tool_calls_count + increment,updated_at=datetime.now())
    result = await db.execute(sttm)

    await db.commit()
    return result.rowcount > 0


#标记会话已转人工
async def set_transferred_to_human(
    db: AsyncSession,
    conversation_id: int
):
    sttm = update(Conversation).where(Conversation.id == conversation_id).values(transferred_to_human=True, updated_at=datetime.now())
    result = await db.execute(sttm)

    await db.commit()
    return result.rowcount > 0