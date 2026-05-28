from datetime import datetime
from sqlalchemy import Integer, Index, String, Boolean, JSON, DateTime
from sqlalchemy.orm import  DeclarativeBase,Mapped, mapped_column

from models.base import TimestampMixin, Base


class Conversation(Base,TimestampMixin):
    __tablename__ = 'conversation'

    __table_args__ = (
        Index("idx_session_id", "session_id"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="会话ID")
    user_id: Mapped[str] = mapped_column(String(100), nullable=True, comment="用户ID")
    title: Mapped[str] = mapped_column(String(200), default="新对话", comment="会话标题")
    messages: Mapped[list] = mapped_column(JSON, default=list, comment="对话历史")
    total_messages: Mapped[int] = mapped_column(Integer, default=0, comment="总消息数")
    tool_calls_count: Mapped[int] = mapped_column(Integer, default=0, comment="工具调用次数")
    transferred_to_human: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否转人工")