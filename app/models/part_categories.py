from sqlalchemy import INTEGER, VARCHAR, DATE, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.db import Base


class PartsCategories(Base):
    __tablename__ = 'parts_categories'

    id = Column(INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(INTEGER(), ForeignKey('parts_categories.id', ondelete='SET NULL'), nullable=True)
    train_type_id = Column(INTEGER(), ForeignKey('train_types.id', ondelete='SET NULL'), nullable=True)
    name = Column(VARCHAR(100), nullable=False)
    img_url = Column(VARCHAR(255), nullable=True, unique=True)
    code = Column(VARCHAR(50), nullable=True, unique=True)
    installation_start_date = Column(DATE(), nullable=False)
    installation_end_date = Column(DATE(), nullable=True)

    # relationships

    parent = relationship(
        'PartsCategories',
        remote_side=[id],
        back_populates='children',
        foreign_keys=[parent_id]
    )

    children = relationship(
        'PartsCategories',
        back_populates='parent',
    )

    train_type = relationship(
        'TrainTypes',
        back_populates='parts_categories',
        foreign_keys=[train_type_id]
    )

    oem_parts = relationship(
        'OEMParts',
        back_populates='category'
    )

    def __repr__(self):
        return f"<PartsCategory(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"