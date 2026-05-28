from fastapi import APIRouter, Depends
from langchain_classic.agents import agent
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.chat import ChatRequest
from service.customer_agent import CustomerServiceAgent

router = APIRouter(prefix="/api/chat",tags=["智能问答"])
agent = CustomerServiceAgent()

@router.post("")
async def chat(
        request: ChatRequest,
        db: AsyncSession = Depends(get_db)
):
    if not request.message:
        return{
            "code" : 400,
            "message": "消息不能为空"
        }


    try:
        result = await agent.chat(
            db=db,
            session_id=request.session_id or "",
            user_input=request.message
        )

        return{
            "message":"问答成功",
            "data":{
                "session_id": result["session_id"],
                "response": result["response"],
                "status": result["status"],
                "conversation_id": result["conversation_id"]
            }
        }
    except Exception as e:
        return {
            "code":500,
            "message":f"处理失败: {str(e)}"
        }