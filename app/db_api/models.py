from sqlalchemy import BigInteger, Text, Boolean, DateTime
from sqlalchemy import Column
from sqlalchemy import true
from sqlalchemy.sql.functions import now

from app.db_api.base import Base


class User(Base):
    __tablename__ = "users"
    
    tg_id = Column(BigInteger, primary_key=True)

    username = Column(Text, unique=True)
    banned = Column(Boolean, nullable=False, server_default=true())

    created_at = Column(DateTime, nullable=False, server_default=now())
