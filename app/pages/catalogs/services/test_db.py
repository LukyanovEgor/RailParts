from sqlalchemy.orm import Session

from app.models import TrainTypes
from sqlalchemy import select



def get_train_types_all(db: Session):

    query = select(TrainTypes)
    result = db.execute(query)
    types = result.scalars().all()

    return types