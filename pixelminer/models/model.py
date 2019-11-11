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
from sqlalchemy.orm import backref, relationship
from pixelminer.database import BaseModel as Base, reference_col
from datetime import datetime
import os


class Subreddit(Base):
    """A model for defining a subreddit."""
    __tablename__ = 'subreddits'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), index=True)
    display_name = Column(String(255), index=True)
    posts = relationship('Post', back_populates='subreddit')

    comments = relationship('Comment', back_populates='subreddit')

    def _repr__(self):
        return f'{self.display_name}: r/{self.name}'


class Post(Base):
    """A Model for defining a post within a subreddit."""
    __tablename__ = 'posts'
    id = Column(String(127), primary_key=True)
    name = Column(String(255), index=True)
    url = Column(String(1023), nullable=False, index=True)
    score = Column(Integer, nullable=False, default=0, index=True)
    upvote_ratio = Column(Float, nullable=False, index=True)
    last_updated_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted = Column(Boolean, nullable=False, default=False, index=True)

    comments = relationship('Comment', back_populates='post')

    filepath = Column(String(), nullable=True)
    filehash = Column(Binary(256), nullable=True)
    is_downloaded = Column(Boolean, nullable=False, default=True, index=True)

    subreddit_id = reference_col('subreddits', pk_name='id', index=True)
    subreddit = relationship('Subreddit', back_populates='posts')

    def __repr__(self):
        return f'Post[{self.id}]: {self.url}'

    def download(self):
        """Attempt to download the reddit post."""
        pass


class Comment(Base):
    """A model for encapsulating PRAW's Comment Forest"""
    __tablename__ = 'comments'
    id = Column(String(255), primary_key=True)
    author = Column(String(255), index=True)
    body = Column(String)
    created_utc = Column(DateTime, index=True)
    score = Column(Integer, index=True)

    subreddit_id = Column(String, ForeignKey('subreddits.id'), nullable=False, index=True)
    subreddit = relationship('Subreddit', back_populates='comments')

    post_id = Column(String(127), ForeignKey('posts.id'), nullable=False, index=True)
    post = relationship('Post', back_populates='comments')

    parent_comment_id = Column(String, ForeignKey('comments.id'), nullable=False)
    replies = relationship(
        'Comment',
        backref=backref('parent_comment', remote_side=[id])
    )
