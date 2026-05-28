from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import conversation
from crud.conversation import get_conversations_by_session_id, get_conversation_by_id
from crud.message import get_all_messages, get_last_messages
from db.database import get_db
from schemas.conversation import ConversationCreate, ConversationUpdate
from schemas.message import MessageResponse

router=APIRouter(prefix="/api/conversation", tags=["会话管理"])

#创建列表
@router.post("/create_conversation")
async def create_conversation(
        data: ConversationCreate,
        user_id: int,
        db:AsyncSession = Depends(get_db)
):
    response = await conversation.create_conversation(db, user_id, data.title)

    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "id": response.id,
            "user_id": response.user_id,
            "title": response.title,
            "created_at": response.created_at.isoformat(),
            "updated_at": response.updated_at.isoformat()
        }
    }


#根据 session_id 获取会话
@router.get("/session/{session_id}")
async def get_by_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):

    response = await get_conversations_by_session_id(db, session_id)
    if not response:
        raise HTTPException(status_code=404, detail="会话不存在")
    return


#更新会话标题
@router.put("/{conversation_id}/title")
async def update_conversation(
        data:ConversationUpdate,
        conversation_id: int,
        db:AsyncSession = Depends(get_db)
):
    response = await conversation.update_conversation_title(db,conversation_id,data.title)

    return {
        "code":200,
        "message":"更新标题成功",
        "data":{
            "id":response.id,
            "title": response.title
        }
    }


#删除会话
@router.delete("/delete_conversation")
async def delete_conversation(
        conversation_id: int,
        db:AsyncSession = Depends(get_db)
):
    response = await conversation.delete_conversation(db,conversation_id)
    if not response:
        raise HTTPException(status_code=404, detail="会话不存在")

    return {"message": "删除成功",}


#分页获取会话的所有消息
@router.get("/get_all_conversation")
async def get_all_conversation(
        user_id: int,
        conversation_id: int,
        skip: int ,
        limit: int ,
        db:AsyncSession = Depends(get_db)
):
    response = await conversation.get_all_conversations(db, user_id, skip, limit)

    if not response:
        raise HTTPException(status_code=404, detail="会话不存在")

    msgs = await get_all_messages(db, conversation_id, skip, limit)

    return [MessageResponse.model_validate(m) for m in msgs]


#获取最近10条消息
@router.get("/get_last_conversation")
async def get_last_message(
        conversation_id:int,
        count:int,
        db:AsyncSession = Depends(get_db)
):
    response = await get_conversation_by_id(db, conversation_id)

    if not response:
        raise HTTPException(status_code=404, detail="会话不存在")
    msgs = await get_last_messages(db, conversation_id, count)

    return [MessageResponse.model_validate(m) for m in msgs]
