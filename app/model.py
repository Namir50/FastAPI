from .database immport Base
from sqlalchemy import Column, integer

class Post(Base):
    __tablename__ = "posts"

    id = Column(integer)