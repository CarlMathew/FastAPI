from sqlalchemy import Column, Integer, String, Boolean, DATETIME, TIMESTAMP
from sqlalchemy.sql.expression import text
from database import base


class Post(base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP()'))
