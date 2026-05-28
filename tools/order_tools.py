import json
from crud.order import get_order_by_id, update_order_refund
from db.database import AsyncSessionLocal


#检查订单状态
async def check_order_status(order_id:str):
    async with AsyncSessionLocal() as session:
        order = await get_order_by_id(session,order_id)

        if order:
            return json.dumps({
                "status": "success",
                "data": {
                    "order_id": order.order_id,
                    "user_name": order.user_name,
                    "product_name": order.product_name,
                    "status": order.status,
                    "price": order.price,
                    "shipping_info": order.shipping_info
                }
            }, ensure_ascii=False)

        return json.dumps({
            "status": "error",
            "message": f"未找到单号 {order_id} 的订单，请核对订单号。"
        }, ensure_ascii=False)


#查询物流信息
async def check_shipping(order_id: str):
    async with AsyncSessionLocal() as session:
        order = await get_order_by_id(session, order_id)

        if not order:
            return json.dumps({
                "status": "error",
                "message":f"订单{order_id}不存在"
            },ensure_ascii=False)

        shipping_tracking = {
            "ORD-001":[
                {"time": "2026-02-10 08:00", "status": "包裹已揽收", "location": "深圳"},
                {"time": "2026-03-11 14:30", "status": "运输中", "location": "广州"},
                {"time": "2026-05-12 09:00", "status": "派送中", "location": "北京"},
            ],
            "ORD-002": [
                {"time": "2025-12-05 10:00", "status": "已签收", "location": "上海"},
            ],
        }

        tracking = shipping_tracking.get(order_id, [{"status": "暂无物流信息", "location": "未知"}])

        return json.dumps({
            "status": "success",
            "order_id": order_id,
            "product_name": order.product_name,
            "current_status": order.status,
            "shipping_info": order.shipping_info,
            "tracking": tracking
        }, ensure_ascii=False)


#退款
async def apply_refund(order_id: str,reason: str):
    async with AsyncSessionLocal() as session:
        order = await get_order_by_id(session, order_id)

        if not order:
            return json.dumps({
                "status": "error",
                "message":f"订单 {order_id} 不存在，无法退款"
            },ensure_ascii=False)

        if order.status in ['已退款', '退款处理中']:
            return json.dumps({
                "status": "error",
                "message": f"订单当前状态为：{order.status}，请勿重复申请退。"
            }, ensure_ascii=False)

        if order.status == '已签收':
            return json.dumps({
                "status": "warning",
                "message": f"订单 {order_id} 已签收，退款需要您先寄回商品。请问是否需要退货"
            }, ensure_ascii=False)

        success = await update_order_refund(session, order_id, "退款处理中", reason)

        if success:
            return json.dumps({
                "status": "success",
                "message": f"退款申请已提交成功！\n订单号：{order_id}\n退款原因：{reason}\n预计3-7个工作日原路返回"
            }, ensure_ascii=False)

        return json.dumps({
            "status": "error",
            "message": "退款申请提交失败，请稍后重试或联系人工客服。"
        }, ensure_ascii=False)


#转人工
async def transfer_human(reason: str):
    return json.dumps({
        "status": "human_fallback",
        "message": f"请求人工介入，原因：{reason}"
    }, ensure_ascii=False)





