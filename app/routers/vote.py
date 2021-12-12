from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas
from .. import models
from .. import oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["vote"],
)


@router.post("/")
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    user_pk: int = Depends(oauth2.get_current_user),
):
    q_post = db.query(models.Post).filter(models.Post.pk == vote.post_id)
    if not q_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    q_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == user_pk,
    )
    if vote.direct == 1:
        if q_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        else:
            new_vote = models.Vote(user_id=user_pk, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"success": f"Added vote to the post: {vote.post_id}"}
    else:
        if not q_vote.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            q_vote.delete(synchronize_session=False)
            db.commit()
            return {"success": f"Deleted vote to the post: {vote.post_id}"}
