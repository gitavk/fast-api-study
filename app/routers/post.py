from typing import List
from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from .. import oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["post"],
)


@router.get("/", response_model=List[schemas.PostVoteResponse])
async def read(db: Session = Depends(get_db), limit: int = 10):
    q_posts = (
        db.query(
            models.Post,
            func.count(
                models.Vote.post_id,
            ).label("votes"),
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.pk,
            isouter=True,
        )
        .group_by(models.Post.pk)
    )
    return q_posts.limit(limit).all()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create(
    post_data: schemas.Post,
    db: Session = Depends(get_db),
    user_pk: int = Depends(oauth2.get_current_user),
):
    post_data.owner_id = user_pk
    post = models.Post(**post_data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{pid}", response_model=schemas.PostResponse)
async def get(pid: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pk == pid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/{pid}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(pid: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pk == pid)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{pid}")
async def upd(pid: int, post_data: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pk == pid)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post.update(post_data.dict(), synchronize_session=False)
    db.commit()
    return {"data": post.first()}
