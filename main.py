from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import chat, ticket, conversation, user

app = FastAPI(
    title="智能客服工单处理系统",
    description="智能客服调用工具处理问题",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(conversation.router)
app.include_router(ticket.router)