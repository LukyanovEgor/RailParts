from sqlalchemy import INTEGER, VARCHAR, DECIMAL, TEXT, TIMESTAMP, Column, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(), ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    status = Column(VARCHAR(20), default='сформирован', nullable=False)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(), server_default=func.now(), onupdate=func.now(), nullable=True)

    # relationships

    user = relationship(
        'Users',
        back_populates='orders',
        foreign_keys=[user_id]
    )

    items = relationship(
        'OrderItems',
        back_populates='order',
        cascade='all, delete-orphan'
    )