from sqlalchemy import INTEGER, VARCHAR, TEXT, DATE, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.db import Base


class Trains(Base):
    __tablename__ = 'trains'

    id = Column(INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    type_id = Column(INTEGER(), ForeignKey('train_types.id', ondelete='SET NULL'), nullable=False)
    unique_id = Column(VARCHAR(12), nullable=False, unique=True)
    manufactured_date = Column(DATE(), nullable=False)
    details = Column(TEXT(), nullable=True)

    # relationships

    train_type = relationship(
        'TrainTypes',
        back_populates='trains',  # имя в модели TrainTypes
        foreign_keys=[type_id]
    )

    def __repr__(self):
        return f"<Trains(id={self.id}, unique_id='{self.unique_id}', type_id={self.type_id})>"