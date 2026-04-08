from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from typing import Optional, Dict, Any


# Предполагаем, что модель TrainTypes импортирована
from app.models import Trains


def search_train_db(session: Session, unique_id: str) -> Optional[Dict[str, Any]]:
    """
    Находит поезд по unique_id и возвращает информацию о нем и его типе.

    :param session: Активная сессия SQLAlchemy
    :param unique_id: Уникальный идентификатор поезда (строка)
    :return: Словарь с данными или None, если поезд не найден
    """

    # Формируем запрос с подгрузкой связанного объекта (train_type)
    stmt = (
        select(Trains)
        .options(joinedload(Trains.train_type))
        .where(Trains.unique_id == unique_id)
    )

    # Выполняем запрос и получаем один объект
    train = session.scalar(stmt)

    if not train:
        return None

    train_type_data = None

    if train.train_type:
        train_type_data = {
            "id": train.train_type.id,
            "name": train.train_type.name,  # Замените 'name' на реальное поле
            "description": getattr(train.train_type, 'description', None)  # Пример опционального поля
        }
    else:
        train_type_data = {"error": "Тип поезда не найден (возможно, удален)"}

    result = {
        "train": {
            "id": train.id,
            "unique_id": train.unique_id,
            "manufactured_date": train.manufactured_date,
            "details": train.details,
            "type_id": train.type_id
        },
        "train_type": train_type_data
    }

    return result