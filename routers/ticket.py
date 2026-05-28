from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud.ticket import update_ticket, get_ticket_by_id, get_tickets_by_session, get_tickets_by_user
from db.database import get_db
from schemas.ticket import TicketResponse

router=APIRouter(prefix="/api/conversation", tags=["工单"])

#查询工单详情
@router.get("/{ticket_id}")
async def get_ticket(
    data: TicketResponse,
    db: AsyncSession = Depends(get_db)
):
    tickets = await get_ticket_by_id(db, data.ticket_id)

    if not tickets:
        raise HTTPException(status_code=404, detail="工单不存在")

    return {
        "code": 200,
        "message": "查询工单成功",
        "data": {
            "ticket_id": tickets.ticket_id,
            "session_id": tickets.session_id,
            "user_id": tickets.user_id,
            "reason": tickets.reason,
            "status": tickets.status,
            "handler": tickets.handler,
            "created_at": tickets.created_at.isoformat(),
            "resolved_at": tickets.resolved_at.isoformat()
        }
    }

#查询会话的所有工单
@router.get("/session/{session_id}")
async def get_tickets_by_session_id(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    tickets = await get_tickets_by_session(db, session_id)

    if not tickets:
        return {"message":"工单不存在", "code":404}

    return {
        "code": 200,
        "message": "查询工单列表成功",
        "data": {
            "total": len(tickets),
            "list": [
                {
                    "ticket_id": t.ticket_id,
                    "reason": t.reason,
                    "status": t.status,
                    "created_at": t.created_at.isoformat()
                }
                for t in tickets
            ]
        }
    }


#查询用户的所有工单
@router.get("/user/{user_id}",)
async def get_tickets_by_user_id(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):

    tickets = await get_tickets_by_user(db, user_id, skip, limit)

    return{
        "code": 200,
        "message" : "查询用户工单成功",
        "data" : {
            "total": len(tickets),
            "list": [
                {
                "ticket_id": t.ticket_id,
                "reason": t.reason,
                "status": t.status,
                "created_at": t.created_at.isoformat()
                }
            for t in tickets
            ]
        }
    }



#更新工单状态（客服使用）
@router.put("/{ticket_id}")
async def update_status(
    ticket_id: str,
    status: str,
    handler: str = None,
    db: AsyncSession = Depends(get_db)
):
    ticket = await update_ticket(db, ticket_id, status, handler)

    if not ticket:
        raise HTTPException(status_code=404, detail="工单不存在")

    return {"message": "状态更新成功","status": ticket.status}