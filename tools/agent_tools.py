from tools.order_tools import check_order_status, check_shipping, apply_refund, transfer_human


#工具重命名
TOOL_MAP = {
    "check_order_status": check_order_status,
    "check_shipping": check_shipping,
    "apply_refund": apply_refund,
    "transfer_to_human": transfer_human
}



AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "查询订单状态。当用户询问订单详情、订单进度时调用。需要用户提供订单号。",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "订单号，格式如 ORD-001"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_shipping",
            "description": "查询物流信息。当用户询问快递、物流、配送、什么时候到货时调用。需要订单号。",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "订单号"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_refund",
            "description": "处理退款申请。当用户明确要求退款、退货、退钱时调用。需要订单号和原因。",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "订单号"
                    },
                    "reason": {
                        "type": "string",
                        "description": "退款原因"
                    }
                },
                "required": ["order_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "转接人工客服。当用户情绪激动、使用脏话、强烈投诉、或主动要求转人工时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "转接人工的原因"
                    }
                },
                "required": ["reason"]
            }
        }
    }
]