from sqlalchemy import select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import Order

#根据根据订单号获取订单
async def get_order_by_id(
        db:AsyncSession,
        order_id:str
):
    sttm = select(Order).where(Order.order_id == order_id)
    result = await db.execute(sttm)

    return result.scalar_one_or_none()

#更新退款信息
async def update_order_refund(
        db:AsyncSession,
        order_id: str,
        status:str,
        reason:str
):
    sttm = update(Order).where(Order.order_id == order_id).values(status=status,refund_reason=reason)
    result = await db.execute(sttm)

    await db.commit()
    return result.rowcount>0