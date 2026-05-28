from datetime import datetime
from sqlalchemy import  DateTime, Integer, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from models.base import Base, TimestampMixin


class Ticket(Base, TimestampMixin):
    """工单表（人工兜底）"""
    __tablename__ = "tickets"

    __table_args__ = (
        Index("idx_ticket_id", "ticket_id"),
        Index("idx_session_id", "session_id"),
        Index("idx_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="工单号")
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, comment="会话ID")
    user_id: Mapped[str] = mapped_column(String(100), nullable=True, comment="用户ID")
    reason: Mapped[str] = mapped_column(String(500), nullable=False, comment="转人工原因")
    last_conversation: Mapped[str] = mapped_column(Text, nullable=True, comment="最后对话")
    status: Mapped[str] = mapped_column(String(20), default="pending",comment="状态")
    handler: Mapped[str] = mapped_column(String(100), nullable=True, comment="处理人")
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, comment="解决时间")