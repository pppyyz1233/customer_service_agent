import uuid
from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models.ticket import Ticket

#根据工单号获取工单
async def get_ticket_by_id(
        db: AsyncSession,
        ticket_id: str
):
    stmt = select(Ticket).where(Ticket.ticket_id == ticket_id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_ticket(db: AsyncSession, session_id: str, reason: str, user_id: str = None, last_conversation: str = None):
    ticket = Ticket(
        ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
        session_id=session_id,
        user_id=user_id,
        reason=reason,
        last_conversation=last_conversation,
        status="pending"
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

#获取会话的所有工单
async def get_tickets_by_session(
        db: AsyncSession,
        session_id: str
):
    stmt = select(Ticket).where(Ticket.session_id == session_id).order_by(desc(Ticket.created_at))

    result = await db.execute(stmt)
    return result.scalars().all()

#获取用户的所有工单
async def get_tickets_by_user(
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100
):
    stmt = select(Ticket).where(Ticket.user_id == user_id).order_by(desc(Ticket.created_at)).offset(skip).limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()

#更新工单状态
async def update_ticket(
        db:AsyncSession,
        ticket_id:str,
        status: str,
        handler: str = None
):
    sttm = select(Ticket).where(Ticket.ticket_id == ticket_id)
    result = await db.execute(sttm)
    ticket = result.scalar_one_or_none()

    if ticket:
        ticket.status = status
        if handler:
            ticket.handler = handler
        if status in ["resolved", "closed"]:
            ticket.resolved_at = datetime.now()
        ticket.updated_at = datetime.now()

        await db.commit()
        await db.refresh(ticket)

    return ticket
