from sqlalchemy import INTEGER, TEXT, DATE, Column
from sqlalchemy.orm import relationship
from app.db import Base



class TrainTypes(Base):
    __tablename__ = 'train_types'

    id = Column(INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(TEXT(), nullable=False)
    description = Column(TEXT(), nullable=False)
    prod_start_date = Column(DATE(), nullable=False)
    prod_end_date = Column(DATE(), nullable=True)

    # relationships

    trains = relationship(
        'Trains',
        back_populates='train_type',
        foreign_keys='Trains.type_id'
    )

    parts_categories = relationship(
        'PartsCategories',
        back_populates='train_type'
    )
