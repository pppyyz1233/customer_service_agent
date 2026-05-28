import json
import logging
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from crud.conversation import get_conversations_by_session_id, create_conversation, update_message_cache, \
    set_transferred_to_human, add_tool_calls
from crud.message import create_message, get_all_messages, get_last_messages
from crud.ticket import create_ticket
from tools.agent_tools import AGENT_TOOLS, TOOL_MAP
from utils.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, MAX_TOOL_ITERATIONS

logger = logging.getLogger(__name__)

class CustomerServiceAgent:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError("请配置 DEEPSEEK_API_KEY")

        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.model_name = DEEPSEEK_MODEL
        self.max_tool_iterations = MAX_TOOL_ITERATIONS

        self.system_prompt = {
            "role": "system",
            "content": (
                "你是一个专业、友好的智能客服助手。\n\n"
                "[可用工具]\n"
                "1. check_order_status：查询订单状态\n"
                "2. check_shipping：查询物流信息\n"
                "3. apply_refund：申请退款\n"
                "4. transfer_to_human：转人工客服\n\n"
                "[核心规则]\n"
                "1. 必须调用工具查询真实数据，禁止编造\n"
                "2. 用户没有订单号时，先询问订单号\n"
                "3. 用户情绪激动或要求转人工时，立即调用 transfer_to_human\n"
                "4. 回答要简洁、友好，可适当使用表情符号"
            )
        }

    #处理用户对话
    async def chat(
            self,
            db: AsyncSession,
            session_id: str,
            user_input: str
    ):
        conversation = await get_conversations_by_session_id(db, session_id)

        if not conversation:
            conversation = await create_conversation(db, user_id="")
            session_id = conversation.session_id

        await create_message(db, conversation.id, "user", user_input)

        #构建对话上下文
        history_message = await get_all_messages(db, conversation.id)
        messages = [self.system_prompt]
        for msg in history_message:
            messages.append({"role": msg.role, "content": msg.content})

        iteration = 0
        tool_calls_history = []

        while iteration < self.max_tool_iterations:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=AGENT_TOOLS,
                    tool_choice="auto",
                    temperature=0.7
                )
                response_message = response.choices[0].message
                messages.append(response_message.model_dump())

                #不调用工具
                if not response_message.tool_calls:
                    await create_message(db, conversation.id, "assistant",response_message.content)

                    #构建缓存
                    all_messages = await get_all_messages(db, conversation.id)
                    messages_cache = [
                        {"role":msg.role, "content":msg.content}
                        for msg in all_messages
                    ]
                    await update_message_cache(db, conversation.id, messages_cache)

                    return {
                        "status": "success",
                        "response": response_message.content,
                        "session_id": session_id,
                        "conversation_id": conversation.id,
                        "tool_calls": tool_calls_history
                    }

                #调用工具
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    #转人工处理
                    if func_name == "transfer_to_human":
                        logger.info(f"对话{session_id}，正在转接人工客服")

                        #获取最近10条对话用于工单
                        last_msgs = await get_last_messages(db, conversation.id,count=10)
                        last_conversation = json.dumps([
                            {"role": m.role, "content": m.content}
                            for m in last_msgs
                        ], ensure_ascii=False)

                        #创建工单
                        await create_ticket(db,session_id,func_args.get("reason"),conversation.user_id,last_conversation)
                        await set_transferred_to_human(db, conversation.id)

                        return {
                            "status": "human_fallback",
                            "response": f"正在为您转接人工客服，请稍候...",
                            "session_id": session_id,
                            "conversation_id": conversation.id,
                            "tool_calls": tool_calls_history
                        }

                    #其他工具
                    tool_func = TOOL_MAP.get(func_name)

                    if tool_func:
                        logger.info(f"执行工具: {func_name}, 参数: {func_args}")
                        tool_result = await tool_func(**func_args)#解包字典
                        tool_calls_history.append({"function": func_name,"arguments": func_args,"result": tool_result})
                        await add_tool_calls(db, conversation.id)
                    else:
                        tool_result = json.dumps({"error": f"未知工具: {func_name}"})

                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": tool_result
                    })
                iteration += 1

            except Exception as e:
                logger.error(f"Agent处理出错: {e}")
                return {
                    "status": "error",
                    "response": f"系统繁忙，请稍后重试。",
                    "session_id": session_id,
                    "conversation_id": conversation.id,
                    "tool_calls": tool_calls_history
                }
        return {
            "status": "error",
            "response": "处理超时，请稍后重试或转人工客服。",
            "session_id": session_id,
            "conversation_id": conversation.id,
            "tool_calls": tool_calls_history
        }
