from sqlalchemy import INTEGER, DECIMAL, TIMESTAMP, Column, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    order_id = Column(INTEGER(), ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    oem_part_id = Column(INTEGER(), ForeignKey('oem_parts.id', ondelete='SET NULL'), nullable=True)
    analogue_part_id = Column(INTEGER(), ForeignKey('analogue_parts.id', ondelete='SET NULL'), nullable=True)
    quantity = Column(INTEGER(), nullable=False, default=1)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)

    # защита на уровне БД, чтобы нельзя было заполнить оба сразу или оставить оба пустыми
    __table_args__ = (
        CheckConstraint(
            '(oem_part_id IS NOT NULL AND analogue_part_id IS NULL) OR '
            '(oem_part_id IS NULL AND analogue_part_id IS NOT NULL)',
            name='chk_one_part_type'
        ),
    )

    # relationships

    order = relationship(
        'Orders',
        back_populates='items'
    )

    oem_part = relationship(
        'OEMParts',
        back_populates='order_items'
    )

    analogue_part = relationship(
        'AnalogueParts',
        back_populates='order_items'
    )