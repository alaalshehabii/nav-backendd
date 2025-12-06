from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # add foreign key
from sqlalchemy.orm import relationship
from .base import BaseModel
from .comment import CommentModel
from .user import UserModel # add user model

class TeaModel(BaseModel):

    __tablename__ = "teas"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True)
    in_stock = Column(Boolean)
    rating = Column(Integer)

    # NEW: Foreign key linking tea to user
    user_id = Column(Integer, ForeignKey('users.id'))

    # NEW: Relationship - a tea belongs to one user
    user = relationship('UserModel', back_populates='teas')

    comments = relationship("CommentModel", back_populates="tea")
