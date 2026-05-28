from datetime import datetime

from sqlalchemy import DateTime, func, Integer, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from models.base import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer,ForeignKey("conversation.id", ondelete="CASCADE"),nullable=False,comment="会话ID")
    role: Mapped[str] = mapped_column(Enum("user", "assistant"), nullable=False, comment="角色")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    sources: Mapped[list] = mapped_column(JSON, nullable=True, comment="引用来源")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")