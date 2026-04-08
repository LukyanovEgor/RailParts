from sqlalchemy import INTEGER, TEXT, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.db import Base


class OEMParts(Base):
    __tablename__ = 'oem_parts'

    id = Column(INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    oem_num = Column(TEXT(), nullable=False, unique=True)
    name = Column(TEXT(), nullable=False)
    category_id = Column(INTEGER(), ForeignKey('parts_categories.id', ondelete='SET NULL'), nullable=False)

    # relationships

    category = relationship(
        'PartsCategories',
        back_populates='oem_parts',
        foreign_keys=[category_id]
    )

    analogue_parts = relationship(
        'AnalogueParts',
        back_populates='oem_part'
    )