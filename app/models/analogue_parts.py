from sqlalchemy import INTEGER, TEXT, VARCHAR, ForeignKey, Column
from sqlalchemy.orm import relationship
from app.db import Base


class AnalogueParts(Base):
    __tablename__ = 'analogue_parts'

    id = Column(INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    oem_id = Column(INTEGER(), ForeignKey('oem_parts.id', ondelete='SET NULL'), nullable=False)
    analogue_num = Column(TEXT(), nullable=False, unique=True)
    name = Column(TEXT(), nullable=False)
    img_url = Column(VARCHAR(255), nullable=True)
    manufacturer = Column(TEXT(), nullable=False)

    # relationships

    oem_part = relationship(
        'OEMParts',
        back_populates='analogue_parts',
        foreign_keys=[oem_id]
    )

