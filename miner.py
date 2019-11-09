#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import os
import click as cli
from loguru import logger
from pixelminer.database import Base, initialize_engine
from pixelminer.models.model import Subreddit, Post

CONFIG = configparser.ConfigParser()

def run_mining(subreddits):
    conn = praw.Reddit(
        client_id=CONFIG['PRAW']['CLIENT_ID'],
        client_secret=CONFIG['PRAW']['CLIENT_SECRET'],
        user_agent=CONFIG['PRAW']['USER_AGENT']
    )

    for submission in conn.multireddit(*subreddits).stream.submissions():
        pass


@cli.group()
@cli.option('--config', type=cli.Path(exists=True, dir_okay=False), default='miner.cfg')
def main(config):
    CONFIG.read(config)
    if not os.path.exists(CONFIG['IO']['log_dir']):
        os.makedirs(CONFIG['IO']['log_dir'])
    if not os.path.exists(CONFIG['IO']['result_dir']):
        os.makedirs(CONFIG['IO']['result_dir'])


@main.command()
def init_db():
    engine = initialize_engine
    Base.metadata.create_all(engine)


@main.command()
@cli.argument('subreddits', nargs='+')
def stream(subreddits, config):
    print(subreddits)

if __name__ == '__main__':
    main()
