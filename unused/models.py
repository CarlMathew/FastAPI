from database import Base
from sqlalchemy import Column, Integer, String, Boolean, VARCHAR



class Post(Base):
    __tablename__ = "post2"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    published = Column(Boolean, default=True)


