from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Float,
    DateTime,
    Binary,
    Boolean
)
from pixelminer.database import BaseModel, reference_col
from datetime import datetime
import os


class Subreddit(Base):
    """A model for defining a subreddit."""
    __tablename__ = 'subreddits'
    name = Column(String(255), primary_key=True)
    posts = relationship('RedditPost', back_populates='subreddit')


class Post(Base):
    """A Model for defining a post within a subreddit."""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    url = Column(String(100), nullable=False, index=True)
    score = Column(Integer, nullable=False, default=0, index=True)
    upvote_ratio = Colum(Float, nullable=False, index=True)
    last_updated_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted = Column(Boolean, nullable=False, default=False, index=True)

    filepath = Column(String(), nullable=True)
    filehash = Column(Binary(256), nullable=True)

    subreddit_id = reference_col('subreddits', pk_name='name', index=True)
    subreddit = relationship('Subreddit', back_populates='posts')

    def download(self):
        """Attempt to download the reddit post."""
        pass
