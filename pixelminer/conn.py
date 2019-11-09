from celery import Celery

def make_celery_conn(backend='pyampq', broker='pyampq'):
    """Creates a celery connection.
    Args:
        backend (str): The backend for celery to use.
        broker (str):  The broker to store celery results.

    Returns:
        Celery: Returns a celery class.

    """
    raise NotImplementedError
