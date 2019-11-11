from sqlalchemy.orm.exc import NoResultFound
from pixelminer.models.model import Subreddit, Post, Comment
from datetime import datetime


def get_or_create(session, Model, **kwargs):
    try:
        instance = session.query(Model).filter_by(**kwargs).one()
        created = False
    except NoResultFound:
        instance = Model(**kwargs)
        session.add(instance)
        session.commit()
        created = True
    return instance, created


def resolve_subreddit(session, submission):
    subreddit = submission.subreddit
    return get_or_create(
        session,
        Subreddit,
        id=subreddit.id,
        name=subreddit.name,
        display_name=subreddit.display_name
    )

def get_or_update_post(session, subreddit, submission):
    try:
        post = session.query(Post).filter(Post.id == submission.id).one()
        created = False
    except NoResultFound:
        post = Post(
            id=submission.id,
            name=submission.name,
            url=submission.url,
            score=submission.score,
            upvote_ratio=submission.upvote_ratio,
            subreddit=subreddit,
        )
        created = True

    if created or post.last_updated_on < datetime.utcnow():
        # Update
        post.score = submission.score
        post.upvate_ratio=submission.upvote_ratio,
        post.last_updated_on = datetime.utcnow()
        session.add(post)
        session.commit()

    return post, created
