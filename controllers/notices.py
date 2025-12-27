
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.notice import Notice
from schemas.notice import NoticeCreate, NoticeResponse

router = APIRouter()

@router.get("/notices", response_model=list[NoticeResponse])
def get_notices(db: Session = Depends(get_db)):
    return db.query(Notice).order_by(Notice.id.desc()).all()


@router.post("/notices", response_model=NoticeResponse)
def create_notice(notice: NoticeCreate, db: Session = Depends(get_db)):
    new_notice = Notice(
        category=notice.category,
        status=notice.status,
        message=notice.message
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice


@router.delete("/notices/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    db.delete(notice)
    db.commit()
    return {"message": "Notice deleted successfully"}


