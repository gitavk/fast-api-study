from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from ..database import get_db
from ..utils import get_hash

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    data.password = get_hash(data.password)
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
