"""The outlining of the portfolio app models."""
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class BlogPost(Base):
    """Blog Post Model."""

    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    date = Column(Date)

    def to_json(self):
        """JSON."""
        return {
            "title": self.title,
            "body": self.body,
            "date": self.date,
        }

Index('my_index', BlogPost.id, unique=True, mysql_length=255)
