from sqlalchemy.orm import Session

from app.models import PartsCategories
from datetime import date


def get_categories_tree(db: Session, train_type_id: int):
    """
    Возвращает дерево категорий для конкретного train_type_id
    """
    # Загружаем ВСЕ категории для указанного train_type_id
    categories = db.query(PartsCategories).filter(
        PartsCategories.train_type_id == train_type_id
    ).all()

    # Преобразуем в словари
    def category_to_dict(cat):
        return {
            "id": cat.id,
            "parent_id": cat.parent_id,
            "name": cat.name,
            "code": cat.code,
            "img_url": cat.img_url,
            "installation_start_date": cat.installation_start_date.isoformat()
            if isinstance(cat.installation_start_date, date)
            else str(cat.installation_start_date) if cat.installation_start_date else None,
            "children": []
        }

    # Создаем словарь для быстрого доступа по id
    categories_dict = {cat.id: category_to_dict(cat) for cat in categories}

    # Строим дерево
    tree = []
    for cat in categories:
        cat_dict = categories_dict[cat.id]

        if cat.parent_id is None:
            # Корневая категория
            tree.append(cat_dict)
        elif cat.parent_id in categories_dict:
            # Добавляем к родителю
            parent = categories_dict[cat.parent_id]
            parent["children"].append(cat_dict)
        else:
            # Категория с parent_id, которого нет в выборке
            # (может быть если parent_id относится к другому train_type_id)
            # Добавляем как корневую
            tree.append(cat_dict)

    return tree