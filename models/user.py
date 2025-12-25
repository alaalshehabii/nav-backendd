from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from config.environment import secret

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    saved_flights = relationship(
        "UserFlight",
        cascade="all, delete",
        backref="user"
    )

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        payload = {
            "sub": str(self.id),
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, secret, algorithm="HS256")
