from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Orders, OrderItems


def make_order(db: Session, user_id: int, part_id: int, is_oem: bool = True):
    """
    Создаёт заказ или добавляет позицию в существующий активный заказ.
    Если позиция уже есть в заказе, увеличивает её quantity на 1.
    """
    try:
        # 1. Ищем активный заказ пользователя
        order = db.execute(
            select(Orders)
            .where(Orders.user_id == user_id, Orders.status == 'сформирован')
            .order_by(Orders.created_at.desc())
        ).scalars().first()

        # 2. Если заказа нет или он в другом статусе — создаём новый
        if not order:
            order = Orders(user_id=user_id)  # status='сформирован' по умолчанию
            db.add(order)
            db.flush()  # Генерируем order.id до коммита, чтобы можно было искать элементы

        # 3. Проверяем, есть ли уже такая деталь в этом заказе
        # Благодаря CHECK CONSTRAINT достаточно проверить только одно поле
        condition = OrderItems.oem_part_id == part_id if is_oem else OrderItems.analogue_part_id == part_id
        existing_item = db.execute(
            select(OrderItems).where(OrderItems.order_id == order.id, condition)
        ).scalars().first()

        # 4. Обновляем или создаём позицию
        if existing_item:
            existing_item.quantity += 1
        else:
            new_item = OrderItems(
                order=order,
                oem_part_id=part_id if is_oem else None,
                analogue_part_id=part_id if not is_oem else None,
                quantity=1
            )
            db.add(new_item)

        db.commit()

        return order

    except Exception as e:
        db.rollback()
        raise e