from datetime import datetime

from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from models.base import TimestampMixin, Base


class Order(Base, TimestampMixin):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id:Mapped[str] = mapped_column(String(20), unique=True,nullable=False,index=True,comment="订单id")
    product_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="产品名称")
    user_name:Mapped[str] = mapped_column(String(20),nullable=False,index=True,comment="用户名")
    status:Mapped[str] = mapped_column(String(20),nullable=False,default="处理中",comment="状态")
    price:Mapped[float] = mapped_column(Float,nullable=False,comment="商品价格")
    shipping_info:Mapped[str] = mapped_column(String(100),nullable=True,comment="物流信息")
    refund_reason:Mapped[str] = mapped_column(String(100),nullable=True,comment="退款原因")


