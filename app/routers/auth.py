from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from ..database import get_db
from ..utils import verify_pwd
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["authentication"],
)


@router.post("/login/")
async def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if not verify_pwd(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    access_token = create_access_token(data={"pk": user.pk})

    return {"access_token": access_token, "token_type": "bearer"}
