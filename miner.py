#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import os
import click as cli
import configparser
from loguru import logger
from pixelminer.database import Base, initialize_engine
from pixelminer.models.model import Subreddit, Post
from pixelminer.utils import get_or_create, resolve_subreddit, get_or_update_post
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

CONFIG = configparser.ConfigParser()


def run_mining(subreddits):
    engine = initialize_engine(CONFIG)
    Session = sessionmaker(bind=engine)
    session = Session()

    conn = praw.Reddit(
        client_id=CONFIG['PRAW']['CLIENT_ID'],
        client_secret=CONFIG['PRAW']['CLIENT_SECRET'],
        user_agent=CONFIG['PRAW']['USER_AGENT']
    )
    logger.debug(f'Connection read only: {conn.read_only}')
    subreddit_uri = '+'.join(subreddits)
    logger.debug(f'Streaming {subreddits}')
    logger.debug(f'Using URI {subreddit_uri}')

    for raw_submission in conn.subreddit(subreddit_uri).stream.submissions():
        subreddit, created = resolve_subreddit(session, raw_submission)
        if created:
            logger.debug(f'Created subreddit {subreddit.name}')
        post, created = get_or_update_post(session, subreddit, raw_submission)

        if created:
            logger.debug(f'Scraped post: {post}')
        else:
            logger.debug(f'Updated post: {post}')


@cli.group()
@cli.option('--config', type=cli.Path(exists=True, dir_okay=False), default='miner.cfg')
def main(config):
    CONFIG.read(config)
    logger.debug(f'Loaded config {config} with {CONFIG.sections()}')
    if not os.path.exists(CONFIG['IO']['log_dir']):
        os.makedirs(CONFIG['IO']['log_dir'])
    if not os.path.exists(CONFIG['IO']['result_dir']):
        os.makedirs(CONFIG['IO']['result_dir'])


@main.command()
def init_db():
    engine = initialize_engine(CONFIG)
    Base.metadata.create_all(engine)


@main.command()
@cli.argument('subreddits', nargs=-1)
def stream(subreddits):
    while True:
        try:
            run_mining(subreddits)
        except praw.exceptions.PRAWException as e:
            logger.error(f'Encountered {e}. Reconnecting...')

if __name__ == '__main__':
    main()
