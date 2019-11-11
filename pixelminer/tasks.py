from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import Task


def DBTask(psql_uri):

    class WrappedTask(Task):
        """Wrap the Celery Task to have SQLAlchemy session contexts."""
        _session = None

        def __init__(self):
            self._uri = psql_uri
            self._engine = create_engine(self._uri)
            self._Session = session_maker(bind=self._engine)

        def after_return(self, *args, **kwargs):
            """Clean up"""
            if self._session is not None:
                self._session.remove()

        @property
        def session(self):
            if self._session is None:
                self._session = self._Session()

            return self._session

    return WrappedTask
