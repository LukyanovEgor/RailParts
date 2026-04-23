from sqlalchemy.orm import Session
from app.models import PartsCategories


def show_image(db: Session, part_category_id: int):
    """
    Возвращает изображение категории
    """
    category = db.query(PartsCategories).filter(
        PartsCategories.id == part_category_id
    ).first()

    return category.img_url